let delay = 3;
let randomNumber = Math.random();
let timerTapSeconds = Math.floor(randomNumber*10);
let timerTapMiliseconds = Math.floor((randomNumber*10 - timerTapSeconds) * 1000);
let totalTimer = (timerTapSeconds+delay)*1000 + timerTapMiliseconds; // in miliseconds
let difference = 0;
let numberInString = '';


function changeColor() {
    document.querySelector('.jogo').style.background = '#BD780A';
    startCounting();   
}

setTimeout(changeColor, totalTimer);

// =====================================================================

var inGame = false;

function updateTimer(starterTimer) {
    if (inGame) {
        let now = new Date();
        let currentTimer = now.getTime();
        difference = (currentTimer - starterTimer) / 1000;
        if (difference >= 10) {
            difference = 10;
            let differenceDecimals = Math.floor(difference*10) / 10;
            numberInString = differenceDecimals.toString();
            endGame();
        } else {
            let differenceDecimals = Math.floor(difference*10) / 10;
            numberInString = differenceDecimals.toString();
            let arrayNumbers = numberInString.split('.');
            if (arrayNumbers.length === numberInString.length) {
                numberInString += '.0'
            }
            document.querySelector('.timer').textContent = numberInString + ' s';
        }
    }
}

function startCounting() {
    let now = new Date();
    let starterTimer = now.getTime();
    inGame = true;
    setInterval(function() { updateTimer(starterTimer); }, 10);
}

function sendPostWithScore() {
    let data = {'score': difference*1000, 'gameType': 1};
    fetch("/game", {
        method: "POST",
        headers: {'Content-Type': 'application/json'}, 
        body: JSON.stringify(data)
    }).then(res => {
        window.location.replace('/');
    });
}

function endGame() {
    if (inGame) {
        inGame = false;
        document.querySelector('.timer').style.fontSize = "1.2em";
        document.querySelector('.timer').textContent = 'Guardando resultado: ' + numberInString + ' s';
        setTimeout(sendPostWithScore, 3000); // voltar ao menu principal
    }
}

var divJogo = document.getElementById('jogo_div');
divJogo.onclick = endGame;

