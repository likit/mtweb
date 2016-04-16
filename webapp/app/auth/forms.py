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
    firstname = StringField('Name', validators=[DataRequired()])
    lastname = StringField('Lastname', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password',
            validators=[EqualTo('password2'), DataRequired()])
    password2 = PasswordField('Confirmed password', validators=[DataRequired()])
    submit = SubmitField('Submit')
