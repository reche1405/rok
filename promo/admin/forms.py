from wtforms import Form, StringField, PasswordField, BooleanField, validators
from wtforms.csrf.session import SessionCSRF
from flask_admin.form import FileUploadField
from markupsafe import Markup
class LoginForm(Form):
    class Meta:
        csrf = True
        csrf_class = SessionCSRF  
        csrf_secret = b'yD5g@4]!wer45g8fda5thk^wtyokVe468f3v{/}' 
    username = StringField(
        u'Username',
        validators=[
            validators.input_required(), 
            validators.length(min=5,max=12, message="Please enter a username within 5 and 12 characters."),
            ]
    )
    password = PasswordField(
        u'Password',
        validators=[
            validators.input_required(),
            validators.length(8, 60, "Password must be between 8 and 60 characters."),
        ]
    )
    remember_me = BooleanField(
        u'Remember Me',
        default=False
    )


class ImagePreviewWidget(FileUploadField):
    def __call__(self, field, **kwargs):
        # Render the standard file upload input HTML
        html = super(ImagePreviewWidget, self).__call__(field, **kwargs)
        
        # If the model already has an image path, prepend the image preview HTML
        if field.data:
            # Adjust "/static/uploads/" to match your routing setup
            preview_html = f'<div style="margin-bottom: 10px;"><img src="/media/{field.data}" style="max-height: 150px; border: 1px solid #ddd; padding: 5px; border-radius: 4px;"></div>'
            html = Markup(preview_html) + html
            
        return html