#! -*- coding: utf-8 -*-
from datetime import datetime
from app import db, flask_bcrypt
from sqlalchemy.ext.hybrid import hybrid_property


class QStakeholderQuestion(db.Model):
    '''
    Stakeholder questions.
    '''
    __tablename__ = 'qstakeholder_questions'
    id = db.Column(db.Integer(), primary_key=True)
    taker_id = db.Column(db.Integer(), db.ForeignKey('qstakeholder_takers.id'))
    order = db.Column(db.Integer())
    qtext = db.Column(db.Text())
    discipline = db.Column(db.String(4))
    taker = db.relationship('QStakeholderTakers',
                backref=db.backref('questions', lazy='dynamic'))


class QStakeholders(db.Model):
    '''
    Stakeholders evaluation scores.
    '''

    __tablename__ = 'qstakeholders'
    id = db.Column(db.Integer(), primary_key=True)
    taker_id = db.Column(db.Integer(),
                db.ForeignKey('qstakeholder_takers.id'))
    question_id = db.Column(db.Integer(),
                db.ForeignKey('qstakeholder_questions.id'))
    qanswer = db.Column(db.Text())
    qyear = db.Column(db.String(12))
    question = db.relationship('QStakeholderQuestion',
                    backref=db.backref('answers', lazy='dynamic'))


class QStakeholderTakers(db.Model):
    '''
    Stakeholders.
    '''

    __tablename__ = 'qstakeholder_takers'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Text())
    position = db.Column(db.String(255))
    institution_type = db.Column(db.String(255))
    affiliation = db.Column(db.String(255))
    alumni = db.Column(db.String(255))
    supervisor_position = db.Column(db.String(255))
    assigned_rep_position = db.Column(db.String(255))
    executive_year = db.Column(db.Integer())
    qyear = db.Column(db.String(12))
    discipline = db.Column(db.String(4))


class QWellroundedQuestion(db.Model):
    '''
    Wellrounded questions.
    '''
    __tablename__ = 'qwellrounded_questions'
    id = db.Column(db.Integer(), primary_key=True)
    order = db.Column(db.Integer())
    qtext = db.Column(db.Text())


class QWellrounded(db.Model):
    '''
    Wellrounded answers.
    '''
    __tablename__ = 'qwellroundeds'
    id = db.Column(db.Integer(), primary_key=True)
    taker_id = db.Column(db.Integer(),
                db.ForeignKey('qwellrounded_takers.id'))
    question_id = db.Column(db.Integer(),
                    db.ForeignKey('qwellrounded_questions.id'))
    qanswer = db.Column(db.Text())
    qyear = db.Column(db.String(12))
    taker = db.relationship('QWellroundedTaker',
                    backref=db.backref('questions', lazy='dynamic'))
    question = db.relationship('QWellroundedQuestion',
                    backref=db.backref('answers', lazy='dynamic'))


class QWellroundedTaker(db.Model):
    '''
    Takers.
    '''
    __tablename__ = 'qwellrounded_takers'
    id = db.Column(db.Integer(), primary_key=True)
    fullname = db.Column(db.String(255))
    discipline = db.Column(db.String(255))
    line_id = db.Column(db.String(255))
    facebook_id = db.Column(db.String(255))
    email = db.Column(db.String(255))
