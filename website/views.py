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
        if checkIfUserComplete():
            session['page'] = current_page
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
                numberOfGames = 3
                current_game = chooseGame(numberOfGames)
                return render_template(current_game)

            elif (current_page == 'account'):
                return render_template('account.html')

            elif (current_page == 'games_list'):
                gamesList = Game.query.filter_by(patient_id=current_user.id, ).all()
                availableGames = ['Reação', 'Rapidez', 'Memória']
                typeOfActions = ['milissegundos', 'cliques', 'tentativas']
                recordAvailableGames = []
                for i in range(len(availableGames)):
                    tempGameList = Game.query.filter_by(patient_id=current_user.id, gameTypeIndex=i+1).all()
                    tempRecord = 0
                    if (i == 0):
                        # Tempo reação
                        tempRecord = 10000
                        for game in tempGameList:
                            if (int(game.score) < tempRecord):
                                tempRecord = int(game.score)
                    elif (i == 1):
                        # Nº cliques
                        tempRecord = 0
                        for game in tempGameList:
                            if (int(game.score) > tempRecord):
                                tempRecord = int(game.score)
                    elif (i == 2):
                        # Memória
                        tempRecord = 10000
                        for game in tempGameList:
                            if (int(game.score) < tempRecord):
                                tempRecord = int(game.score)
                    recordAvailableGames.append(tempRecord)
                return render_template('games_list.html', gamesList=gamesList, availableGames=availableGames, recordAvailableGames=recordAvailableGames, typeOfActions=typeOfActions)

            elif (current_page == 'assessment'):
                return render_template('assessment.html') # TO DO

            elif (current_page == 'assessmentList'):
                assessmentList = Assessment.query.filter_by(patient_id=current_user.id).all()
                return render_template('assessment_list.html', assessmentList=assessmentList)

            else:
                error, typeOfContainer = manageSession()
                return render_template('login_signup.html', error=error, typeOfContainer=typeOfContainer)
        else:
            return render_template('settings.html', patient_id=current_user.id, patient_username=current_user.username,
            patient_email=current_user.email, patient_name=current_user.name, patient_phoneNumber=current_user.phoneNumber,
            patient_bornDate=current_user.bornDate, patient_gender=current_user.gender, patient_patientNumber=current_user.patientNumber,
            patient_alzheimer=current_user.alzheimer, patient_parkinson=current_user.parkinson, patient_observations=current_user.observations,
            patient_doctor_id=current_user.doctor_id, patient_assessments=current_user.assessments, patient_games=current_user.games)

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
        firstQuestion = 'Durante a última semana teve dificuldades em lembrar-se de coisas, seguir conversas, prestar atenção, pensar claramente ou encontrar os caminhos em casa ou na cidade?'
        firstAnswer = request.json['first-answer']
        secondQuestion = 'Durante a última semana viu, cheirou, ouviu ou sentiu coisas que não estavam mesmo no local?'
        secondAnswer = request.json['second-answer']
        thirdQuestion = 'Durante a última semana sentiu-se me baixo, triste, sem esperança ou incapaz de desfrutar das coisas? Se sim, este sentimento demorou mais de um dia seguido? Tornou dificil continuar com as atividades habituais ou estar com pessoas?'
        thirdAnswer = request.json['third-answer']
        forthQuestion = 'Durante a última semana sentiu-se nervoso, preocupado ou tenso? Se sim, este sentimento demorou mais do que um dia seguido? Tornou dificil continuar com as atividades habituais ou estar com pessoas?'
        forthAnswer = request.json['forth-answer']
        fifthQuestion = 'Durante a última semana sentiu-se indiferente ao fazer atividades ou estar com outras pessoas?'
        fifthAnswer = request.json['fifth-answer']
        sixthQuestion = 'Durante a última semana sentiu impulsos difíceis de controlar, como por exemplo apostar, usar o computador ou tomar mais comprimidos? Sente-se levado a fazer ou a pensar em algo, e a ser dificil de parar?'
        sixthAnswer = request.json['sixth-answer']
        new_assessment = Assessment(testType='UPDRS', patient_id=current_user.id, currentTime=datetime.now())
        db.session.add(new_assessment)
        db.session.commit() # to be able to get the assessment id
        first_answer = Question(indexInAssessment=0, question=firstQuestion, answer=firstAnswer, assessment_id=new_assessment.id)
        db.session.add(first_answer)
        second_answer = Question(indexInAssessment=1, question=secondQuestion, answer=secondAnswer, assessment_id=new_assessment.id)
        db.session.add(second_answer)
        third_answer = Question(indexInAssessment=2, question=thirdQuestion, answer=thirdAnswer, assessment_id=new_assessment.id)
        db.session.add(third_answer)
        forth_answer = Question(indexInAssessment=0, question=forthQuestion, answer=forthAnswer, assessment_id=new_assessment.id)
        db.session.add(forth_answer)
        fifth_answer = Question(indexInAssessment=0, question=fifthQuestion, answer=fifthAnswer, assessment_id=new_assessment.id)
        db.session.add(fifth_answer)
        sixth_answer = Question(indexInAssessment=0, question=sixthQuestion, answer=sixthAnswer, assessment_id=new_assessment.id)
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
    return redirect(url_for('views.home'))
    