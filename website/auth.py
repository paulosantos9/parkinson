from flask import Blueprint, render_template, request, redirect, url_for
from .models import User, Assessment
from . import db # import from website folder
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET'])
def login():
    data = request.form
    print(data)
    return render_template('index.html')
    
@auth.route('/login', methods=['POST'])
def login_cred():
    data = request.form
    print(data)
    return render_template('index.html')

@auth.route('/logout')
def logout():
    return '<p>logout</p>'

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')

        error = None
        typeOfContainer = 0 # login
        if len(email) < 6:
            #flash('Email deve ter mais de 6 caracteres.', category='Erro')
            error = 'Email deve ter mais de 6 caracteres.'
            typeOfContainer = 1 # register
        elif len(username) < 4:
            #flash('Nome de utilizador deve ter mais de 3 caracteres.', category='erro')
            error = 'Nome de utilizador deve ter mais de 3 caracteres.'
            typeOfContainer = 1
        elif password != password_confirm:
            #flash('Palavras-passe têm de ser iguais.', category='Erro')
            error = 'Palavras-passe têm de ser iguais.'
            typeOfContainer = 1
        elif len(password) < 7:
            #flash('Palavra-passe deve ter mais de 6 caracteres.', category='Erro')
            error = 'Palavra-passe deve ter mais de 6 caracteres.'
            typeOfContainer = 1
        else:
            # add user to database
            #flash('Conta criada.', category='success')
            new_user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('views.main'))

        print(typeOfContainer)
        return render_template('index.html', error=error, typeOfContainer=typeOfContainer)