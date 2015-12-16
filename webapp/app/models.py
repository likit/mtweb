import datetime
from app import db, flask_bcrypt
from sqlalchemy.ext.hybrid import hybrid_property

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(255), unique=True)
    created_on = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    username = db.Column(db.String(40), unique=True)
    _password = db.Column('password', db.String(60))

    def __init__(self, email, username, password):
        self.email = email
        self.password = password
        self.username = username

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


class LabInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    org = db.Column(db.String(255))
    labs = db.Column(db.String(255))
    province = db.Column(db.String(255))
    district = db.Column(db.String(255))
    address = db.Column(db.Text())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User',
            backref=db.backref('labinfo', lazy='dynamic'))
    added_on = db.Column(db.DateTime, default=datetime.datetime.utcnow())
