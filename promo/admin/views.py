import os
from werkzeug.utils import secure_filename
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask_admin import form, AdminIndexView, expose
from flask import current_app, redirect, url_for, request
from slugify import slugify
from models.list import ListItem
from models.project import Project, Unit

# Define where your uploads live on the server
# (Matches the UPLOAD_FOLDER we discussed earlier)
UPLOAD_PATH = current_app

class BaseSecureView(ModelView):
    def is_accessible(self):
        # Only allow access if the user is authenticated
        # Pro tip: If your User model has an 'is_admin' field, check it here: 
        # return current_user.is_authenticated and current_user.is_admin
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # Redirect logged-out users straight to your custom login view.
        # request.url ensures the user is sent back here after typing their password.
        return redirect(url_for('login', next=request.url))

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
        if model.title:
            model.slug = slugify(model.title)


class ListAdminView(BaseSecureView):
    # This magic line pulls the ListItem form directly into the List view
    inline_models = [ListItem]
    
    # Optional customization:
    # column_list = ('name',)


class SecuredAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('login', next=request.url))
        return super(SecuredAdminIndexView, self).index()


class ProjectAdminView(BaseSecureView):
    """Admin view for Project with inline Units in the form."""
    # Show units inline on the project edit/create form
    inline_models = [Unit]

    # Optionally auto-generate slug from project title
    def on_model_change(self, form, model, is_created):
        if getattr(model, 'title', None):
            model.slug = slugify(model.title)
    

    
