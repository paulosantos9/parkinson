function sendPostWithScore(score) {
    let now = new Date();
    timeSpent = (now.getTime() - startTime)/1000;
    if (timeSpent > 10) timeSpent = 10;
    let data = {'score': score, 'gameType': 5, 'timeSpent': timeSpent};
    fetch("/game", {
        method: "POST",
        headers: {'Content-Type': 'application/json'}, 
        body: JSON.stringify(data)
    }).then(res => {
        window.location.replace('/backToMain');
    });
}

function updateFieldIfNotNull(fieldName, value){
    if (value != null) document.getElementById(fieldName).innerHTML = 'Pontos: ' + rotationSum;
}

function handleOrientation(event) { // Orientação X, Y e Z em graus
    updateFieldIfNotNull('value_a', event.alpha);
    updateFieldIfNotNull('value_b', event.beta);
    updateFieldIfNotNull('value_c', event.gamma);
}

function handleAccelerometer(event) {
    accelerationSum += Math.floor(
        Math.abs(event.acceleration.x),
        Math.abs(event.acceleration.y),
        Math.abs(event.acceleration.z)
    );
    updateFieldIfNotNull('value_a', accelerationSum);
    //updateFieldIfNotNull('value_a', event.acceleration.x);
    //updateFieldIfNotNull('value_b', event.acceleration.y);
    //updateFieldIfNotNull('value_c', event.acceleration.z);
}

function handleAccelerometerIncludingGravity(event) {
    updateFieldIfNotNull('value_a', event.accelerationIncludingGravity.x);
    updateFieldIfNotNull('value_b', event.accelerationIncludingGravity.y);
    updateFieldIfNotNull('value_c', event.accelerationIncludingGravity.z);
}

function handleGyroscope(event) {
    rotationSum -= Math.floor(
        Math.abs(event.rotationRate.alpha),
        Math.abs(event.rotationRate.beta),
        Math.abs(event.rotationRate.gamma)
    );
    if (rotationSum < 0) {
        rotationSum = 0;
        inGame = false;
        document.getElementById('pre-game').style.backgroundColor = 'rgb(255,255,255)';
        sendPostWithScore(rotationSum);
    }
    updateFieldIfNotNull('counter', rotationSum);
    //updateFieldIfNotNull('value_a', event.rotationRate.alpha);
    //updateFieldIfNotNull('value_b', event.rotationRate.beta);
    //updateFieldIfNotNull('value_c', event.rotationRate.gamma);
}

function handleMotion(event) {
    if (inGame) {
        //handleAccelerometer(event);
        //handleAccelerometerIncludingGravity(event);
        handleGyroscope(event);
    }
}

// Prepare game
function calculateDifference() {
    let now = new Date();
    let currentTimer = now.getTime();
    difference = currentTimer - startTime;
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
        convertToSecondsString();
        if (difference > 10000) {
            inGame = false;
            difference = 10000;
            document.getElementById('container').style.display = 'none';
            document.getElementById('title').textContent = 'Guardando teste...';
            document.getElementsByTagName('p')[0].style.display = 'none';
            document.getElementsByTagName('p')[1].style.display = 'none';
            if (document.getElementsByTagName('p')[2]) {
                document.getElementsByTagName('p')[2].style.display = 'none';
            }
            document.getElementById('pre-game').style.backgroundColor = 'rgb(255,255,255)'
            sendPostWithScore(rotationSum);
        } else {
            document.querySelector('#timer').textContent = numberInString + ' s';
        }
    } else {
        document.getElementById('container').style.display = 'none';
        document.getElementById('title').textContent = 'Guardando teste...';
        document.getElementsByTagName('p')[0].style.display = 'none';
        document.getElementsByTagName('p')[1].style.display = 'none';
        if (document.getElementsByTagName('p')[2]) {
            document.getElementsByTagName('p')[2].style.display = 'none';
        }
    }
}

function startGame() {
    document.getElementById('start-game').style.display = 'none';
    document.getElementById('exit-game').style.display = 'none';
    document.getElementById('container').style.display = 'block';
    inGame = true;
    rotationSum = 10000;
    window.addEventListener("devicemotion", handleMotion);
    //window.addEventListener("deviceorientation", handleOrientation);
    startTime = new Date();
    startTime = startTime.getTime()
    setInterval(updateTimer, 100);
}

let accelerationSum = 10000;
let rotationSum = 10000;
let inGame = false;
let startTime;

let startGameButton = document.getElementById("start-game");
startGameButton.onclick = function(e) {
    e.preventDefault();
    
    // Request permission for iOS 13+ devices
    if (
      DeviceMotionEvent &&
      typeof DeviceMotionEvent.requestPermission === "function"
    ) {
      DeviceMotionEvent.requestPermission()
      .then(permissionState => {
        if (permissionState === 'granted') {
            startGame();
        } else {
            window.location.replace('/backToMain');
        }
        })
        .catch(_ => {
            window.location.replace('/backToMain');
        });
    }

    startGame();
  };

// Menu inicial
document.getElementById('exit-game').onclick = function() {
    window.location.replace('/backToMain')
}