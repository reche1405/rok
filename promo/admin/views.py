import os, io
from werkzeug.utils import secure_filename
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.form import InlineFormAdmin 
from flask_login import current_user
from flask_admin import form, AdminIndexView, expose
from flask import current_app, redirect, url_for, request, flash
from slugify import slugify
from promo.models import db
from promo.models.list import ListItem
from promo.models.project import Project, Unit
from promo.models.media import Media
from promo.extensions import cache
from wtforms.fields import FileField
from wtforms.validators import Optional
from zipfile import ZipFile
from PIL import Image, ImageOps


# Define where your uploads live on the server
# (Matches the UPLOAD_FOLDER we discussed earlier)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

class InlineMedia(InlineFormAdmin):
    form_columns = ['id', 'title', 'filename', 'relative_path', 'alt_tag', 'slug', 'description']

    # 2. Force Flask-Admin to treat the 'filename' field as an image upload input
    form_extra_fields = {
        'relative_path': FileField(
            'Upload Image',
            base_path=lambda:(current_app.config['UPLOAD_PATH']),
            url_relative_path='media/'
        )
    }


class BaseSecureView(ModelView):
    def is_accessible(self):
        # Only allow access if the user is authenticated
        # Pro tip: If your User model has an 'is_admin' field, check it here: 
        # return current_user.is_authenticated and current_user.is_admin
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # Redirect logged-out users straight to your custom login view.
        # request.url ensures the user is sent back here after typing their password.

        return redirect(url_for('main.login', next=request.url))

class MediaAdminView(BaseSecureView):

    def __init__(self, model, session, *args, **kwargs):
        self.form_args = {
            'relative_path': {
                'label': 'Upload Media File',
                'base_path': current_app.config['UPLOAD_PATH'], # Dynamic import!
                'allow_overwrite': False
            }
        }
        super(MediaAdminView, self).__init__(model, session, *args, **kwargs)
    # 1. Show the path and slug in the dashboard table list
    column_list = ['id', 'title', 'filename', 'slug', 'relative_path']

    # 2. Tell Flask-Admin to render a file upload input instead of a text field
    form_overrides = {
        'relative_path': form.FileUploadField
    }

   

    def on_model_change(self, form, model, is_created):
        """
        SQLAlchemy Hook: This intercepts the form data right before it saves 
        to the database, allowing us to auto-populate the filename and slug.
        """
        if model.relative_path:
            # Flask-Admin's FileUploadField automatically saves the file to disk
            # and updates model.relative_path to just the filename (e.g., "roof_damage.jpg").
            
            # 1. Clean and store the filename safely
            model.filename = secure_filename(model.relative_path)
            
            # 2. Auto-generate the unique slug from the filename (removing extension)
            name_without_ext = os.path.splitext(model.filename)[0]
            
            model.slug = slugify(name_without_ext)


class SlugifyAdminView(BaseSecureView):

    def on_model_change(self, form, model, is_created):
        super().on_model_change(form, model, is_created)
        if model.title:
            model.slug = slugify(model.title)


class ListAdminView(BaseSecureView):
    # This magic line pulls the ListItem form directly into the List view
    inline_models = [ListItem]
    
    # Optional customization:
    # column_list = ('name',)

class CachedAdminView(BaseSecureView):
    def on_model_change(self, form, model, is_created):
        super().on_model_change(form, model, is_created)
        cache.delete('global_site_links')

    def on_model_delete(self, model):
        super().on_model_delete(model)
        cache.delete('global_site_links')


class SecuredAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('main.login', next=request.url))
        return super(SecuredAdminIndexView, self).index()
    



def process_zip_upload( zip_file_storage):
    """
    Takes a FileStorage object (from request.files), extracts images,
    saves them, and returns a list of created Media objects.
    """
    MAX_WIDTH = 1920
    MAX_HEIGHT = 1080
    IMAGE_QUALITY = 82 # 80-85 is the sweet spot for web optimization
    media_objects = []
    
    # Read the zip file into memory
    zip_data = io.BytesIO(zip_file_storage.read())
    upload_path = current_app.config['UPLOAD_PATH']
    
    with ZipFile(zip_data, 'r') as archive:
        for file_info in archive.infolist():
            # Skip directories and hidden system files (like __MACOSX)
            if file_info.is_dir() or file_info.filename.startswith('__'):
                continue
                
            raw_filename = os.path.basename(file_info.filename)
            if raw_filename and allowed_file(raw_filename):
                secure_name = secure_filename(raw_filename)
                
                # Extract the file data as bytes
                #file_bytes = archive.read(file_info.filename)
                
                # --- YOUR EXISTING STORAGE LOGIC HERE ---


                # Example: If you save to a local folder:
                filepath = os.path.join(upload_path, secure_name)
                """ with open(filepath, 'wb') as f:
                    f.write(file_bytes) """
                # ----------------------------------------
                cleaned_name = secure_filename(raw_filename)
                name_without_ext, ext = os.path.splitext(cleaned_name)
                
                # 2. Derive fields
                # Replace dashes/underscores with spaces for a clean title
                title = name_without_ext.replace('-', ' ').replace('_', ' ').title()
                alt_tag = f"Image showing {title}"
                slug = generate_unique_slug(name_without_ext)
            
                # 3. Define and handle paths
                # To prevent filename collisions on disk, you can append the slug to the filename
                final_filename = f"{cleaned_name}"
                relative_path = f'{final_filename}'
                absolute_path = filepath
                
                # Ensure the destination directory exists
                os.makedirs(os.path.dirname(absolute_path), exist_ok=True)

                # --- PILLOW PROCESSING LOGIC ---
                # 1. Read bytes from zip into a stream
                file_bytes = archive.read(file_info.filename)
                image_stream = io.BytesIO(file_bytes)
                
                with Image.open(image_stream) as img:
                    # Fix orientation (Smartphones often save orientation metadata instead of rotating pixels)
                    img = ImageOps.exif_transpose(img)
                    
                    # Convert to RGB if it's RGBA (PNG) so it can save as a JPEG smoothly
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                    
                    # 2. Resize proportionally if it exceeds maximum boundaries
                    img.thumbnail((MAX_WIDTH, MAX_HEIGHT), Image.Resampling.LANCZOS)
                    
                    # 3. Save directly to disk with optimization parameters
                    img.save(absolute_path, optimize=True, quality=IMAGE_QUALITY)
                # -------------------------------
                
                media_item = Media(
                    title=title,
                    filename=final_filename,
                    relative_path=relative_path,
                    alt_tag=alt_tag,
                    slug=slug,
                    description=f"Bulk uploaded via zip archive: {zip_file_storage.filename}"
                )
                
                db.session.add(media_item)
                media_objects.append(media_item)
                
    return media_objects

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
def generate_unique_slug( base_title):
    """Generates a clean, unique slug by checking the database."""
    base_slug = slugify(base_title)
    if not base_slug:
        base_slug = "media-file"
        
    slug = base_slug
    counter = 1
    
    # Loop to ensure uniqueness against existing slugs
    while Media.query.filter_by(slug=slug).first() is not None:
        slug = f"{base_slug}-{counter}"
        counter += 1
        
    return slug
 


class ProjectAdminView(BaseSecureView):
    """Admin view for Project with inline Units in the form."""
    # Show units inline on the project edit/create form
    form_columns = ['title', 'featured', 'location', 'desc', 'short_desc', 'media', 'featured_media', 'zip_file', 'type', 'zip_file']
    inline_models = [ 
        (Media, {
            'label' : "Featured Media",
            'form_class': InlineMedia,
            'prop_name': 'featured_media' # The exact name of your model's ForeignKey relationship
        }),
        Unit                 
    ]
    form_extra_fields = {
        'zip_file': FileField('Bulk Upload Images (.zip)', validators=[Optional()])
    }
    # Optionally auto-generate slug from project title
    def on_model_change(self, form, model, is_created):
        super().on_model_change(form, model, is_created)
        if getattr(model, 'title', None):
            base_slug  = slugify(model.title)
            counter = 1
            slug = base_slug
        # Loop to ensure uniqueness against existing slugs
        while Media.query.filter_by(slug=slug).first() is not None:
            slug = f"{base_slug}-{counter}"
            counter += 1
        model.slug = slug    

        if form.zip_file.data:
            zip_file_storage = form.zip_file.data
            
            if zip_file_storage.filename.endswith('.zip'):
                try:
                    # 1. Process zip and get the list of created Media objects
                    new_media_items = process_zip_upload(zip_file_storage)
                    
                    if new_media_items:
                        # 2. Append to the many-to-many relationship
                        # 'media' is the relationship attribute on your Project model
                        model.media.extend(new_media_items)
                        
                        # Inform the admin user of success
                        flash(f'Successfully extracted and linked {len(new_media_items)} images.', 'success')
                    else:
                        flash('Zip file parsed, but no valid images were found.', 'warning')
                        
                except Exception as e:
                    # Flask-Admin handles exceptions gracefully, but dropping a flash helps
                    flash(f'Error processing zip file: {str(e)}', 'error')
                    raise e # Raising the exception rolls back the DB transaction automatically
            else:
                flash('Uploaded file was not a valid ZIP archive.', 'error')
       
class UnitAdminView(BaseSecureView):
    form_columns = ['title', 'description', 'featured_media', 'media', 'project', 'zip_file' ]
    form_extra_fields = {
        'zip_file': FileField('Bulk Upload Images (.zip)', validators=[Optional()])
    }

    def on_model_change(self, form, model, is_created):
        super().on_model_change(form, model, is_created)
        if getattr(model, 'title', None):
            base_slug  = slugify(model.title)
            counter = 1
            slug = base_slug
        # Loop to ensure uniqueness against existing slugs
        while Media.query.filter_by(slug=slug).first() is not None:
            slug = f"{base_slug}-{counter}"
            counter += 1
        model.slug = slug    

        if form.zip_file.data:
            zip_file_storage = form.zip_file.data
            
            if zip_file_storage.filename.endswith('.zip'):
                try:
                    # 1. Process zip and get the list of created Media objects
                    new_media_items = process_zip_upload(zip_file_storage)
                    
                    if new_media_items:
                        # 2. Append to the many-to-many relationship
                        # 'media' is the relationship attribute on your Project model
                        model.media.extend(new_media_items)
                        model.project.media.extend(new_media_items)
                        # Inform the admin user of success
                        flash(f'Successfully extracted and linked {len(new_media_items)} images.', 'success')
                    else:
                        flash('Zip file parsed, but no valid images were found.', 'warning')
                        
                except Exception as e:
                    # Flask-Admin handles exceptions gracefully, but dropping a flash helps
                    flash(f'Error processing zip file: {str(e)}', 'error')
                    raise e # Raising the exception rolls back the DB transaction automatically
            else:
                flash('Uploaded file was not a valid ZIP archive.', 'error')
    