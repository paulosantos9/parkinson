from . import db # import from website folder
from flask_login import UserMixin

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    gameTypeIndex = db.Column(db.Integer)
    currentTime = db.Column(db.DateTime)
    timeSpent = db.Column(db.String(50))
    score = db.Column(db.String(50))
    image = db.Column(db.Text)
    audioPath = db.Column(db.String(50))
    jitter = db.Column(db.String(50))
    shimmer = db.Column(db.String(50))

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    indexInAssessment = db.Column(db.Integer)
    question = db.Column(db.Integer)
    answer = db.Column(db.Integer)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessment.id'))

class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    testType = db.Column(db.String(150))
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    currentTime = db.Column(db.DateTime)
    doctorNotes = db.Column(db.String(10000))
    questions = db.relationship('Question')

class Achievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    locked = db.Column(db.Boolean)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    icon = db.Column(db.String(50))
    description = db.Column(db.String(150))

class Person(db.Model, UserMixin):
    __abstract__ = True
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(270))

class Doctor(Person):
    id = db.Column(db.Integer, primary_key=True)
    patientsList = db.relationship('Patient')

class Patient(Person):
    id = db.Column(db.Integer, primary_key=True)
    observations = db.Column(db.String(10000))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    assessments = db.relationship('Assessment')
    games = db.relationship('Game')
    achievements = db.relationship('Achievement')

class Medication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    currentTime = db.Column(db.DateTime)
    medicationType = db.Column(db.Integer)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))