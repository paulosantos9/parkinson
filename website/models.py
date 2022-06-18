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
    sound = db.Column(db.Text)

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

class Person(db.Model, UserMixin):
    __abstract__ = True
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(270))
    name = db.Column(db.String(150))
    phoneNumber = db.Column(db.String(9))
    bornDate = db.Column(db.Date)
    gender = db.Column(db.String(1))

class Doctor(Person):
    id = db.Column(db.Integer, primary_key=True)
    patientsList = db.relationship('Patient')

class Patient(Person):
    id = db.Column(db.Integer, primary_key=True)
    patientNumber = db.Column(db.String(9))
    alzheimer = db.Column(db.Boolean)
    parkinson = db.Column(db.Boolean)
    observations = db.Column(db.String(10000))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    assessments = db.relationship('Assessment')
    games = db.relationship('Game')