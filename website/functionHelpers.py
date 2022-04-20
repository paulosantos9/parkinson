import datetime
from flask import Blueprint, request, redirect, url_for, session
from flask_login import login_user, login_required, logout_user, current_user

def checkIfUserComplete():
    if (current_user.name == '' or current_user.phoneNumber == '' or current_user.bornDate == datetime.datetime(1900, 1, 1) or  current_user.gender == '' or current_user.patientNumber == ''):
        session['page'] = 'fillUser'
    else:
        session['page'] = 'main'

def manageSession():
    error = session.get('error')
    typeOfContainer = session.get('typeOfContainer')
    if typeOfContainer:
        typeOfContainer = int(typeOfContainer)
    session.pop('error', '')
    session.pop('typeOfContainer', 0)
    return error, typeOfContainer
