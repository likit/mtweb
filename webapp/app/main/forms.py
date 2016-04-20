from flask.ext.wtf import Form
from wtforms import (StringField, SubmitField,
                        TextAreaField, SelectField, BooleanField)
from wtforms.validators import (DataRequired, Email,
                                    Length, EqualTo, Optional)


class EditProfileForm(Form):
    username = StringField('Username', validators=[Length(0,255)])
    location = StringField('Location', validators=[Length(0,255)])
    about_me = TextAreaField('About me')
    office_room = StringField('Office room', validators=[Length(min=4,max=8)])
    office_phone = StringField('Office phone', validators=[Length(max=8)])
    mobile_phone = StringField('Mobile phone', validators=[Length(max=10)])
    car_license_plate = StringField('License plate', validators=[Length(max=8)])
    academic_position = SelectField('Academic position')
    department = SelectField('Department')
    submit = SubmitField('Submit')
