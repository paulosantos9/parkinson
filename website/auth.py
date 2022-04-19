import datetime
from flask import Blueprint, request, redirect, url_for, session
from .models import Game, Assessment, Doctor, Patient
from . import db # import from website folder
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    else:
        if request.method == 'GET':
            error = session.get('error')
            typeOfContainer = session.get('typeOfContainer')
            if typeOfContainer:
                typeOfContainer = int(typeOfContainer)
            session.pop('error', '')
            session.pop('typeOfContainer', 0)
            
            return redirect(url_for('views.home', error=error, typeOfContainer=typeOfContainer))
        elif request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            error = None
            typeOfContainer = 0

            user = Patient.query.filter_by(username=username).first()

            if user:
                if check_password_hash(user.password, password):
                    login_user(user, remember=True)
                    if current_user.is_authenticated:
                        return redirect(url_for('views.home'))
                    else:
                        error = session.get('error')
                        typeOfContainer = session.get('typeOfContainer')
                        if typeOfContainer:
                            typeOfContainer = int(typeOfContainer)
                        session.pop('error', '')
                        session.pop('typeOfContainer', 0)
                        return redirect(url_for('views.home'))
                else:
                    error = 'Credenciais incorretas, tente novamente.'
            else:
                error = 'Credenciais incorretas, tente novamente.'
            
            session['error'] = error
            session['typeOfContainer'] = typeOfContainer
            return redirect(url_for('views.home'))
        else:
            error = "Method invalid"
            session['error'] = error
            session['typeOfContainer'] = typeOfContainer
            return redirect(url_for('views.home'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('patient')
    return redirect(url_for('views.home'))

@auth.route('/update', methods=['POST'])
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
            current_user.alzheimer = request.form.get('alzheimerOption') == '1'
            current_user.parkinson = request.form.get('parkinsonOption') == '1'
            
            db.session.commit()

            return redirect(url_for('views.home'))
        else:
            return redirect(url_for('views.home'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    else:
        error = session.get('error')
        typeOfContainer = session.get('typeOfContainer')
        if typeOfContainer:
            typeOfContainer = int(typeOfContainer)
        session.pop('error', '')
        session.pop('typeOfContainer', 0)
    
        if request.method == 'GET':
            session['error'] = error
            session['typeOfContainer'] = typeOfContainer
            return redirect(url_for('views.home'))
        elif request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            print(email)
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
            elif len(email) < 6:
                error = 'Email deve ter mais de 6 caracteres.'
            elif len(username) < 4:
                error = 'Nome de utilizador deve ter mais de 3 caracteres.'
            elif password != password_confirm:
                error = 'Palavras-passe têm de ser iguais.'
            elif len(password) < 7:
                error = 'Palavra-passe deve ter mais de 6 caracteres.'
            else:
                # add user to database
                print(email)
                new_user = Patient(email=email, username=username, password=generate_password_hash(password, method='sha256'), name='', phoneNumber='', bornDate=datetime.datetime(1900, 1, 1), gender='', patientNumber='', alzheimer=False, parkinson=False, observations='', doctor_id=-1)
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                if current_user.is_authenticated:
                    return redirect(url_for('views.home'))
                else:
                    session['error'] = error
                    session['typeOfContainer'] = typeOfContainer
                    return redirect(url_for('views.home'))
            session['error'] = error
            session['typeOfContainer'] = typeOfContainer
            return redirect(url_for('views.home'))
        else:
            session['error'] = error
            session['typeOfContainer'] = typeOfContainer
            return redirect(url_for('views.home'))