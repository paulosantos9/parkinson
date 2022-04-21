let delay = 9.5;
let difference = 0;
let numberInString = '';
let isCountingDown = true;
let counterClicks = 0;
let sentPostWithScore = false;

function updateTimer(starterTimer) {
    let now = new Date();
    let currentTimer = now.getTime();

    if (isCountingDown) {
        if (currentTimer - starterTimer > 0) {
            isCountingDown = false;
        }
    } else {
        if (currentTimer - starterTimer < 0) {
            isCountingDown = true;
        }
    }
    difference = Math.abs((currentTimer - starterTimer) / 1000);
    if (difference >= 10) {
        difference = 10;
        setTimeout(sendPostWithScore, 3000);
    }
    let differenceDecimals = Math.floor(difference*10) / 10;
    numberInString = differenceDecimals.toString();
    let arrayNumbers = numberInString.split('.');
    if (arrayNumbers.length === numberInString.length) {
        numberInString += '.0'
    }
    if (isCountingDown) {
        document.querySelector('.timer').textContent = numberInString + ' s';
    } else {
        document.querySelector('.timer').textContent = 'Clicks ' + counterClicks + ' - ' + numberInString + ' s';
        document.querySelector('.timer').style.fontSize = "1.5em";
        document.querySelector('.jogo').style.background = '#BD780A';
    }
}

function sendPostWithScore() {
    if (sentPostWithScore == false) {
        sentPostWithScore = true;
        let data = {'score': counterClicks, 'gameType': 2};
        fetch("/game", {
            method: "POST",
            headers: {'Content-Type': 'application/json'}, 
            body: JSON.stringify(data)
        }).then(res => {
            window.location.replace('/');
        });
    }
}

function cyclic() {
    let now = new Date();
    let countdownTime = new Date(now.getTime() + delay*1000); // 10 segundos depois
    if (difference == 10 && isCountingDown == false) {
        
    } else {
        
    }
    setInterval(function() { updateTimer(countdownTime); }, 10);
}

cyclic();

function addCounter() {
    if (isCountingDown == false && difference < 10) {
        counterClicks++;
    }
}

var divJogo = document.getElementById('jogo_div');
divJogo.onclick = addCounter;