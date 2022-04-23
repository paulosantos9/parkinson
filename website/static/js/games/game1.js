let delay = 3;
var randomNumber = Math.random();
var timerTapSeconds = Math.floor(randomNumber*3);
var timerTapMiliseconds = Math.floor((randomNumber*3 - timerTapSeconds) * 1000);
var totalTimer = (timerTapSeconds+delay)*1000 + timerTapMiliseconds; // in miliseconds

function changeColor() {
    document.querySelector('.jogo').style.background = '#BD780A';
    startCounting();   
}

setTimeout(changeColor, totalTimer); // change color after random timer

// =====================================================================
let difference = 0;
let numberInString = '';
let starterTimer;
var inGame = false;

function calculateDifference() {
    let now = new Date();
    let currentTimer = now.getTime();
    difference = currentTimer - starterTimer;
}

function convertToSecondsString() {
    let differenceDecimals = Math.floor(difference/1000*10) / 10;
    numberInString = differenceDecimals.toString();
    let arrayNumbers = numberInString.split('.');
    if (arrayNumbers.length === numberInString.length) {
        numberInString += '.0'
    }
}

function updateTimer() {
    if (inGame) {
        calculateDifference();
        if( difference > 10000) {
            difference = 10000;
        }
        convertToSecondsString();
        if (difference == 10000) {
            endGame();
        } else {
            document.querySelector('.timer').textContent = numberInString + ' s';
        }
    }
}

function sendPostWithScore() {
    let data = {'score': difference, 'gameType': 1};
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
        calculateDifference();
        if( difference > 10000) {
            difference = 10000;
            difference = '10';
        } else {
            difference = difference / 1000;
            difference = difference.toString();
            if (difference.split('.')[1].length !== 3) {
                difference += '0'
            }
        }
        document.querySelector('.timer').style.fontSize = "1.2em";
        document.querySelector('.timer').textContent = 'Guardando resultado: ' + difference + ' s';
        setTimeout(sendPostWithScore, 2000); // voltar ao menu principal
    }
}

function startCounting() {
    let now = new Date();
    starterTimer = now.getTime();
    inGame = true;
    setInterval(function() { updateTimer(); }, 10);
}

document.getElementById('jogo_div').onclick = endGame; // add function to the game div on click

