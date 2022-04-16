from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        return render_template('main.html')
    else:
        error = session.get('error')
        typeOfContainer = session.get('typeOfContainer')
        if typeOfContainer:
            typeOfContainer = int(typeOfContainer)
        session.pop('error', '')
        session.pop('typeOfContainer', 0)
        return render_template('index.html', error=error, typeOfContainer=typeOfContainer)