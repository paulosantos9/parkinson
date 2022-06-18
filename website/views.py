from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_login import current_user
from .functionHelpers import checkIfUserComplete, manageSession, chooseGame, database_assessments
from .models import Game, Question, Assessment
from . import db # import from website folder
from random import randint

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
                session['page'] = 'main_menu'
                return render_template('login_signup.html')

            elif (current_page == 'game'):
                numberOfGames = [1, 2, 3, 4, 5, 6]
                current_game, gameType = chooseGame(numberOfGames)
                gamesList = Game.query.filter_by(patient_id=current_user.id, gameTypeIndex=gameType).all()
                typeOfRecord = {1: 'min', 2: 'max', 3: 'min', 4: '', 5: 'max', 6: ''}
                if (len(gamesList)):
                    if (typeOfRecord[gameType] == 'max'): # Quando o recorde é o máximo
                        tempRecord = 0
                        for game in gamesList:
                            if (int(game.score) > tempRecord):
                                tempRecord = int(game.score)
                    elif (typeOfRecord[gameType] == 'min'):  # Quando o recorde é o mínimo
                        tempRecord = 10000
                        for game in gamesList:
                            if (int(game.score) < tempRecord):
                                tempRecord = int(game.score)
                    else:
                        tempRecord = -1
                    typeOfActions = {1: 'milissegundos', 2: 'cliques', 3: 'tentativas', 4: '', 5: 'pontos', 6: ''}
                    record = 'Recorde: ' + str(tempRecord) + ' ' + typeOfActions[gameType]
                else:
                    record = ''

                if gameType == 4: # Imagem aleatoria para desenhar
                    randomNum = randint(0,1)
                    image = ['spiral', 'wave'][randomNum]
                    text = ['Vamos desenhar uma espiral. Tente desenhar por cima do tracejado.', 'Vamos desenhar uma onda. Tente desenhar por cima do tracejado até ao avião.'][randomNum]
                    return render_template(current_game, record=record, image=image, text=text)
                return render_template(current_game, record=record)

            elif (current_page == 'game_pc'):
                numberOfGames = [1, 2, 3, 4, 6]
                current_game, index = chooseGame(numberOfGames)
                return render_template(current_game)

            elif (current_page == 'account'):
                return render_template('account.html')

            elif (current_page == 'gamesList'):
                gamesList = Game.query.filter_by(patient_id=current_user.id).all()
                availableGames = ['Reação', 'Rapidez', 'Memória', 'Desenho', 'Equilíbrio', 'Audio']
                typeOfActions = ['milissegundos', 'cliques', 'tentativas', '', 'pontos', '']
                bestRecord = ['min', 'max', 'min', '', 'max', '']
                recordAvailableGames = []
                for i in range(len(availableGames)):
                    tempGameList = Game.query.filter_by(patient_id=current_user.id, gameTypeIndex=i+1).all()
                    tempRecord = 0
                    if (bestRecord[i] == 'max'): # Quando o recorde é o máximo
                        tempRecord = 0
                        for game in tempGameList:
                            if (int(game.score) > tempRecord):
                                tempRecord = int(game.score)
                    elif (bestRecord[i] == 'min'):  # Quando o recorde é o mínimo
                        tempRecord = 10000
                        for game in tempGameList:
                            if (int(game.score) < tempRecord):
                                tempRecord = int(game.score)
                    else:
                        tempRecord = -1
                    recordAvailableGames.append(tempRecord)
                return render_template('games_list.html', gamesList=gamesList, availableGames=availableGames, recordAvailableGames=recordAvailableGames, typeOfActions=typeOfActions)

            elif (current_page == 'assessment'):
                assessment_index = session.get('assessment')
                print(assessment_index)
                currentAssessment = database_assessments[int(assessment_index)]
                return render_template('assessment.html', assessment=currentAssessment)

            elif (current_page == 'assessmentList'):
                assessmentListBefore = Assessment.query.filter_by(patient_id=current_user.id).all()
                assessmentListAfter = []

                for assessment in assessmentListBefore:
                    questionComplete = [element for element in database_assessments if element['name'] == assessment.testType][0]
                    questions = []
                    for index, question in enumerate(questionComplete['questions']):
                        questions.append(
                            {
                                'question': question['question'],
                                'answer': question['answers'][assessment.questions[index].answer - 1]
                            }
                        )

                    assessmentListAfter.append(
                        {
                            'name': assessment.testType,
                            'time': assessment.currentTime,
                            'questions': questions
                        }
                    )

                return render_template('assessment_list.html', assessmentList=assessmentListAfter)
            
            elif (current_page == 'choose_assessment'):
                return render_template('choose_assessment.html', options=database_assessments)

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
    if request.method == 'GET': # Jogar
        session['page'] = 'game'

    else: # Guardar resultado jogo

        data_retrieved = False
        if data_retrieved == False:
            if 'audio' in request.json: # Audio
                audio = request.json['audio']
                score = 0
                gameTypeIndex = 6
                timeSpent = 0
                image = ''
                data_retrieved = True
            else:
                audio = ''

        if data_retrieved == False:
            if 'image' in request.json: # Image
                image = request.json['image']
                score = 0
                gameTypeIndex = 4
                timeSpent = request.json['timeSpent']
                data_retrieved = True
            else:
                image = ''

        if data_retrieved == False: # Rest of games
            score = request.json['score']
            gameTypeIndex = request.json['gameType']
            timeSpent = request.json['timeSpent']

        new_game = Game(patient_id=current_user.id, gameTypeIndex=gameTypeIndex, currentTime=datetime.now(), score=score, timeSpent=timeSpent, image=image, sound=audio)
        db.session.add(new_game)
        db.session.commit()
        session['page'] = 'main_menu'
    return redirect(url_for('views.home'))

@views.route('/game/pc', methods=['GET'])
def play_pc():
    session['page'] = 'game_pc'
    return redirect(url_for('views.home'))


@views.route('/account', methods=['GET'])
def account():
    session['page'] = 'account'
    return redirect(url_for('views.home'))

@views.route('/listGames', methods=['GET'])
def listGames():
    session['page'] = 'gamesList'
    return redirect(url_for('views.home'))

@views.route('/assessment', methods=['GET', 'POST'])
def assessment():
    if request.method == 'GET': # Fazer teste
        assessment_index = request.args.get('index')
        session['assessment'] = assessment_index
        session['page'] = 'assessment'
        return redirect(url_for('views.home'))

    else: # Adicionar teste
        assessmentType = request.json['type']
        answers = request.json['answers']

        new_assessment = Assessment(testType=assessmentType, patient_id=current_user.id, currentTime=datetime.now())
        db.session.add(new_assessment)
        db.session.commit() # to be able to get the assessment id for the questions
        
        for index, answer in enumerate(answers):
            new_answer = Question(indexInAssessment=index, question=index, answer=answer, assessment_id=new_assessment.id)
            db.session.add(new_answer)   
        db.session.commit()

        session['page'] = 'main_menu'
        return redirect(url_for('views.home'))

@views.route('/choose_assessment', methods=['GET'])
def choose_assessment():
    session['page'] = 'choose_assessment'
    return redirect(url_for('views.home'))

@views.route('/assessments', methods=['GET']) # Ver lista de testes
def assessments():
    session['page'] = 'assessmentList'
    return redirect(url_for('views.home'))

@views.route('/settings', methods=['GET']) # Preencher dados da conta
def settings():
    session['page'] = 'settings'
    return redirect(url_for('views.home'))

@views.route('/backToMain', methods=['GET']) # Voltar ao menu inicial
def backToMain():
    session['page'] = 'main_menu'
    return redirect(url_for('views.home'))
    