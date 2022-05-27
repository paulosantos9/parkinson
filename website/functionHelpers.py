import datetime
from flask import session
from flask_login import current_user
from random import randint
import re

database_assessments = [
    {
        'name': 'UPDRS',
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
        'name': 'IADL',
        'questions': [
            {
                'question': 'Ability to Use Telephone.',
                'answers': [
                    'Operates telephone on own initiative-looks up and dials numbers, etc.',
                    'Dials a few well-known numbers.',
                    'Answers telephone but does not dial.',
                    'Does not use telephone at all.'
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
    }
]


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
