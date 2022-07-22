from asyncio.windows_events import NULL
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, send_from_directory
from flask_login import current_user
from .functionHelpers import *
from .models import Game, Question, Assessment, Achievement
from . import db # import from website folder
from random import randint
from datetime import datetime

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    current_page = session.get('page')
    if current_user.is_authenticated:
        session['page'] = current_page
        if (current_page == 'main_menu'):
            return render_template('main_menu.html')

        elif (current_page == 'game'):
            numberOfGames = [1, 2, 3, 4, 5, 6]
            current_game, gameType = chooseGame(numberOfGames)
            gamesList = Game.query.filter_by(patient_id=current_user.id, gameTypeIndex=gameType).all()
            typeOfRecord = {1: 'min', 2: 'max', 3: 'min', 4: 'max', 5: 'max', 6: ''}
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
                typeOfActions = {1: 'milissegundos', 2: 'cliques', 3: 'tentativas', 4: '%', 5: 'pontos', 6: ''}
                record = 'Recorde: ' + str(tempRecord) + ' ' + typeOfActions[gameType]
            else:
                record = ''

            if gameType == 4: # Imagem aleatoria para desenhar
                randomNum = randint(0,2)
                image = ['spiral', 'wave', 'clock'][randomNum]
                game = ['Espiral', 'Onda', 'Relógio'][randomNum]
                text = ['Vamos desenhar uma espiral. Tente desenhar por cima do tracejado.', 'Vamos desenhar uma onda. Tente desenhar por cima do tracejado até ao avião.', 'Ainda se lembra como se desenha um relógio? Desenhe um relógio analógico às 11 horas e 10 minutos.'][randomNum]
                return render_template(current_game, record=record, image=image, text=text, game=game)

            return render_template(current_game, record=record)

        elif (current_page == 'game_pc'):
            numberOfGames = [1, 2, 3, 4, 6]
            current_game, gameType = chooseGame(numberOfGames)
            gamesList = Game.query.filter_by(patient_id=current_user.id, gameTypeIndex=gameType).all()
            typeOfRecord = {1: 'min', 2: 'max', 3: 'min', 4: 'max', 5: 'max', 6: ''}
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
                typeOfActions = {1: 'milissegundos', 2: 'cliques', 3: 'tentativas', 4: '%', 5: 'pontos', 6: ''}
                record = 'Recorde: ' + str(tempRecord) + ' ' + typeOfActions[gameType]
            else:
                record = ''

            if gameType == 4: # Imagem aleatoria para desenhar
                randomNum = randint(0,2)
                image = ['spiral', 'wave', 'clock'][randomNum]
                game = ['Espiral', 'Onda', 'Relógio'][randomNum]
                text = ['Vamos desenhar uma espiral. Tente desenhar por cima do tracejado.', 'Vamos desenhar uma onda. Tente desenhar por cima do tracejado até ao avião.', 'Ainda se lembra como se desenha um relógio? Desenhe um relógio analógico às 11 horas e 10 minutos.'][randomNum]
                return render_template('/games/game' + str(gameType) + '.html', record=record, image=image, text=text, game=game)

            return render_template(current_game, record=record)

        elif (current_page == 'info_choose'):
            return render_template('info_choose.html', options=database_diseases)

        elif (current_page == 'info'):
            info_index = session.get('info')
            current_info = database_diseases[int(info_index)]
            return render_template('info.html', current_info=current_info)

        elif (current_page == 'account'):
            return render_template('account.html')

        elif (current_page == 'gamesList'):
            gamesList = Game.query.filter_by(patient_id=current_user.id).all()
            recordAvailableGames = []
            for i in range(len(database_games)):
                tempGameList = Game.query.filter_by(patient_id=current_user.id, gameTypeIndex=i+1).all()
                tempRecord = 0
                if (database_games[i]['bestRecord'] == 'max'): # Quando o recorde é o máximo
                    tempRecord = 0
                    for game in tempGameList:
                        if (int(game.score) > tempRecord):
                            tempRecord = int(game.score)
                elif (database_games[i]['bestRecord'] == 'min'):  # Quando o recorde é o mínimo
                    tempRecord = 10000
                    for game in tempGameList:
                        if (int(game.score) < tempRecord):
                            tempRecord = int(game.score)
                else:
                    tempRecord = -1
                recordAvailableGames.append(tempRecord)
            return render_template('graph.html')
            #return render_template('graph.html', gamesList=gamesList, availableGames=availableGames, recordAvailableGames=recordAvailableGames, typeOfActions=typeOfActions)

        elif (current_page == 'assessment'):
            assessment_index = session.get('assessment')
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

        elif (current_page == 'achievements'):
            achivements = Achievement.query.filter_by(patient_id=current_user.id).all()
            return render_template('achievements.html', database_achievements=achivements)
        
        elif (current_page == 'choose_evolution'):
            return render_template('choose_evolution.html', options=database_games)

        elif (current_page == 'evolution'):
            return render_template('graph.html', index=session.get('evolution'))

        elif (current_page == 'choose_assessment'):
            return render_template('choose_assessment.html', options=database_assessments)

        else:
            return render_template('main_menu.html')

    else:
        error, typeOfContainer = manageSession()
        username = session['username']
        session['username'] = ''
        email = session['email']
        session['email'] = ''
        return render_template('login_signup.html', error=error, typeOfContainer=typeOfContainer, username=username, email=email)


@views.route('/game', methods=['GET', 'POST'])
def play():
    if request.method == 'GET': # Jogar
        session['page'] = 'game'

    else: # Guardar resultado jogo
        data_retrieved = False
        if data_retrieved == False and 'audio_data' in request.files: # Audio

            file = request.files['audio_data']
            
            filename = saveAudioFile(file)

            jitter, shimmer = calculateAudioParameters(filename)

            gameTypeIndex = 6
            data_retrieved = True

            new_game = Game(patient_id=current_user.id, gameTypeIndex=gameTypeIndex, currentTime=datetime.now(), audioPath=filename, jitter=jitter, shimmer=shimmer)

        if data_retrieved == False and 'image' in request.json: # Image

            image = request.json['image']
            gameTypeIndex = 4
            timeSpent = request.json['timeSpent']
            imageType = request.json['imageType']
            reference_image = ['spiral', 'wave', 'clock'][['Espiral', 'Onda', 'Relógio'].index(imageType)]

            score = calculate_image_accuracy(image, reference_image) # calculate

            data_retrieved = True

            new_game = Game(patient_id=current_user.id, gameTypeIndex=gameTypeIndex, currentTime=datetime.now(), score=score, timeSpent=timeSpent, image=image)

        if data_retrieved == False: # Rest of games

            score = request.json['score']
            gameTypeIndex = request.json['gameType']
            timeSpent = request.json['timeSpent']

            new_game = Game(patient_id=current_user.id, gameTypeIndex=gameTypeIndex, currentTime=datetime.now(), score=score, timeSpent=timeSpent)


        # Add game
        db.session.add(new_game)

        # Add achievement
        check_game_achievements(gameTypeIndex)

        db.session.commit()
        session['page'] = 'main_menu'

    return redirect(url_for('views.home'))

@views.route('/game/pc', methods=['GET'])
def play_pc():
    session['page'] = 'game_pc'
    return redirect(url_for('views.home'))

@views.route('/info', methods=['GET'])
def info():
    if request.method == 'GET':
        info_index = request.args.get('index')
        session['info'] = info_index
        session['page'] = 'info'
        return redirect(url_for('views.home'))

@views.route('/info_choose', methods=['GET'])
def info_choose():
    session['page'] = 'info_choose'
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
    if request.method == 'GET': # Fazer questionário
        assessment_index = request.args.get('index')
        session['assessment'] = assessment_index
        session['page'] = 'assessment'
        return redirect(url_for('views.home'))

    else: # Adicionar questionário
        assessmentType = request.json['type']
        answers = request.json['answers']

        new_assessment = Assessment(testType=assessmentType, patient_id=current_user.id, currentTime=datetime.now())
        db.session.add(new_assessment)
        db.session.commit() # to be able to get the assessment id for the questions

        for index, answer in enumerate(answers):
            new_answer = Question(indexInAssessment=index, question=index, answer=answer, assessment_id=new_assessment.id)
            db.session.add(new_answer)

        check_test_achievements(assessmentType)

        db.session.commit()

        session['page'] = 'main_menu'
        return redirect(url_for('views.home'))

@views.route('/choose_assessment', methods=['GET'])
def choose_assessment():
    session['page'] = 'choose_assessment'
    return redirect(url_for('views.home'))

@views.route('/assessments', methods=['GET']) # Ver lista de questionários
def assessments():
    session['page'] = 'assessmentList'
    return redirect(url_for('views.home'))

@views.route('/achievements', methods=['GET']) # Ver lista de conquistas
def achievements():
    session['page'] = 'achievements'
    return redirect(url_for('views.home'))

@views.route('/backToMain', methods=['GET']) # Voltar ao menu inicial
def backToMain():
    session['page'] = 'main_menu'
    return redirect(url_for('views.home'))

@views.route('/choose_evolution', methods=['GET']) # pick evolution
def choose_evolution():
    session['page'] = 'choose_evolution'
    return redirect(url_for('views.home'))

@views.route('/evolution/<int:index>', methods=['GET']) # show evolution
def evolution(index):
    session['page'] = 'evolution'
    session['evolution'] = index
    return redirect(url_for('views.home'))

@views.route('/games_data/<int:index>', methods=['GET']) # Get games data for graph
def games_data(index):
    games_list = [serialize_game(x) for x in Game.query.filter_by(patient_id=current_user.id, gameTypeIndex=index).all()]
    return jsonify({'games_list': games_list, 'unit': database_games[index-1]['action'], 'type': database_games[index-1]['name']})

def serialize_game(game):
    if (game.gameTypeIndex != 6):
        return {
            'gameTypeIndex': game.gameTypeIndex,
            'currentTime': game.currentTime,
            'score': game.score,
            'timeSpent': game.timeSpent,
        }
    else:
        return {
            'gameTypeIndex': game.gameTypeIndex,
            'currentTime': game.currentTime,
            'jitter': game.jitter,
            'shimmer': game.shimmer,
        }

@views.route("/<path:path>")
def get_files(path):
    if path == 'manifest.json' or path == 'icons/icon-192x192.png' or path == 'icons/icon-512x512.png' or path == 'sw.js':
        return send_from_directory('static', 'PWA/'+path)
    else:
        return render_template('error_page.html'), 404
