from django.shortcuts import redirect
from .models import Achievement
from datetime import datetime
from flask import session
from flask_login import current_user
from random import randint
import re
from math import sqrt
import base64
from PIL import Image
import os
from werkzeug.utils import secure_filename
import parselmouth
from parselmouth.praat import call

database_games = [
    {
        'name':'Reação',
        'action': 'milissegundos',
        'bestRecord': 'min',
    },
    {
        'name': 'Rapidez',
        'action': 'cliques',
        'bestRecord': 'max',
    },
    {
        'name': 'Memória',
        'action': 'tentativas',
        'bestRecord': 'min',
    },
    {
        'name': 'Desenho',
        'action':'%',
        'bestRecord': 'max',
    },
    {
        'name': 'Equilíbrio',
        'action':'pontos',
        'bestRecord': 'max',
    },
    {
        'name': 'Audio',
        'action': '',
        'bestRecord': '',
    }
]

database_achievements = [
    {
        'icon': 'mobile',
        'name': 'Jogador',
        'description': 'Jogue pelo menos um jogo.',
    },
    {
        'icon': 'flash',
        'name': 'Reação',
        'description': 'Jogue pelo menos uma vez o jogo da reação.',
    },
    {
        'icon': 'tap',
        'name': 'Rapidez',
        'description': 'Jogue pelo menos uma vez o jogo da rapidez.',
    },
    {
        'icon': 'memory',
        'name': 'Memória',
        'description': 'Jogue pelo menos uma vez o jogo da memória.',
    },
    {
        'icon': 'draw',
        'name': 'Desenho',
        'description': 'Faça pelo menos um desenho.',
    },
    {
        'icon': 'balance',
        'name': 'Equilíbrio',
        'description': 'Jogue pelo menos uma vez o jogo do equilíbrio.',
    },
    {
        'icon': 'talk',
        'name': 'Fala',
        'description': 'Faça pelo menos um teste da fala.',
    },
    {
        'icon': 'master',
        'name': 'Mestre',
        'description': 'Jogar todos os jogos.'
    },
    {
        'icon': 'test',
        'name': 'Teste',
        'description': 'Faça pelo menos um questionário.'
    },
    {
        'icon': 'smile',
        'name': 'Sintomas',
        'description': 'Indique pelo menos uma vez como se sente.'
    },
    {
        'icon': 'brain',
        'name': 'UPDRS',
        'description': 'Faça pelo menos um questionário relativo ao UPDRS.'
    },
    {
        'icon': 'daly',
        'name': 'Tarefas',
        'description': 'Faça pelo menos um questionário relativo às tarefas do dia a dia.'
    }
]

database_diseases = [
    {
        'name': "Doença de Alzheimer",
        'entries': [
            {
                'name': 'História',
                'info': 'A doença de Alzheimer é a doença neurodegenerativa mais comum e representa também a causa mais frequente de demência, cerca de 70% do total de casos.'
            },
            {
                'name': 'Sintomas',
                'info': 'A manifestação clínica mais presente é a demência, o que significa uma maior perda cognitiva que o esperado para a idade do paciente. Outros sintomas incluem alterações de humor, personalidade e comportamentos, perda de memória, dificuldades linguísticas e motores e alucinações.'
            },
            {
                'name': 'Diagnóstico',
                'info': 'Ainda não existem atualmente um único teste capaz de detetar a presença de Alzheimer. O que acontece é que é feita uma análise a dierentes componentes que permite aos doutores fazerem um diagnóstico. Estes componentes incluem a análise do histórico médico do paciente e da sua família, testemunhos familiares em termos de abilidades mentais e comportamentos, testes cognitivos, testes sanguíneos e imagens médicas do cérebro e presença de biomarcadores desta doença.',
            },
            {
                'name': 'Prevalência',
                'info': 'Estudos apontam para mais de 50 milhões de pessoas com esta doença em todo o mundo, sendo que esperado que atinja os 150 milhões em 2050. Ocorre especialmente em pessoas mais idosas, principalmente após os 65 anos. Portugal é o quarto país da União Europeia com maior percentagem de casos de Alzheimer, cerca de 2%.'
            },
            {
                'name': 'Tratamentos',
                'info': 'O número de tratamentos disponíveis para Alzheimer são limitados. Fatores que ajudam na melhoria dos sintomas nestes pacientes incluem a estimulação cognitiva e a prática de exercício físico. Os jogos que apresentamos nesta aplicação ajudam a melhorar a capacidade cognitiva dos pacientes.'
            }
        ]

    },
    {
        'name': "Doença de Parkinson",
        'entries': [
            {
                'name': 'História',
                'info': 'A doença de Parkinson é a segunda doença neurodegenerativa mais comum atualmente e a sua prevalência tem aumentado mais rapidamente do que as restantes, sendo principalmente caraterizada por deficiências nas capacidades motoras.'
            },
            {
                'name': 'Sintomas',
                'info': 'O sintoma mais frequente na doença de Parkinson são as deficiências motoras, que incluem a lentidão dos movimentos, tremores em repouso, rigidez muscular, problemas posturais e dificuldades em falar ou engolir. Outros problemas incluem perturbações do sono e do humor, caligrafia pequena, problemas de visão, depressão e dores.',
            },
            {
                'name': 'Diagnóstico',
                'info': 'O diagnóstico da doença de Parkinson baseia-se na avaliação dos sintomas clínicos, tais como a lentidão de movimentos, tremores em repouso e rigidez, histórico médico e exames físicos, como reflexos, sensibilidade e agilidade. Os médicos utilizam ainda testes padrão com perguntas e respostas para verificar a presença da doença e a sua gravidade.',
            },
            {
                'name': 'Prevalência',
                'info': 'Estudos apontam para mais de 8 milhões de pessoas com doença de Parkinson no mundo, com o aparecimento anual de 1 milhão de novos casos e 340 mil mortes. Estudos apontam para uma maior percentagem de homens com doença, sendo que o aparecimento nas mulheres ocorre mais tarde.'
            },
            {
                'name': 'Tratamentos',
                'info': 'A doença de Parkinson não tem cura atualmente e o tratamento foca-se no alívio dos sintomas. O tratamento inclui medicação, terapia física e estimulação cerebral profunda. Com o passar do tempo a medicação torna-se menos efetiva, pelo que os médicos vão ajustando o tipo e a dosagem da medicação.'
            }
        ]

    },
]

database_assessments = [
    {
        'name': 'Sintomas',
        'questions': [
            {
                'question': 'Como estão os sintomas?',
                'answers': [
                    'Sem sintomas (Doença controlada)',
                    'Com movimentos involuntários',
                    'Com sintomas motores, rigidez, dureza e menos mobilidade'
                ]
            }
        ]
    },
    {
        'name': 'Diagnóstico Parkinson',
        'questions': [
            {
                'question': 'Durante a última semana, você teve algum problema para adormecer à noite ou em permanecer dormindo durante a noite? Considere o quanto descansado se sentiu ao acordar de manhã.',
                'answers': [
                    'Sem problemas.',
                    'Os problemas do sono existem, mas habitualmente não impedem que tenha uma noite de sono completa.',
                    'Os problemas do sono causam habitualmente alguma dificuldade em ter uma noite de sono completa.',
                    'Os problemas do sono causam muitas dificuldades em ter uma noite de sono completa, mas habitualmente ainda durmo mais de metade da noite.',
                    'Habitualmente não consigo dormir durante a maior parte da noite.'
                ]
            },
            {
                'question': 'Durante a última semana, teve dificuldade em manter-se acordado durante o dia?',
                'answers': [
                    'Sem sonolência durante o dia.',
                    'Tenho sonolência durante o dia, mas consigo resistir e permaneço acordado.',
                    'Por vezes adormeço quando estou sozinho e relaxado. Por exemplo, enquanto leio ou vejo televisão.',
                    'Por vezes adormeço quando não deveria. Por exemplo, enquanto como ou falo com outras pessoas.',
                    'Adormeço frequentemente quando não deveria. Por exemplo, enquanto como ou falo com outras pessoas.'
                ]
            },
            {
                'question': 'Durante a última semana, teve sensações desconfortáveis no seu corpo tais como dor, sensação de ardor, formigamento ou cãimbras?',
                'answers': [
                    'Não tenho estas sensações desconfortáveis.',
                    'Tenho estas sensações desconfortáveis. No entanto, consigo fazer coisas e estar com outras pessoas sem dificuldade.',
                    'Estas sensações causam alguns problemas quando faço coisas ou estou com outras pessoas.',
                    'Estas sensações causam muitos problemas, mas não me impedem de fazer coisas ou de estar com outras pessoas.',
                    'Estas sensações impedem-me de fazer coisas ou de estar com outras pessoas.'
                ]
            },
            {
                'question': 'Durante a última semana, teve problemas em reter a urina? Por exemplo, necessidade urgente em urinar, necessidade de urinar vezes de mais, ou perder controlo da urina?',
                'answers': [
                    'Sem problemas em reter a urina.',
                    'Preciso de urinar frequentemente ou tenho urgência em urinar. No entanto, estes problemas não me causam dificuldades nas atividades diárias.',
                    'Os problemas com a urina causam-me algumas dificuldades nas atividades diárias. No entanto, não tenho perdas acidentais de urina.',
                    'Os problemas com a urina causam-me muitas dificuldades nas atividades diárias, incluindo perdas acidentais de urina.',
                    'Não consigo reter a minha urina e uso uma fralda ou tenho sonda urinária.'
                ]
            },
            {
                'question': 'Durante a última semana, teve problemas de obstipação intestinal (prisão de ventre) que lhe tenham causado dificuldade em evacuar?',
                'answers': [
                    'Sem obstipação (prisão de ventre).',
                    'Tive obstipação (prisão de ventre). Faço um esforço extra para evacuar. No entanto, este problema não perturba as minhas atividades ou o meu conforto.',
                    'A obstipação (prisão de ventre) causa-me alguma dificuldade em fazer coisas ou em estar confortável.',
                    'A obstipação (prisão de ventre) causa-me muita dificuldade em fazer coisas ou em estar confortável. No entanto, não me impede de fazer o que quer que seja.',
                    'Habitualmente preciso da ajuda física de outra pessoa para evacuar.'
                ]
            },
            {
                'question': 'Durante a última semana, sentiu que iria desmaiar, ficou tonto ou com sensação de cabeça vazia quando se levantou, após ter estado sentado ou deitado?',
                'answers': [
                    'Não tenho a sensação de cabeça vazia ou tonturas.',
                    'Tenho a sensação de cabeça vazia ou de tonturas, mas não me causam dificuldade em fazer coisas.',
                    'A sensação de cabeça vazia ou de tonturas fazem com que tenha de me segurar a alguma coisa, mas não preciso de me sentar ou deitar.',
                    'A sensação de cabeça vazia ou de tonturas fazem com que tenha de me sentar ou deitar para evitar desmaiar ou cair.',
                    'A sensação de cabeça vazia ou de tonturas fazem com que caia ou desmaie.'
                ]
            },
            {
                'question': 'Durante a última semana, sentiu-se habitualmente fatigado? Esta sensação não é por estar com sono ou triste.',
                'answers': [
                    'Sem fadiga.',
                    'Sinto fadiga. No entanto, não me causa dificuldade em fazer coisas ou em estar com pessoas.',
                    'A fadiga causa-me alguma dificuldade em fazer coisas ou em estar com pessoas.',
                    'A fadiga causa-me muita dificuldade em fazer coisas ou em estar com pessoas. No entanto, não me impede de fazer nada.',
                    'A fadiga impede-me de fazer coisas ou de estar com pessoas.'
                ]
            }
        ]
    },
    {
        'name': 'Tarefas do dia a dia',
        'questions': [
            {
                'question': 'Usar o telemóvel.',
                'answers': [
                    'Capaz de operar o telefone por iniciativa própria. Procura e marca números de telefone.',
                    'Capaz de marcar alguns números bem conhecidos.',
                    'Capaz de atender mas não sabe ligar.',
                    'Não usa o telemóvel.'
                ]
            },
            {
                'question': 'Fazer compras.',
                'answers': [
                    'Capaz de tratar de todas as necessidades de compras sozinho.',
                    'Capaz de tratar de pequenas compras sozinho.',
                    'Precisa de acompanhamento em qualquer viagem de compras.',
                    'Completamente incapaz de fazer compras.'
                ]
            },
            {
                'question': 'Preparar comida.',
                'answers': [
                    'Capaz de planear, preparar e servir refeições adequadas independentemente.',
                    'Capaz de preparar refeições adequadas se tiver os ingredientes.',
                    'Capaz de aquecer, servir e preparar refeições, mas não mantém uma dieta adequada.',
                    'Necessita de ter as refeições preparadas e servidas.'
                ]
            },
            {
                'question': 'Doméstica.',
                'answers': [
                    'Capaz de manter a casa sozinha ou com ajuda ocasional, no caso de trabalhos pesados.',
                    'Capaz de realizar tarefas diárias leves, como lavar pratos e fazer as camas.',
                    'Capaz de realizar tarefas diárias leves mas não conseque manter um nível aceitável de limpeza.',
                    'Precisa de ajuda com todas as tarefas domésticas.',
                    'Não participa nas tarefas domésticas.'
                ]
            },
            {
                'question': 'Lavandaria.',
                'answers': [
                    'Capaz de lavar a roupa pessoal de forma completa.',
                    'Capaz de lavar apenas pequenos artigos, como por exemplo meias.',
                    'Toda a lavandaria tem de ser feita por outras pessoas.'
                ]
            },
            {
                'question': 'Meio de transporte.',
                'answers': [
                    'Capaz de viajar de forma independente em transportes públicos ou no próprio carro.',
                    'Capaz de organizar a sua viagem de forma autónoma de taxi, mas não consegue utilizar outros transportes públicos.',
                    'Capaz de viajar em transportes públicos quando acompanhado.',
                    'Capaz de viajar de taxi ou carro apenas com assistência.',
                    'Não viaja a lado nenhum.'
                ]
            },
            {
                'question': 'Responsabilidade na medicação.',
                'answers': [
                    'Capaz de tomar a medicação correta, nas dosagens corretas e à hora correta.',
                    'Capaz de tomar a medicação se preparada previamente, com dosagens separadas.',
                    'Não consegue tomar medicação sozinho.'
                ]
            },
            {
                'question': 'Finanças.',
                'answers': [
                    'Capaz de gerir as questões financeiras de forma independente, como pagar a renda, faturas e ir ao banco.',
                    'Capaz de gerir as compras do dia a dia, mas precisa de ajuda com bancos e compras importantes.',
                    'Incapaz de lidar com dinheiro.'
                ]
            },
        ]
    }
]

def manageSession():
    error = session.get('error')
    typeOfContainer = session.get('typeOfContainer')
    if typeOfContainer:
        typeOfContainer = int(typeOfContainer)
    session.pop('error', '')
    session.pop('typeOfContainer', 0)
    return error, typeOfContainer

def chooseGame(numberOfGames):
    index = randint(0, len(numberOfGames)-1)
    gameType = numberOfGames[index]
    return gameType

def isPasswordValid(password, password_confirm):
    minLength = 8
    if len(password) < minLength:
        return False, 'Palavra-passe deve ter ' + str(minLength) + ' ou mais caracteres.'
    elif not re.search("[a-z]", password):
        return False, 'Palavra-passe deve ter letras minúsculas, maiúsculas, números e símbolos.'
    elif not re.search("[A-Z]", password):
        return False, 'Palavra-passe deve ter letras minúsculas, maiúsculas e números e símbolos.'
    elif not re.search("[0-9]", password):
        return False, 'Palavra-passe deve ter letras minúsculas, maiúsculas e números e símbolos.'
    elif not set(password).intersection("!\"#$%&()*+,-/:;<=>?@[\]^`{|}~'._"):
        return False, 'Palavra-passe deve ter letras minúsculas, maiúsculas e números e símbolos.'
    elif re.search("\s", password):
        return False, 'Palavra-passe não pode ter espaços.'
    elif password != password_confirm:
        return False, 'Palavras-passe têm de ser iguais.'
    else:
        return True, ''

def isEmailValid(email):
    """regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    regexAlernative = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{1,10}+[@]\w+[.]\w{2,3}$'
    return re.search(regex,email) or re.search(regexAlernative,email)"""
    return True

def isUsernameValid(username):
    minLength = 4
    maxLength = 50
    if re.search("[0-9]", username[0]):
        return False, 'Nome de utilizador não pode começar por um número.'
    elif (len(username)<minLength):
        return False, 'Nome de utilizador deve ter ' + str(minLength) + ' ou mais caracteres.'
    elif (len(username)>maxLength):
        return False, 'Nome de utilizador só pode ter até ' + str(maxLength) + ' caracteres.'
    elif set(username).intersection("!\"#$%&()*+,-/:;<=>?@[\]^`{|}~'"):
        return False, 'Nome de utilizador só pode conter caracteres alfanuméricos e os símbolos . e _.'
    elif re.search("\s", username):
        return False, 'Nome de utilizador não pode ter espaços.'
    else:
        return True, ''


def check_game_achievements(gameTypeIndex):
    # Jogador
    achievement = Achievement.query.filter_by(patient_id=current_user.id, name='Jogador').all()
    if achievement[0].locked == True:
        achievement[0].locked = False

    # First try games achievements
    games_names = ['Reação', 'Rapidez', 'Memória', 'Desenho', 'Equilíbrio', 'Fala']
    achievement = Achievement.query.filter_by(patient_id=current_user.id, name=games_names[gameTypeIndex-1]).all()
    if achievement[0].locked == True:
        achievement[0].locked = False

    # Mestre
    played_all_games = True
    for game in games_names:
        achievement = Achievement.query.filter_by(patient_id=current_user.id, name=game).all()
        if achievement[0].locked == True:
            played_all_games = False
            break
    achievement = Achievement.query.filter_by(patient_id=current_user.id, name='Mestre').all()
    achievement[0].locked = not played_all_games

def check_test_achievements(assessmentType):
    # Test
    achievement = Achievement.query.filter_by(patient_id=current_user.id, name='Teste').all()
    if achievement[0].locked == True:
        achievement[0].locked = False

    # First try test achievements
    test_names = []
    for entry in database_assessments:
        test_names.append(entry['name'])
    test_index = test_names.index(assessmentType)
    achievement_options = ['Sintomas', 'UPDRS', 'Tarefas']
    achievement_name = achievement_options[test_index]
    achievement = Achievement.query.filter_by(patient_id=current_user.id, name=achievement_name).all()
    if achievement[0].locked == True:
        achievement[0].locked = False

def calculate_image_accuracy(image_data, reference_image):
    # get reference image
    cwd = os.getcwd()
    if 'home' in cwd:
        reference_image = Image.open(cwd + '/mysite/website/static/images/reference_' + reference_image + '.png')
    else:
        reference_image = Image.open(cwd + '/website/static/images/reference_' + reference_image + '.png')
    reference_pixels = reference_image.getdata()
    reference_image_side = int(sqrt(len(reference_pixels)))
    # invert reference image
    inverted_reference_image = []
    for pixel in reference_pixels: # background white
        #print(pixel)
        if pixel == (255,255,255,255) or pixel == (255,255,255):
            inverted_reference_image.append(0)
        else:
            inverted_reference_image.append(1)


    # get test image
    image_saved_bytes = image_data.split(',')[1]
    image_saved_bytes = bytes(image_saved_bytes, 'utf-8')

    while True:
        if 'home' in cwd:
            file_name = cwd + "/mysite/website/static/images/temp/image_test_" + secure_filename(str(datetime.now())) + '.png'
        else:
            file_name = cwd + "/website/static/images/temp/image_test_" + secure_filename(str(datetime.now())) + '.png'
        if not os.path.exists(file_name): break
    print(file_name)

    with open(file_name, "wb") as fh:
        fh.write(base64.decodebytes(image_saved_bytes) + b'==')

    image_test = Image.open(file_name)
    image_test = image_test.resize((reference_image_side, reference_image_side))
    test_pixels = image_test.getdata()
    # invert test image
    inverted_test_image = []
    for pixel in test_pixels:
        if pixel == (0, 0, 0, 0): # empty
            inverted_test_image.append(0)
        else:
            inverted_test_image.append(1)

    # compare images
    total_pixels = inverted_reference_image.count(1)
    image_sobreposition = [a and b for a, b in zip(inverted_reference_image, inverted_test_image)]
    correct_pixels = image_sobreposition.count(1)

    reference_image.close()
    image_test.close()
    os.remove(file_name)

    return int(correct_pixels / total_pixels * 100) # percentage

def saveAudioFile(file):
    # extension name
    extname = '.wav'

    # get a viable filename
    cwd = os.getcwd()
    while True:
        timeNow = str(datetime.now()).replace('.', '_')
        if 'home' in cwd:
            timeNow = str(datetime.now()).replace('.', '_')
            dst = cwd + '/mysite/website/static/audio/' + secure_filename(f'{timeNow}{extname}')
        else:
            dst = os.path.join(
                'website\\static\\audio',
                secure_filename(f'{timeNow}{extname}'))


        if not os.path.exists(dst): break

    # Save the file to disk.
    file.save(dst)

    return dst

def calculateAudioParameters(filename):
    f0min = 75
    f0max = 500

    sound = parselmouth.Sound(filename) # read the sound
    #pitch = call(sound, "To Pitch", 0.0, f0min, f0max) #create a praat pitch object
    #meanF0 = call(pitch, "Get mean", 0, 0, unit) # get mean pitch
    #stdevF0 = call(pitch, "Get standard deviation", 0 ,0, unit) # get standard deviation
    #harmonicity = call(sound, "To Harmonicity (cc)", 0.01, 75, 0.1, 1.0)
    #hnr = call(harmonicity, "Get mean", 0, 0)
    pointProcess = call(sound, "To PointProcess (periodic, cc)", f0min, f0max)

    localJitter = call(pointProcess, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
    #localabsoluteJitter = call(pointProcess, "Get jitter (local, absolute)", 0, 0, 0.0001, 0.02, 1.3)
    #rapJitter = call(pointProcess, "Get jitter (rap)", 0, 0, 0.0001, 0.02, 1.3)
    #ppq5Jitter = call(pointProcess, "Get jitter (ppq5)", 0, 0, 0.0001, 0.02, 1.3)
    #ddpJitter = call(pointProcess, "Get jitter (ddp)", 0, 0, 0.0001, 0.02, 1.3)

    localShimmer =  call([sound, pointProcess], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    #localdbShimmer = call([sound, pointProcess], "Get shimmer (local_dB)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    #apq3Shimmer = call([sound, pointProcess], "Get shimmer (apq3)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    #aqpq5Shimmer = call([sound, pointProcess], "Get shimmer (apq5)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    #apq11Shimmer =  call([sound, pointProcess], "Get shimmer (apq11)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    #ddaShimmer = call([sound, pointProcess], "Get shimmer (dda)", 0, 0, 0.0001, 0.02, 1.3, 1.6)

    return localJitter, localShimmer