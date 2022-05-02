// Defining variables
var delay = 5;
var maxTime = 10;
let difference = 0;
let numberInString = '';
let isCountingDown = true;
let counterClicks = 0;
let sentPostWithScore = false;

// Function needed

function sendPostWithScore() {
    sentPostWithScore = true;
    let data = {'score': counterClicks, 'gameType': 2};
    fetch("/game", {
        method: "POST",
        headers: {'Content-Type': 'application/json'}, 
        body: JSON.stringify(data)
    }).then(res => {
        window.location.replace('/backToMain');
    });
}

function updateTimer(starterTimer) {
    if (sentPostWithScore == false) {
        let now = new Date();
        let currentTimer = now.getTime();

        if (isCountingDown) {
            if (currentTimer - starterTimer > 0) { isCountingDown = false; }
        } else {
            if (currentTimer - starterTimer < 0) { isCountingDown = true; }
        }
        difference = Math.abs((currentTimer - starterTimer) / 1000);
        if (difference >= maxTime & isCountingDown == false) { // finish
            difference = maxTime;
            sentPostWithScore = true;
            setTimeout(sendPostWithScore, 3000);
        }
        let differenceDecimals = Math.floor(difference*10) / 10;
        numberInString = differenceDecimals.toString();
        let arrayNumbers = numberInString.split('.');
        if (arrayNumbers.length === numberInString.length) {
            numberInString += '.0'
        }
        if (isCountingDown === false) {
            document.querySelector('.timer').textContent = 'Cliques ' + counterClicks + ' - ' + numberInString + ' s';
            document.querySelector('.timer').style.fontSize = "1.5em";
            document.querySelector('.jogo').style.background = '#BD780A';
        }
        
        if (sentPostWithScore == true) {
            document.getElementById('container').style.display = 'none';
            document.getElementById('title').textContent = 'Guardando teste...';
            document.getElementsByTagName('p')[0].style.display = 'none';
        }
    }
}

function startGame() {
    let now = new Date();
    let countdownTime = new Date(now.getTime() + delay*1000); // segundos para milissegundos
    setInterval(function() { updateTimer(countdownTime); }, 10);
}

document.getElementById('exit-game').onclick = function() {
    window.location.replace('/backToMain')
}

document.getElementById('start-game').onclick = function() {
    document.getElementById('start-game').style.display = 'none';
    document.getElementById('exit-game').style.display = 'none';
    document.getElementById('container').style.display = 'block';
    startGame();
}

var divJogo = document.getElementById('jogo_div').onclick = function() {
    if (isCountingDown == false && difference < maxTime) {
        counterClicks++;
    }   
};