#! -*- coding: utf-8 -*-

from app import db, flask_bcrypt
from app.models import Lab
from datetime import datetime

class QACustomerCode(db.Model):
    __tablename__ = 'customercodes'
    id = db.Column(db.Integer(), primary_key=True)
    qa_program_id = db.Column(db.Integer(), db.ForeignKey('qaprograms.id'))
    lab_id = db.Column(db.Integer(), db.ForeignKey('labs.id'))
    customer_code = db.Column(db.String(128)) # customer code

    program = db.relationship('QAProgram', backref='customer_codes',
                            foreign_keys='QACustomerCode.qa_program_id')

    lab = db.relationship('Lab', backref='eqa_customer_codes',
                            foreign_keys='QACustomerCode.lab_id')
    current_authorized_user = db.relationship('User', uselist=False)

    def __repr__(self):
        return "<QACustomerCode %s>" % self.customer_code


class QAProgram(db.Model):
    __tablename__ = 'qaprograms'
    id = db.Column(db.Integer(), primary_key=True)
    customer_code_id = db.Column(db.Integer(),
                            db.ForeignKey('customercodes.id'))
    en_name = db.Column(db.String(255))
    th_name = db.Column(db.String(255))
    code_name = db.Column(db.String(64))

    def __repr__(self):
        return "<QAProgram %s>" % self.en_name


class OTPCode(db.Model):
    __tablename__ = 'otpcodes'
    id = db.Column(db.Integer(), primary_key=True)
    code = db.Column(db.String(64))
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    lifespan = db.Column(db.Integer())
    used = db.Column(db.Boolean())
    used_by = db.Column(db.Integer(), db.ForeignKey('users.id'))
    customer_code_id = db.Column(db.Integer(),
                        db.ForeignKey('customercodes.id'))

    customer_code = db.relationship('QACustomerCode',
            backref='otp_codes', foreign_keys='OTPCode.customer_code_id')

    def __repr__(self):
        return "<OTPCode %s>" % self.code
