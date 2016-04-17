from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import (DataRequired, Email,
                                    Length, EqualTo, Optional)
class EditProfileForm(Form):
    username = StringField('Username', validators=[Length(0,255)])
    location = StringField('Location', validators=[Length(0,255)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')
