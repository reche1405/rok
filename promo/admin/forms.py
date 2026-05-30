from wtforms import Form, StringField, PasswordField, BooleanField, validators
from wtforms.csrf.session import SessionCSRF
from flask_admin.form import FileUploadField, FileUploadInput
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


# 1. Keep the custom widget as it was
class ImagePreviewWidget(FileUploadInput):
    def __call__(self, field, **kwargs):
        html = super(ImagePreviewWidget, self).__call__(field, **kwargs)
        if field.data:
            # Adjust "/static/uploads/" to your setup
            preview_html = f'<div style="margin-bottom: 10px;"><img src="/static/uploads/{field.data}" style="max-height: 150px; border: 1px solid #ddd; padding: 5px; border-radius: 4px;"></div>'
            html = Markup(preview_html) + html
        return html

# 2. Define a custom field that uses your widget by default
class PreviewFileUploadField(FileUploadField):
    widget = ImagePreviewWidget()