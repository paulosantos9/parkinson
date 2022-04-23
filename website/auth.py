import datetime
from flask import Blueprint, request, redirect, url_for, session
from .models import Game, Assessment, Doctor, Patient
from . import db # import from website folder
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .functionHelpers import checkIfUserComplete, isUsernameValid, manageSession, isPasswordValid, isEmailValid

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    session['page'] = 'login_signup'
    if current_user.is_authenticated:
        checkIfUserComplete()
        return redirect(url_for('views.home'))
    else:
        if request.method == 'GET': # by url, should not be available so redirect
            error, typeOfContainer = manageSession()
            
            return redirect(url_for('views.home', error=error, typeOfContainer=typeOfContainer))
        
        elif request.method == 'POST': # by url form
            username = request.form.get('username')
            password = request.form.get('password')

            error = None
            typeOfContainer = 0

            user = Patient.query.filter_by(username=username).first()

            if user:
                if check_password_hash(user.password, password):
                    login_user(user, remember=True)
                    checkIfUserComplete()
                    return redirect(url_for('views.home'))
                else:
                    error = 'Credenciais incorretas, tente novamente.'
            else:
                error = 'Credenciais incorretas, tente novamente.'
            
            session['error'] = error
            session['typeOfContainer'] = typeOfContainer

            return redirect(url_for('views.home'))

        else: # method other tham GET or POST
            error = "Method invalid"
            session['error'] = error
            session['typeOfContainer'] = typeOfContainer

            return redirect(url_for('views.home'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    session['page'] = 'login_signup'
    return redirect(url_for('views.home'))

@auth.route('/update', methods=['GET', 'POST'])
def update():
    if current_user.is_authenticated:
        if request.method == 'POST':
            # need to perform check before updating to check if every field is well filled
            current_user.username = request.form.get('username')
            current_user.email = request.form.get('email')
            current_user.name = request.form.get('name')
            current_user.phoneNumber = request.form.get('phoneNumber')
            bornDate = request.form.get('bornDate')
            year = int(bornDate[0:4])
            month = int(bornDate[5:7])
            day = int(bornDate[8:20])
            current_user.bornDate = datetime.datetime(year, month, day)
            current_user.gender = request.form.get('genderOption')
            current_user.patientNumber = request.form.get('patientNumber')
            current_user.alzheimer = request.form.get('alzheimerOption') == '1' # passing to True or False
            current_user.parkinson = request.form.get('parkinsonOption') == '1'
            
            db.session.commit()

            checkIfUserComplete()

            return redirect(url_for('views.home'))
        else:
            checkIfUserComplete()
            return redirect(url_for('views.home'))
    else:
        session['page'] = 'login_signup'
        
        return redirect(url_for('views.home'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    session['page'] = 'login_signup'
    
    if current_user.is_authenticated:
        session['page'] = 'main_menu'

        return redirect(url_for('views.home'))
    else:
        error, typeOfContainer = manageSession()
   
        if request.method == 'GET':
            session['error'] = error
            session['typeOfContainer'] = typeOfContainer
            return redirect(url_for('views.home'))
        elif request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')

            password = request.form.get('password')
            password_confirm = request.form.get('password_confirm')

            emailAlreadyUsed = True if Patient.query.filter_by(email=email).first() else False
            usernameAlreadyUsed = True if Patient.query.filter_by(username=username).first() else False

            error = None
            typeOfContainer = 1 # 1 - register, 0 - login

            if emailAlreadyUsed:
                error = 'Este email já se encontra em utilização.'
            elif usernameAlreadyUsed:
                error = 'Este nome de utilizador já se encontra em utilização.'
            elif isUsernameValid(username)[0] == False:
                error = isUsernameValid(username)[1]
            elif isEmailValid(email) == False:
                error = 'Email inválido.'
            elif isPasswordValid(password, password_confirm)[0] == False:
                error = isPasswordValid(password, password_confirm)[1]
            else:
                # add user to database
                new_user = Patient(email=email, username=username, password=generate_password_hash(password, method='sha256'), name='', phoneNumber='', bornDate=datetime.datetime(1900, 1, 1), gender='', patientNumber='', alzheimer=False, parkinson=False, observations='', doctor_id=-1)
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)

                session['page'] = 'settings'
                
            session['error'] = error
            session['typeOfContainer'] = typeOfContainer

            return redirect(url_for('views.home'))
        else:
            session['error'] = error
            session['typeOfContainer'] = typeOfContainer
            return redirect(url_for('views.home'))