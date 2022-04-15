from flask import Blueprint, request, redirect, url_for, session
from .models import User, Assessment
from . import db # import from website folder
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    session['error'] = ''
    session['typeOfContainer'] = 0
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

            user = User.query.filter_by(username=username).first()

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
    if typeOfContainer:
        typeOfContainer = int(typeOfContainer)
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
            password = request.form.get('password')
            password_confirm = request.form.get('password_confirm')

            emailAlreadyUsed = True if User.query.filter_by(email=email).first() else False
            usernameAlreadyUsed = True if User.query.filter_by(username=username).first() else False

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
                new_user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'))
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