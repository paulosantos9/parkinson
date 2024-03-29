// Defining variables
var delay = 3;
var randomNumber = Math.random();
var timerTapSeconds = Math.floor(randomNumber*3);
var timerTapMiliseconds = Math.floor((randomNumber*3 - timerTapSeconds) * 1000);
var totalTimer = (timerTapSeconds+delay)*1000 + timerTapMiliseconds;
let difference = 0;
let numberInString = '';
let starterTimer;
var inGame = false;
let timeSpent = 0;

document.getElementById('jogo_div').onclick = endGame; // add function to the game div on click

// Setting up functions

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

function sendPostWithScore() {
    let data = {'score': difference, 'gameType': 1, 'timeSpent': timeSpent};
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
        let now = new Date();
        timeSpent = (now.getTime() - starterTimer)/1000;
        calculateDifference();
        if( difference > 10000) {
            difference = 10000;
            numberInString = '10';
        } else {
            convertToSecondsString();
            if (numberInString.split('.')[1] !== undefined) {
                if (numberInString.split('.')[1].length !== 3) {
                    numberInString += '0'
                }
            } else {
                numberInString += '.0'
            }
        }
        numberInString = (difference / 1000).toString();
        if (numberInString.split('.')[1] !== undefined) {
            while (numberInString.split('.')[1].length !== 3) {
                numberInString += '0'
            }
        } else {
            numberInString += '.000'
        }
        document.getElementById('pre-game').style.backgroundColor = 'rgb(255,255,255)';
        document.getElementById('container').style.display = 'none';
        document.getElementById('title').textContent = 'Guardando teste...';
        for (let i = 0; i < document.getElementsByTagName('p').length; i++) document.getElementsByTagName('p')[i].style.display = 'none';
        
        setTimeout(sendPostWithScore, 2000); // voltar ao menu principal
    }
}

function updateTimer() {
    if (inGame) {
        calculateDifference();
        convertToSecondsString();
        if (difference > 10000) {
            endGame();
        } else {
            document.querySelector('.timer').textContent = numberInString + ' s';
        }
    }
}

function startCounting() {
    let now = new Date();
    starterTimer = now.getTime();
    inGame = true;
    setInterval(function() { updateTimer(); }, 10);
}

function changeColor() {
    document.querySelector('.jogo').style.background = '#BD780A';
    startCounting();   
}

function startGame() {
    setTimeout(changeColor, totalTimer); // change color and start game
}

document.getElementById('exit-game').onclick = function() {
    window.location.replace('/choose_game')
}

document.getElementById('start-game').onclick = function() {
    document.getElementById('start-game').style.display = 'none';
    document.getElementById('exit-game').style.display = 'none';
    document.getElementById('container').style.display = 'block';
    startGame();
}