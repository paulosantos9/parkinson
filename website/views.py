from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, session, helpers
from flask_login import login_required, current_user
from .functionHelpers import checkIfUserComplete, manageSession, chooseGame
from .models import Game, Question, Assessment
from . import db # import from website folder

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    current_page = session.get('page')
    if current_user.is_authenticated:
        if (current_page == 'main_menu'):
            return render_template('main_menu.html')

        elif (current_page == 'settings'):
            return render_template('settings.html', patient_id=current_user.id, patient_username=current_user.username,
            patient_email=current_user.email, patient_name=current_user.name, patient_phoneNumber=current_user.phoneNumber,
            patient_bornDate=current_user.bornDate, patient_gender=current_user.gender, patient_patientNumber=current_user.patientNumber,
            patient_alzheimer=current_user.alzheimer, patient_parkinson=current_user.parkinson, patient_observations=current_user.observations,
            patient_doctor_id=current_user.doctor_id, patient_assessments=current_user.assessments, patient_games=current_user.games)
        
        elif (current_page == 'login_signup'):
            return render_template('login_signup.html')

        elif (current_page == 'game'):
            if (session.get('current_game') == 0 or session.get('current_game') == None):
                numberOfGames = 2
                current_game = chooseGame(numberOfGames)
                session['current_game'] = current_game
            else:
                current_game = session.get('current_game')
            return render_template(current_game)
        
        elif (current_page == 'account'):
            return render_template('account.html')

        elif (current_page == 'games_list'):
            gamesList = Assessment.query.filter_by(patient_id=current_user.id).all()
            return render_template('games_list.html', games=gamesList)

        elif (current_page == 'assessment'):
            return render_template('assessment.html') # TO DO

        elif (current_page == 'assessmentList'):
            assessmentList = Assessment.query.filter_by(patient_id=current_user.id).all()
            return render_template('assessment_list.html', assessmentList=assessmentList)

        else:
            error, typeOfContainer = manageSession()
            return render_template('login_signup.html', error=error, typeOfContainer=typeOfContainer)
    else:
        error, typeOfContainer = manageSession()
        return render_template('login_signup.html', error=error, typeOfContainer=typeOfContainer)


@views.route('/game', methods=['GET', 'POST'])
def play():
    if request.method == 'GET':
        session['page'] = 'game'
    else:
        score = request.json['score'] # because its type application/json
        gameTypeIndex = request.json['gameType']
        new_game = Game(patient_id=current_user.id, gameTypeIndex=gameTypeIndex, currentTime=datetime.now(), score=score)
        db.session.add(new_game)
        db.session.commit()
        session['page'] = 'main_menu'

    return redirect(url_for('views.home'))

@views.route('/account', methods=['GET'])
def account():
    session['page'] = 'account'
    return redirect(url_for('views.home'))

@views.route('/listGames', methods=['GET'])
def listGames():
    session['page'] = 'games_list'
    return redirect(url_for('views.home'))

@views.route('/assessment', methods=['GET', 'POST'])
def assessment():
    if request.method == 'GET':
        session['page'] = 'assessment'
        return redirect(url_for('views.home'))
    else:
        firstAnswer = request.form.get('first-answer')
        secondAnswer = request.form.get('second-answer')
        thirdAnswer = request.form.get('third-answer')
        forthAnswer = request.form.get('forth-answer')
        fifthAnswer = request.form.get('fifth-answer')
        sixthAnswer = request.form.get('sixth-answer')
        new_assessment = Assessment(testType='UPDRS', patient_id=current_user.id, currentTime=datetime.now())
        db.session.add(new_assessment)
        db.session.commit() # to be able to get the assessment id
        first_answer = Question(indexInAssessment=0, question='', answer=firstAnswer, assessment_id=new_assessment.id)
        db.session.add(first_answer)
        second_answer = Question(indexInAssessment=1, question='', answer=secondAnswer, assessment_id=new_assessment.id)
        db.session.add(second_answer)
        third_answer = Question(indexInAssessment=2, question='', answer=thirdAnswer, assessment_id=new_assessment.id)
        db.session.add(third_answer)
        forth_answer = Question(indexInAssessment=0, question='', answer=forthAnswer, assessment_id=new_assessment.id)
        db.session.add(forth_answer)
        fifth_answer = Question(indexInAssessment=0, question='', answer=fifthAnswer, assessment_id=new_assessment.id)
        db.session.add(fifth_answer)
        sixth_answer = Question(indexInAssessment=0, question='', answer=sixthAnswer, assessment_id=new_assessment.id)
        db.session.add(sixth_answer)
        db.session.commit()
        session['page'] = 'main_menu'
        return redirect(url_for('views.home'))

@views.route('/assessments', methods=['GET'])
def assessments():
    session['page'] = 'assessmentList'
    return redirect(url_for('views.home'))

@views.route('/settings', methods=['GET'])
def settings():
    session['page'] = 'settings'
    return redirect(url_for('views.home'))

@views.route('/backToMain', methods=['GET'])
def backToMain():
    session['page'] = 'main_menu'
    session['current_game'] = 0 # reset ao jogo escolhido
    return redirect(url_for('views.home'))