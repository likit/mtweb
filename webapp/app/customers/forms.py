# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import (StringField, SubmitField, TextField, SelectField)
from wtforms.validators import DataRequired, Optional


class LabInfoForm(Form):
    org = StringField('Hospital/Company/Organization', validators=[DataRequired()])
    labs = SelectField('Lab/Unit/Department',
            choices=[('', u'โปรดกรอกชื่อหน่วยงาน'),
                        ('Immunology', 'Immunology'),
                        ('Pathology', 'Pathology'),
                        ('Other', 'Other')],
            validators=[DataRequired()])

    new_lab = StringField('Other', validators=[DataRequired()])
    province = StringField('Province', validators=[DataRequired()])
    district = StringField('District', validators=[DataRequired()])
    address = TextField('Address', validators=[DataRequired()])
    submit = SubmitField('Submit')

