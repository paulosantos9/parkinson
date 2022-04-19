from flask import Blueprint, render_template, request, redirect, url_for, session, helpers
from flask_login import login_required, current_user
from .functionHelpers import checkIfUserComplete, manageSession

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        if (session.get('page') == 'main'):
            response = helpers.make_response(render_template('main.html'))
            response.set_cookie('patient_id', str(current_user.id))
            response.set_cookie('patient_username', current_user.username if isinstance(current_user.username, str) == True else str(current_user.username))
            response.set_cookie('patient_email', current_user.email if isinstance(current_user.email, str) == True else str(current_user.email))
            response.set_cookie('patient_name', current_user.name if isinstance(current_user.name, str) == True else str(current_user.name))
            response.set_cookie('patient_phoneNumber', current_user.phoneNumber if isinstance(current_user.phoneNumber, str) == True else str(current_user.phoneNumber))
            response.set_cookie('patient_bornDate', current_user.bornDate if isinstance(current_user.bornDate, str) == True else str(current_user.bornDate))
            response.set_cookie('patient_gender', current_user.gender if isinstance(current_user.gender, str) == True else str(current_user.gender))
            response.set_cookie('patient_patientNumber', current_user.patientNumber if isinstance(current_user.patientNumber, str) == True else str(current_user.patientNumber))
            response.set_cookie('patient_alzheimer', current_user.alzheimer if isinstance(current_user.alzheimer, str) == True else str(current_user.alzheimer))
            response.set_cookie('patient_parkinson', current_user.parkinson if isinstance(current_user.parkinson, str) == True else str(current_user.parkinson))
            response.set_cookie('patient_observations', current_user.observations if isinstance(current_user.observations, str) == True else str(current_user.observations))
            response.set_cookie('patient_doctor_id', current_user.doctor_id if isinstance(current_user.doctor_id, str) == True else str(current_user.doctor_id))
            '''response.set_cookie('patient_assessments', str(current_user.assessments))
            response.set_cookie('patient_games', str(current_user.games))'''
            return '<h1>User complete</h1>'
        elif (session.get('page') == 'completeUser'):
            response = helpers.make_response(render_template('main.html'))
            response.set_cookie('patient_id', str(current_user.id))
            response.set_cookie('patient_username', current_user.username if isinstance(current_user.username, str) == True else str(current_user.username))
            response.set_cookie('patient_email', current_user.email if isinstance(current_user.email, str) == True else str(current_user.email))
            response.set_cookie('patient_name', current_user.name if isinstance(current_user.name, str) == True else str(current_user.name))
            response.set_cookie('patient_phoneNumber', current_user.phoneNumber if isinstance(current_user.phoneNumber, str) == True else str(current_user.phoneNumber))
            response.set_cookie('patient_bornDate', current_user.bornDate if isinstance(current_user.bornDate, str) == True else str(current_user.bornDate))
            response.set_cookie('patient_gender', current_user.gender if isinstance(current_user.gender, str) == True else str(current_user.gender))
            response.set_cookie('patient_patientNumber', current_user.patientNumber if isinstance(current_user.patientNumber, str) == True else str(current_user.patientNumber))
            response.set_cookie('patient_alzheimer', current_user.alzheimer if isinstance(current_user.alzheimer, str) == True else str(current_user.alzheimer))
            response.set_cookie('patient_parkinson', current_user.parkinson if isinstance(current_user.parkinson, str) == True else str(current_user.parkinson))
            response.set_cookie('patient_observations', current_user.observations if isinstance(current_user.observations, str) == True else str(current_user.observations))
            response.set_cookie('patient_doctor_id', current_user.doctor_id if isinstance(current_user.doctor_id, str) == True else str(current_user.doctor_id))
            '''response.set_cookie('patient_assessments', str(current_user.assessments))
            response.set_cookie('patient_games', str(current_user.games))'''
            return response
        elif (session.get('page') == 'login-signup'):
            return render_template('index.html')
        else:
            error, typeOfContainer = manageSession()
            return render_template('index.html', error=error, typeOfContainer=typeOfContainer)
    else:
        if (session.get('page') == 'main'):
            error, typeOfContainer = manageSession()
            return render_template('index.html', error=error, typeOfContainer=typeOfContainer)
        elif (session.get('page') == 'login-signup'):
            error, typeOfContainer = manageSession()
            return render_template('index.html', error=error, typeOfContainer=typeOfContainer)
        elif (session.get('page') == 'completeUser'):
            error, typeOfContainer = manageSession()
            return render_template('index.html', error=error, typeOfContainer=typeOfContainer)
        else:
            error, typeOfContainer = manageSession()
            return render_template('index.html', error=error, typeOfContainer=typeOfContainer)