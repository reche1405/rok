from wtforms import Form, validators
from wtforms.fields import StringField, TextAreaField
from wtforms.fields.html5 import TelField, EmailField
from wtforms.csrf.session import SessionCSRF
class ContactForm(Form):
    class Meta:
        csrf = True
        csrf_class = SessionCSRF  
        csrf_secret = b'yD5g@4]!wer45g8fda5thk^wtyokVe468f3v{/}' 
    name = StringField(
        "Name",
        validators=[
            validators.input_required()
        ], 
        render_kw= {
            "placeholder" : "Joe Bloggs",
            "class" : ""
        }
    )
    email = EmailField(
        "Email",
        validators=[
            validators.input_required()
        ], 
        render_kw= {
            "placeholder" : "joe.bloggs@email.com",
            "class" : ""
        }
    )
    number = TelField(
        "Telephone",
        validators=[
            validators.input_required()
        ],
        render_kw= {
            "placeholder" : "07912 345 678",
            "class" : " mb-3"
        }
    )
    message = TextAreaField(
        "Message",
        validators=[
            validators.input_required()
        ],
        render_kw= {
            "placeholder" : "Tell us about your project...",
            "class" : ""
        })