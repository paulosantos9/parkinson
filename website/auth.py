from flask import Blueprint, render_template, request, redirect, url_for
from .models import User, Assessment
from . import db # import from website folder
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.main'))
    else:
        if request.method == 'GET':
            error = request.args.get('error', '')
            typeOfContainer = request.args.get('typeOfContainer', '0')
            return render_template('index.html', error=error, typeOfContainer=int(typeOfContainer))
        elif request.method == 'POST':
            print('first')
            username = request.form.get('username')
            password = request.form.get('password')

            error = None
            typeOfContainer = 0

            user = User.query.filter_by(username=username).first()

            if user:
                if check_password_hash(user.password, password):
                    login_user(user, remember=True)
                    return redirect(url_for('views.main'))
                else:
                    error = 'Credenciais incorretas, tente novamente.'
            else:
                error = 'Credenciais incorretas, tente novamente.'

            return redirect(url_for('auth.login', error=error, typeOfContainer=int(typeOfContainer)))
        else:
            error = "Method invalid"
            return redirect(url_for('auth.login', error=error, typeOfContainer=int(typeOfContainer)))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    error = request.args.get('error', '')
    typeOfContainer = request.args.get('typeOfContainer', '1')

    if request.method == 'GET':
        return render_template('index.html', error=error, typeOfContainer=int(typeOfContainer))
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
            #flash('Email deve ter mais de 6 caracteres.', category='Erro')
            error = 'Email deve ter mais de 6 caracteres.'
        elif len(username) < 4:
            #flash('Nome de utilizador deve ter mais de 3 caracteres.', category='erro')
            error = 'Nome de utilizador deve ter mais de 3 caracteres.'
        elif password != password_confirm:
            #flash('Palavras-passe têm de ser iguais.', category='Erro')
            error = 'Palavras-passe têm de ser iguais.'
        elif len(password) < 7:
            #flash('Palavra-passe deve ter mais de 6 caracteres.', category='Erro')
            error = 'Palavra-passe deve ter mais de 6 caracteres.'
        else:
            # add user to database
            #flash('Conta criada.', category='success')
            new_user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            return redirect(url_for('views.main'))

        return redirect(url_for('auth.signup', error=error, typeOfContainer=int(typeOfContainer)))
    else:
        return redirect(url_for('auth.signup', error=error, typeOfContainer=int(typeOfContainer)))