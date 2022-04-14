from . import db # import from website folder
from flask_login import UserMixin

class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    disease = db.Column(db.String(150))
    score = db.Column(db.Integer)
    notes = db.Column(db.String(10000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True) # max length is 150
    password = db.Column(db.String(150))
    username = db.Column(db.String(50))
    alzheimer = db.Column(db.String(150))
    parkinson = db.Column(db.String(150))
    assessments = db.relationship('Assessment')