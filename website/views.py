from flask import Blueprint, render_template, request, jsonify, send_from_directory
from flask_login import current_user
from .functionHelpers import *
from .models import Game, Medication, Question, Assessment, Achievement
from . import db # import from website folder
from random import randint
from datetime import datetime as dt
import datetime
from .auth import checkUserLogin

views = Blueprint('views', __name__)

# MAIN MENU
@views.route('/', methods=['GET', 'POST'])
def home():
    userLogedIn = checkUserLogin()
    if userLogedIn[0]:
        return render_template('main_menu.html')
    else:
        return render_template('login_signup.html', error=userLogedIn[3], typeOfContainer=userLogedIn[4], username=userLogedIn[2], email=userLogedIn[1])
        
@views.route('/account_options', methods=['GET'])
def account_options():
    userLogedIn = checkUserLogin()
    if userLogedIn[0]:
        return render_template('account_options.html')
    else:
        return render_template('login_signup.html', error=userLogedIn[3], typeOfContainer=userLogedIn[4], username=userLogedIn[2], email=userLogedIn[1])

# =====================================================================================

# GAMES

@views.route('/game', methods=['POST'])
def add_game():
    userLogedIn = checkUserLogin()
    if userLogedIn[0]:
        if request.method == 'POST':
            data_retrieved = False
            if data_retrieved == False and 'audio_data' in request.files: # Audio

                file = request.files['audio_data']
                filename = saveAudioFile(file)
                jitter, shimmer = calculateAudioParameters(filename)
                gameTypeIndex = 6
                data_retrieved = True

                new_game = Game(patient_id=current_user.id, gameTypeIndex=gameTypeIndex, currentTime=dt.now(), audioPath=filename, jitter=jitter, shimmer=shimmer)

            if data_retrieved == False and 'image' in request.json: # Image

                image = request.json['image']
                gameTypeIndex = 4
                timeSpent = request.json['timeSpent']
                imageType = request.json['imageType']
                reference_image = ['spiral', 'wave', 'clock'][['Espiral', 'Onda', 'Relógio'].index(imageType)]

                score = calculate_image_accuracy(image, reference_image) # calculate

                data_retrieved = True

                new_game = Game(patient_id=current_user.id, gameTypeIndex=gameTypeIndex, currentTime=dt.now(), score=score, timeSpent=timeSpent, image=image)

            if data_retrieved == False: # Rest of games

                score = request.json['score']
                gameTypeIndex = request.json['gameType']
                timeSpent = request.json['timeSpent']

                new_game = Game(patient_id=current_user.id, gameTypeIndex=gameTypeIndex, currentTime=dt.now(), score=score, timeSpent=timeSpent)


            # Add game
            db.session.add(new_game)

            # Add achievement
            check_game_achievements(gameTypeIndex)

            db.session.commit()

            return render_template('main_menu.html')
    else:
        return render_template('login_signup.html', error=userLogedIn[3], typeOfContainer=userLogedIn[4], username=userLogedIn[2], email=userLogedIn[1])

@views.route('/game/<int:index>', methods=['GET', 'POST'])
def handle_game(index):
    userLogedIn = checkUserLogin()
    if userLogedIn[0]:
        game_file = '/games/game' + str(index) + '.html'
        record = calculate_record(index)
        if index == 4: # Imagem aleatoria para desenhar
            randomNum = randint(0,2)
            image = ['spiral', 'wave', 'clock'][randomNum]
            game = ['Espiral', 'Onda', 'Relógio'][randomNum]
            text = ['Vamos desenhar uma espiral. Tente desenhar por cima do tracejado.', 'Vamos desenhar uma onda. Tente desenhar por cima do tracejado até ao avião.', 'Ainda se lembra como se desenha um relógio? Desenhe um relógio analógico às 11 horas e 10 minutos.'][randomNum]
            return render_template(game_file, record=record, image=image, text=text, game=game)
        
        return render_template(game_file, record=record)
    else:
        return render_template('login_signup.html', error=userLogedIn[3], typeOfContainer=userLogedIn[4], username=userLogedIn[2], email=userLogedIn[1])

def calculate_record(game_index):
    gamesList = Game.query.filter_by(patient_id=current_user.id, gameTypeIndex=game_index).all()
    typeOfRecord = {1: 'min', 2: 'max', 3: 'min', 4: 'max', 5: 'max', 6: ''}
    if (len(gamesList)):
        if (typeOfRecord[game_index] == 'max'): # Quando o recorde é o máximo
            tempRecord = 0
            for game in gamesList:
                if (int(game.score) > tempRecord):
                    tempRecord = int(game.score)
        elif (typeOfRecord[game_index] == 'min'):  # Quando o recorde é o mínimo
            tempRecord = 10000
            for game in gamesList:
                if (int(game.score) < tempRecord):
                    tempRecord = int(game.score)
        else:
            tempRecord = -1
        typeOfActions = {1: 'milissegundos', 2: 'cliques', 3: 'tentativas', 4: '%', 5: 'pontos', 6: ''}
        record = 'Recorde: ' + str(tempRecord) + ' ' + typeOfActions[game_index]
    else:
        record = ''
    
    return record

"""@views.route('/listGames', methods=['GET'])
def listGames():
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
    #return render_template('graph.html', gamesList=gamesList, availableGames=availableGames, recordAvailableGames=recordAvailableGames, typeOfActions=typeOfActions)"""

@views.route('/choose_game', methods=['GET']) # show evolution
def choose_game():
    userLogedIn = checkUserLogin()
    if userLogedIn[0]:
        return render_template('choose_game.html')
    else:
        return render_template('login_signup.html', error=userLogedIn[3], typeOfContainer=userLogedIn[4], username=userLogedIn[2], email=userLogedIn[1])



@views.route('/evolution/<int:index>', methods=['GET']) # show evolution
def evolution(index):
    userLogedIn = checkUserLogin()
    if userLogedIn[0]:
        return render_template('graph.html', index=index)
    else:
        return render_template('login_signup.html', error=userLogedIn[3], typeOfContainer=userLogedIn[4], username=userLogedIn[2], email=userLogedIn[1])


@views.route('/choose_game_evolution') # pick evolution
def choose_game_evolution():
    userLogedIn = checkUserLogin()
    if userLogedIn[0]:
        return render_template('choose_game_evolution.html', options=database_games)
    else:
        return render_template('login_signup.html', error=userLogedIn[3], typeOfContainer=userLogedIn[4], username=userLogedIn[2], email=userLogedIn[1])

@views.route('/games_data/<int:index>', methods=['GET']) # Get games data for graph
def games_data(index):
    userLogedIn = checkUserLogin()
    if userLogedIn[0]:
        games_list = [serialize_game(x) for x in Game.query.filter_by(patient_id=current_user.id, gameTypeIndex=index).all()]
        return jsonify({'games_list': games_list, 'unit': database_games[index-1]['action'], 'type': database_games[index-1]['name']})
    else:
        return render_template('login_signup.html', error=userLogedIn[3], typeOfContainer=userLogedIn[4], username=userLogedIn[2], email=userLogedIn[1])

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

# ====================================================================================

# ASSESSMENT

@views.route('/choose_assessment', methods=['GET'])
def choose_assessment():
    userLogedIn = checkUserLogin()
    if userLogedIn[0]:
        return render_template('choose_assessment.html', options=[{'name': 'Diagnóstico Parkinson'}, {'name': 'Tarefas do dia a dia'}])
    else:
        return render_template('login_signup.html', error=userLogedIn[3], typeOfContainer=userLogedIn[4], username=userLogedIn[2], email=userLogedIn[1])


@views.route('/assessment', methods=['GET', 'POST'])
def assessment():
    userLogedIn = checkUserLogin()
    if userLogedIn[0]:
        if request.method == 'GET': # Fazer questionário
            assessment_index = request.args.get('index')
            currentAssessment = database_assessments[int(assessment_index)]
            return render_template('assessment.html', assessment=currentAssessment)

        else: # Adicionar questionário
            assessmentType = request.json['type']
            answers = request.json['answers']

            try:
                current_time = request.json['medication']
                medicationTime = dt(dt.now().year, dt.now().month, dt.now().day, int(current_time.split(':')[0]), int(current_time.split(':')[1]), 0, 0)
                new_medication = Medication(patient_id=current_user.id, currentTime=medicationTime, medicationType=0)
                db.session.add(new_medication)
            except:
                pass

            new_assessment = Assessment(testType=assessmentType, patient_id=current_user.id, currentTime=dt.now())
            db.session.add(new_assessment)
            db.session.commit() # to be able to get the assessment id for the questions

            for index, answer in enumerate(answers):
                new_answer = Question(indexInAssessment=index, question=index, answer=answer, assessment_id=new_assessment.id)
                db.session.add(new_answer)

            check_test_achievements(assessmentType)

            db.session.commit()

            return render_template('main_menu.html')
    else:
        return render_template('login_signup.html', error=userLogedIn[3], typeOfContainer=userLogedIn[4], username=userLogedIn[2], email=userLogedIn[1])



@views.route('/choose_assessment_list', methods=['GET'])
def choose_assessment_list():
    userLogedIn = checkUserLogin()
    if userLogedIn[0]:
        return render_template('choose_assessment_list.html', options=database_assessments)
    else:
        return render_template('login_signup.html', error=userLogedIn[3], typeOfContainer=userLogedIn[4], username=userLogedIn[2], email=userLogedIn[1])

@views.route('/choose_assessment/<int:index>', methods=['GET']) # show evolution
def choose_assement_index(index):
    userLogedIn = checkUserLogin()
    if userLogedIn[0]:
        options = []
        for entry in database_assessments:
            options.append(entry['name'])
        assessment_name = options[index-1]

        if not assessment_name == 'Sintomas':
            assessmentListAfter = []
            assessmentListBefore = Assessment.query.filter_by(patient_id=current_user.id, testType = assessment_name).all()

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
        else:
            # ON - Sem sintomas (Doença controlada) - 1
            # ON - Com movimentos involuntários - 1
            # OFF - Com sintomas motores, rigidez, dureza e menos mobilidade - 0
            return render_template('dairy.html')

        return render_template('assessment_list.html', assessmentList=assessmentListAfter)

    else:
        return render_template('login_signup.html', error=userLogedIn[3], typeOfContainer=userLogedIn[4], username=userLogedIn[2], email=userLogedIn[1])
 
@views.route('/assessments', methods=['GET']) # Ver lista de questionários
def assessments():
    userLogedIn = checkUserLogin()
    if userLogedIn[0]:
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
    else:
        return render_template('login_signup.html', error=userLogedIn[3], typeOfContainer=userLogedIn[4], username=userLogedIn[2], email=userLogedIn[1])


@views.route('/assessments_data', methods=['GET']) # Get games data for graph
def assessments_data():
    userLogedIn = checkUserLogin()
    if userLogedIn[0]:
        todayDate = dt(dt.now().year, dt.now().month, dt.now().day, 0, 0)
        assessment_list = Assessment.query.filter_by(patient_id=current_user.id, testType = 'Sintomas').all()
        medication_list = Medication.query.filter_by(patient_id=current_user.id).all()
        medicationAfter = []
        for element in medication_list:
            medicationAfter.append(element.currentTime)
        # get questions from assessments
        questions = []
        previous_answer = {'time': '', 'answer': -1}
        for assessment in assessment_list:
            # { time: time, assessment_id: id}
            time = assessment.currentTime
            answer = Question.query.filter_by(assessment_id=assessment.id).all()
            answer = answer[0].answer
            if (answer == 1):
                answer = 1
            elif (answer == 2):
                answer = 1
            else:
                answer = 0
            
            complete_answer = {'time': time, 'answer': answer }
            if previous_answer['answer'] != -1 and previous_answer['answer'] != complete_answer['answer']:
                if answer == 0:
                    reverse_answer = 1
                else:
                    reverse_answer = 0
                fake_answer = {'time': complete_answer['time'] - datetime.timedelta(seconds=1), 'answer': reverse_answer }
                questions.append(fake_answer)
            previous_answer = complete_answer
            questions.append( complete_answer )
        return jsonify({'assessments_list': questions, 'medication_list': medicationAfter})
    else:
        return render_template('login_signup.html', error=userLogedIn[3], typeOfContainer=userLogedIn[4], username=userLogedIn[2], email=userLogedIn[1])

# =====================================================       

@views.route('/info', methods=['GET'])
def info():
    userLogedIn = checkUserLogin()
    if userLogedIn[0]:
        if request.method == 'GET':
            current_info = database_diseases[1]
            return render_template('info.html', current_info=current_info)
    else:
        return render_template('login_signup.html', error=userLogedIn[3], typeOfContainer=userLogedIn[4], username=userLogedIn[2], email=userLogedIn[1])
       


@views.route('/info_choose', methods=['GET'])
def info_choose():
    userLogedIn = checkUserLogin()
    if userLogedIn[0]:
        return render_template('info_choose.html', options=database_diseases)
    else:
        return render_template('login_signup.html', error=userLogedIn[3], typeOfContainer=userLogedIn[4], username=userLogedIn[2], email=userLogedIn[1])
       

# =======================================================

@views.route('/achievements', methods=['GET']) # Ver lista de conquistas
def achievements():
    userLogedIn = checkUserLogin()
    if userLogedIn[0]:
        achivements = Achievement.query.filter_by(patient_id=current_user.id).all()
        return render_template('achievements.html', database_achievements=achivements)
    else:
        return render_template('login_signup.html', error=userLogedIn[3], typeOfContainer=userLogedIn[4], username=userLogedIn[2], email=userLogedIn[1])

# ===========================================



@views.route("/<path:path>")
def get_files(path):
    if path == 'manifest.json' or path == 'icons/icon-192x192.png' or path == 'icons/icon-512x512.png' or path == 'sw.js':
        return send_from_directory('static', 'PWA/'+path)
    else:
        return render_template('error_page.html'), 404
 