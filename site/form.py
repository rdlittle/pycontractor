from wtforms import StringField, TextAreaField, validators
from flask_wtf import Form

class ContactForm(Form):
    client_id = StringField('id')
    name = StringField('Name')
    address1 = StringField('Address line 1')
    address2 = StringField('Address line 2')
    city = StringField('City')
    state = StringField('State')
    zipCode = StringField('Zip')
    attn = StringField('Attention')
    phone = StringField('Phone')
    email = StringField('email')
