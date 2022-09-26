import datetime
from flask import Blueprint, request, redirect, url_for, session, render_template
from .models import Patient, Achievement
from .functionHelpers import database_achievements
from . import db # import from website folder
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .functionHelpers import isUsernameValid, manageSession, isPasswordValid, isEmailValid

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        session['page'] = 'login_signup'
        return redirect(url_for('views.home'))
    else:
        if request.method == 'GET': # by url, should not be available so redirect
            error, typeOfContainer = manageSession()
            
            return redirect(url_for('views.home', error=error, typeOfContainer=typeOfContainer))
        
        elif request.method == 'POST': # by url form
            username_email = request.form.get('usernameemail')
            password = request.form.get('password')

            error = None
            typeOfContainer = 0

            user_by_username = Patient.query.filter_by(username=username_email).first()
            user_by_email = Patient.query.filter_by(email=username_email).first()

            # TRY TO LOGIN WITH USERNAME
            if user_by_username:
                if check_password_hash(user_by_username.password, password):
                    login_user(user_by_username, remember=True)
                    return redirect(url_for('views.home'))
                else:
                    error = 'Credenciais incorretas, tente novamente.'
                    
            else:
                error = 'Credenciais incorretas, tente novamente.'
            
            # IF NOT LOGIN WITH USERNAME, TRY TO LOGIN WITH EMAIL
            if user_by_email:
                if check_password_hash(user_by_email.password, password):
                    login_user(user_by_email, remember=True)
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
            
            db.session.commit()

            return redirect(url_for('views.home'))
        else:
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
                new_user = Patient(email=email, username=username, password=generate_password_hash(password, method='sha256'))
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)

                # create achievements
                for achivement_item in database_achievements:
                    achievement = Achievement(name=achivement_item['name'], locked=True, patient_id=current_user.id, icon=achivement_item['icon'], description=achivement_item['description'])
                    db.session.add(achievement)
                db.session.commit()
                session['page'] = 'main_menu'
                
            session['error'] = error
            session['typeOfContainer'] = typeOfContainer
            session['username'] = username
            session['email'] = email

            return redirect(url_for('views.home'))
        else:
            session['error'] = error
            session['typeOfContainer'] = typeOfContainer
            return redirect(url_for('views.home'))

def checkUserLogin():
    if not current_user.is_authenticated:
        error, typeOfContainer = manageSession()
        try:
            username = session['username']
            session['username'] = ''
        except:
            username = ''
        try:
            email = session['email']
            session['email'] = ''
        except:
            email = ''
        return False, email, username, error, typeOfContainer
    else:
        return True, '', ''
