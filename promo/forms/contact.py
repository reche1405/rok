from wtforms import Form, validators
from wtforms.fields import StringField, TextAreaField
from wtforms.fields.html5 import TelField, EmailField
from wtforms.csrf.session import SessionCSRF
from flask_wtf import RecaptchaField
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
            "placeholder" : "",
            "class" : "",
            "name" : "entry.845568049"
        }
    )
    email = EmailField(
        "Email",
        validators=[
            validators.input_required()
        ], 
        render_kw= {
            "placeholder" : "",
            "class" : "",
            "name" : "entry.169352832"

        }
    )
    number = TelField(
        "Telephone",
        validators=[
            validators.input_required()
        ],
        render_kw= {
            "placeholder" : "",
            "class" : " mb-3",
            "name" : "entry.1928429605"
            
        }
    )
    message = TextAreaField(
        "Message",
        validators=[
            validators.input_required()
        ],
        render_kw= {
            "placeholder" : "",
            "class" : "",
            "name" : "entry.1495316646"
        })
    recaptcha = RecaptchaField()