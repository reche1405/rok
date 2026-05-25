from wtforms import Form, StringField, PasswordField, BooleanField, validators
from wtforms.csrf.session import SessionCSRF

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