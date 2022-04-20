let delay = 3;
let randomNumber = Math.random();
let timerTapSeconds = Math.floor(randomNumber*10);
let timerTapMiliseconds = Math.floor((randomNumber*10 - timerTapSeconds) * 1000);
let totalTimer = (timerTapSeconds+delay)*1000 + timerTapMiliseconds; // in miliseconds
console.log(totalTimer);


function changeColor() {
    document.querySelector('.jogo').style.background = '#f00';
    startCounting();   
}

setTimeout(changeColor, totalTimer);

// =====================================================================

var inGame = true;

function updateTimer(starterTimer) {
    if (inGame) {
        let now = new Date();
        let currentTimer = now.getTime();
        let difference = (currentTimer - starterTimer) / 1000;
        let differenceDecimals = Math.floor(difference*10) / 10;
        let numberInString = differenceDecimals.toString();
        let arrayNumbers = numberInString.split('.');
        if (arrayNumbers.length === numberInString.length) {
            numberInString += '.0'
        }
        document.querySelector('.timer').textContent = numberInString;
    }
}

function startCounting() {
    let now = new Date();
    let starterTimer = now.getTime();
    setInterval(function() { updateTimer(starterTimer); }, 10);
}

var divJogo = document.getElementById('jogo_div');
divJogo.onclick = function() {
    inGame = false;
    setTimeout(function() { window.location.replace('/login'); }, 5000) // voltar ao menu principal
}

