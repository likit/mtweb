from flask.ext.wtf import Form
from wtforms import (StringField, SubmitField, IntegerField,
                        TextAreaField, SelectField, BooleanField)
from wtforms.validators import (DataRequired, Email,
                                    Length, EqualTo, Optional)


class EditProfileForm(Form):
    username = StringField('Username', validators=[Length(0,255)])
    location = StringField('Location', validators=[Length(0,255)])
    about_me = TextAreaField('About me')
    office_room = StringField('Office room', validators=[Length(max=8)])
    office_phone = StringField('Office phone', validators=[Length(max=8)])
    mobile_phone = StringField('Mobile phone', validators=[Length(max=10)])
    car_license_plate = StringField('License plate', validators=[Length(max=8)])
    academic_position = SelectField('Academic position', coerce=int)
    department = SelectField('Department')
    submit = SubmitField('Submit')


class AdminEditProfileForm(Form):
    th_firstname = StringField('Thai firstname',
            validators=[Length(0,255), DataRequired()])
    th_lastname = StringField('Thai lastname',
            validators=[Length(0,255), DataRequired()])
    en_firstname = StringField('Eng firstname',
            validators=[Length(0,255), DataRequired()])
    en_lastname = StringField('Eng lastname',
            validators=[Length(0,255), DataRequired()])
    username = StringField('Username', validators=[Length(0,255)])
    email = StringField('Email',
            validators=[Email(), Length(0,255), DataRequired()])
    about_me = TextAreaField('About me')
    title = SelectField('Title', coerce=int)
    office = SelectField('Office', coerce=int)
    mobile_phone = StringField('Mobile phone',
            validators=[Length(max=10)])
    car_license_plate = StringField('License plate',
            validators=[Length(max=8)])
    academic_position = SelectField('Academic position', coerce=int)
    department = SelectField('Department',
                                coerce=int, validators=[DataRequired()])
    job = SelectField('Job', coerce=int, validators=[DataRequired()])
    #TODO: Education field
    gender = IntegerField('Gender')
    mobile_phone = StringField('Mobile phone', validators=[Length(0,24)])
    fax = StringField('Fax', validators=[Length(0,24)])
    user_type = SelectField('User Type', validators=[DataRequired()])
    submit = SubmitField('Submit')
