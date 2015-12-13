# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import (DataRequired, Email,
                                    Length, EqualTo, Optional)

class LoginForm(Form):
    '''Login form.'''
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(Form):
    org = StringField('org', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    labs = SelectField('labs', choices=[('', u'โปรดกรอกชื่อหน่วยงาน')],
            validators=[DataRequired()])
    addlab = StringField('addlab', validators=[DataRequired()])
    lastname = StringField('lastname', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password',
            validators=[EqualTo('password2'), DataRequired()])
    password2 = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Submit')

