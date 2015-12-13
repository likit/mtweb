from app import db
import datetime

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(255), unique=True)
    created_on = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    username = db.Column(db.String(40), unique=True)
