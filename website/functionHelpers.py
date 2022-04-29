import datetime
from flask import session
from flask_login import current_user
from random import randint
import re
from flask import render_template, helpers



def checkIfUserComplete():
    if (current_user.name == '' or current_user.phoneNumber == '' or current_user.bornDate == datetime.datetime(1900, 1, 1) or  current_user.gender == '' or current_user.patientNumber == ''):
        session['page'] = 'settings'
        return False
    else:
        session['page'] = 'main_menu'
        return True

def manageSession():
    error = session.get('error')
    typeOfContainer = session.get('typeOfContainer')
    if typeOfContainer:
        typeOfContainer = int(typeOfContainer)
    session.pop('error', '')
    session.pop('typeOfContainer', 0)
    return error, typeOfContainer

def chooseGame(numberOfGames):
    number = randint(1,numberOfGames)
    game = '/games/game' + str(number) + '.html'
    return game

def isPasswordValid(password, password_confirm):
    minLength = 8
    if len(password) < minLength:
        return False, 'Palavra-passe deve ter ' + str(minLength) + ' ou mais caracteres.'
    elif not re.search("[a-z]", password):
        return False, 'Palavra-passe deve ter letras minúsculas.'
    elif not re.search("[A-Z]", password):
        return False, 'Palavra-passe deve ter letras maiúsculas.'
    elif not re.search("[0-9]", password):
        return False, 'Palavra-passe deve ter pelo menos um número.'
    elif not set(password).intersection("!\"#$%&()*+,-/:;<=>?@[\]^`{|}~'._"):
        return False, 'Palavra-passe deve ter pelo menos um símbolo.'
    elif re.search("\s", password):
        return False, 'Palavra-passe não pode ter espaços.'
    elif password != password_confirm:
        return False, 'Palavras-passe têm de ser iguais.'
    else:
        return True, ''

def isEmailValid(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    return re.search(regex,email)

def isUsernameValid(username):
    minLength = 4
    maxLength = 50
    if re.search("[0-9]", username[0]):
        return False, 'Nome de utilizador não pode começar por um número.'
    elif (len(username)<minLength):
        return False, 'Nome de utilizador deve ter ' + str(minLength) + ' ou mais caracteres.'
    elif (len(username)>maxLength):
        return False, 'Nome de utilizador só pode ter até ' + str(maxLength) + ' caracteres.'
    elif set(username).intersection("!\"#$%&()*+,-/:;<=>?@[\]^`{|}~'"): # keep adding characters to check which one gives errors
        return False, 'Nome de utilizador só pode conter caracteres alfanuméricos e os símbolos . e _.'
    elif re.search("\s", username):
        return False, 'Nome de utilizador não pode ter espaços.'
    else:
        return True, ''
