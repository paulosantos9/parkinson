from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import current_user
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
                numberOfGames = 4
                current_game = chooseGame(numberOfGames)
                return render_template(current_game)

            elif (current_page == 'account'):
                return render_template('account.html')

            elif (current_page == 'gamesList'):
                gamesList = Game.query.filter_by(patient_id=current_user.id).all()
                availableGames = ['Reação', 'Rapidez', 'Memória', 'Desenho']
                typeOfActions = ['milissegundos', 'cliques', 'tentativas', '']
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
                    elif (i == 3):
                        # Desenho
                        pass
                    else:
                        # Inválido
                        pass
                    recordAvailableGames.append(tempRecord)
                return render_template('games_list.html', gamesList=gamesList, availableGames=availableGames, recordAvailableGames=recordAvailableGames, typeOfActions=typeOfActions)

            elif (current_page == 'assessment'):
                return render_template('assessment.html')

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
    if request.method == 'GET': # Jogar
        session['page'] = 'game'
    else: # Guardar resultado jogo
        try: # Porque o desenho não tem score
            score = request.json['score'] # because its type application/json
        except:
            score = ''
        gameTypeIndex = request.json['gameType']
        try: # Porque os jogos não tem imagem
            image = request.json['image']
        except:
            image = ''
        new_game = Game(patient_id=current_user.id, gameTypeIndex=gameTypeIndex, currentTime=datetime.now(), score=score, image=image)
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
    session['page'] = 'gamesList'
    return redirect(url_for('views.home'))

@views.route('/assessment', methods=['GET', 'POST'])
def assessment():
    if request.method == 'GET': # Fazer teste
        session['page'] = 'assessment'
        return redirect(url_for('views.home'))
    else: # Adicionar teste
        questions = []
        answers = []
        questions.append('1. Durante a última semana, você teve algum problema para adormecer à noite ou em permanecer dormindo durante a noite? Considere o quanto descansado se sentiu ao acordar de manhã..')
        answers.append(request.json['first-answer'])
        questions.append('2. Durante a última semana, teve dificuldade em manter-se acordado durante o dia?')
        answers.append(request.json['second-answer'])
        questions.append('3. Durante a última semana, teve sensações desconfortáveis no seu corpo tais como dor, sensação de ardor, formigamento ou cãimbras?')
        answers.append(request.json['third-answer'])
        questions.append('4. Durante a última semana, teve problemas em reter a urina? Por exemplo, necessidade urgente em urinar, necessidade de urinar vezes de mais, ou perder controlo da urina?')
        answers.append(request.json['forth-answer'])
        questions.append('5. Durante a última semana, teve problemas de obstipação intestinal (prisão de ventre) que lhe tenham causado dificuldade em evacuar?')
        answers.append(request.json['fifth-answer'])
        questions.append('6. Durante a última semana, sentiu que iria desmaiar, ficou tonto ou com sensação de cabeça vazia quando se levantou, após ter estado sentado ou deitado?')
        answers.append(request.json['sixth-answer'])
        questions.append('7. Durante a última semana, sentiu-se habitualmente fatigado? Esta sensação não é por estar com sono ou triste.')
        answers.append(request.json['seventh-answer'])

        new_assessment = Assessment(testType='UPDRS', patient_id=current_user.id, currentTime=datetime.now())
        db.session.add(new_assessment)
        db.session.commit() # to be able to get the assessment id
        
        for i in range(len(answers)):
            temp_answer = Question(indexInAssessment=0, question=questions[i], answer=answers[i], assessment_id=new_assessment.id)
            db.session.add(temp_answer)
            
        db.session.commit()
        session['page'] = 'main_menu'
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
    