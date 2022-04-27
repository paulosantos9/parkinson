let counterQuestion = 0;
let maxQuestions = 7;

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
        document.getElementById('anterior').value = 'Voltar';
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
    window.location.replace('/backToMain');
}

function submitAssessment() {
    let firstAnswer = document.querySelector('input[name="first-answer"]:checked').value;
    let secondAnswer = document.querySelector('input[name="second-answer"]:checked').value;
    let thirdAnswer = document.querySelector('input[name="third-answer"]:checked').value;
    let forthAnswer = document.querySelector('input[name="forth-answer"]:checked').value;
    let fifthAnswer = document.querySelector('input[name="fifth-answer"]:checked').value;
    let sixthAnswer = document.querySelector('input[name="sixth-answer"]:checked').value;
    let seventhAnswer = document.querySelector('input[name="seventh-answer"]:checked').value;
    let data = {
        'first-answer': firstAnswer,
        'second-answer': secondAnswer,
        'third-answer': thirdAnswer,
        'forth-answer': forthAnswer,
        'fifth-answer': fifthAnswer,
        'sixth-answer': sixthAnswer,
        'seventh-answer': seventhAnswer,
    };
    fetch("/assessment", {
        method: "POST",
        headers: {'Content-Type': 'application/json'}, 
        body: JSON.stringify(data)
    }).then(res => {
        window.location.replace('/backToMain');
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
        document.getElementById('title').textContent = 'Guardando teste...'
    }
}