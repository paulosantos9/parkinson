
let counterQuestion = 0;
let maxQuestions = document.getElementsByClassName('question').length;

function updateQuestion() {
    let questions = document.getElementsByClassName('question');
    for (let i = 0; i < maxQuestions; i++) {
        if (i === counterQuestion) {
            questions[counterQuestion].style.display = 'block';
        } else {
            questions[i].style.display = 'none';
        }
    }
}

function updateButtons() {
    if (counterQuestion === 0) {
        document.getElementById('anterior').value = '< Voltar';
        document.getElementById('seguinte').value = 'Seguinte >';
    } else if (counterQuestion === maxQuestions) {
        
    } else if (counterQuestion === maxQuestions-1) {
        document.getElementById('anterior').value = '< Anterior';
        document.getElementById('seguinte').value = 'Submeter';
    } else {
        document.getElementById('anterior').value = '< Anterior';
        document.getElementById('seguinte').value = 'Seguinte >'; 
    }
}

updateQuestion();
updateButtons();

function backToMain() {
    window.location.replace('/choose_assessment');
}

function submitAssessment() {

    const assessmentType = document.getElementById('title').textContent;

    const questions = document.getElementsByClassName('question');
    const numberOfQuestions = questions.length;
    let answers = [];
    for (let i = 0; i < numberOfQuestions; i++) { //
        answers.push(document.querySelector('input[name="question' + i + '"]:checked').value);
    }
    let data;
    if ( document.getElementById('medication') ) {
        // then its sintomas
        if (document.getElementById('medication').value ) {
            // then its filled
            console.log(0)
            data = {
                'type': assessmentType,
                'answers': answers,
                'medication': document.getElementById('medication').value
            }
            console.log(data)
        } else {
            console.log(1)
            data = {
                'type': assessmentType,
                'answers': answers,
            }
        }
    } else {
        console.log(2)
        data = {
            'type': assessmentType,
            'answers': answers,
        }
    }
    
    document.getElementById('medication').value
    fetch("/assessment", {
        method: "POST",
        headers: {'Content-Type': 'application/json'}, 
        body: JSON.stringify(data)
    }).then(res => {
        window.location.replace('/');
    });
}

document.getElementById('anterior').onclick = function() {
    counterQuestion--;
    if (counterQuestion < 0) {
        backToMain();
    }
    updateButtons();
    updateQuestion();
    if (counterQuestion < 0) {
        document.getElementById('anterior').style.display = 'none'
        document.getElementById('seguinte').style.display = 'none'
        document.getElementById('title').textContent = 'Voltando...'
    }
}

document.getElementById('seguinte').onclick = function() {
    counterQuestion++;
    if (counterQuestion >= maxQuestions) {
        submitAssessment();
    }
    updateButtons();
    updateQuestion();
    if (counterQuestion >= maxQuestions) {
        document.getElementById('anterior').style.display = 'none'
        document.getElementById('seguinte').style.display = 'none'
        document.getElementById('title').textContent = 'Guardando questionário...'
    }
}