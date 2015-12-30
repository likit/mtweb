#! -*- coding: utf-8 -*-
import datetime
from app import db, flask_bcrypt
from sqlalchemy.ext.hybrid import hybrid_property
from flask.ext.login import UserMixin, AnonymousUserMixin


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(255), unique=True)
    created_on = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    firstname = db.Column(db.String(128), unique=True)
    lastname = db.Column(db.String(128), unique=True)
    _password = db.Column('password', db.String(60))
    affiliation_id = db.Column(db.Integer, db.ForeignKey('affiliations.id'))
    user_type = db.Column(db.Integer)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __init__(self, email, firstname, lastname,
                    password, role, user_type):
        self.email = email
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.role = role
        self.user_type = user_type

    def __repr__(self):
        return '<User %r>' % self.username

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = flask_bcrypt.generate_password_hash(password)

    def can(self, permissions):
        return self.role is not None and \
                (self.role.permissions & permissions) == permissions

    def correct_user_type(self, utype):
        return self.user_type is not None and (self.user_type) == utype

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

#TODO: Add AnonymousUserMixin class
class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


class OrgType(db.Model):
    __tablename__ = 'org_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    th_name = db.Column(db.String(255))
    affiliations = db.relationship('Affiliation',
            backref='org_type', lazy='dynamic')

    @staticmethod
    def insert_types():
        types = {
                'hospital': 'โรงพยาบาล',
                'private': 'เอกชน',
                'government': 'รัณบาล',
                'academic': 'สถาบัรการศึกษา',
                'personal': 'ส่วนตัว',
                'research': 'งานวิจัย',
                'other': 'อื่นๆ',
                }

        for t,th_name in types.iteritems():
            if not OrgType.query.filter_by(name=t).first():
                ot = OrgType(name=t, th_name=unicode(th_name, 'utf8'))
                db.session.add(ot)

        db.session.commit()


class OrgPwd(db.Model):
    __tablename__ = 'orgpwds'
    id = db.Column(db.Integer, primary_key=True)
    expiration_date = db.Column(db.DateTime())
    created_date = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    affiliations = db.relationship('Affiliation', backref='orgpwd',
            lazy='dynamic')

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = flask_bcrypt.generate_password_hash(password)


class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    affiliations = db.relationship('Affiliation', backref='service',
            lazy='dynamic')


class Affiliation(db.Model):
    __tablename__ = 'affiliations'
    id = db.Column(db.Integer, primary_key=True)
    org_type_id = db.Column(db.Integer, db.ForeignKey('org_types.id'))
    org = db.Column(db.String(255))
    labname = db.Column(db.String(255))
    province = db.Column(db.String(255))
    district = db.Column(db.String(255))
    address = db.Column(db.Text())
    users = db.relationship('User', backref='affiliation', lazy='dynamic')
    added_on = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    password_id = db.Column(db.Integer, db.ForeignKey('orgpwds.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))

    def __init__(self, org, province, district,
                        labname=None, address=None):
        self.org = org
        self.labname = labname
        self.province = province
        self.district = district
        self.address = address


class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80


class UserType:
    STUDENT = 0x01
    STAFF = 0x02
    TEACHER = 0x04
    CUSTOMER = 0x08


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %s>' % self.name

    @staticmethod
    def insert_roles():
        roles = {
                'User': (Permission.FOLLOW |
                    Permission.COMMENT |
                    Permission.WRITE_ARTICLES, True),
                'Moderator': (Permission.COMMENT |
                    Permission.FOLLOW |
                    Permission.WRITE_ARTICLES |
                    Permission.MODERATE_COMMENTS, False),
                'Administrator': (0xff, False)
                }

        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

