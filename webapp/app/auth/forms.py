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
    th_firstname = StringField('Thai firstname', validators=[DataRequired()])
    th_lastname = StringField('Thai surname', validators=[DataRequired()])
    en_firstname = StringField('English firstname', validators=[DataRequired()])
    en_lastname = StringField('English surname', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password',
            validators=[EqualTo('password2'), DataRequired()])
    password2 = PasswordField('Confirmed password', validators=[DataRequired()])
    submit = SubmitField('Submit')
