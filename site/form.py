from wtforms import StringField, TextAreaField, validators
from flask_wtf import FlaskForm

class ContactForm(FlaskForm):
    client_id = StringField('id')
    cname = StringField('Name', [
        validators.Length(max=80)
    ])
    address1 = StringField('Address line 1')
    address2 = StringField('Address line 2')
    city = StringField('City')
    state = StringField('State')
    zip_code = StringField('Zip')
    attn = StringField('Attention')
    phone = StringField('Phone')
    email = StringField('email')
