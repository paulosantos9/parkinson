let cardsAvailable = [
    true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true
];
let indexCounter = 0;

function randomizeCards() {
    let randomizedArray = Array.from({length:16},(v,k)=>k+1);
    randomizedArray.sort(() => 0.5 - Math.random());
    let lettersAvailable = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
    let lettersBoard = [];
    for (let i = 0; i < randomizedArray.length; i++) {
        lettersBoard.push(lettersAvailable[ randomizedArray[i] % 8 ]);
    }
    return lettersBoard;
}

function fillBoard() {
    let randomLetters = randomizeCards();
    for (let i = 0; i < randomLetters.length; i++) {
        let card = document.getElementsByClassName('cell')[i].children[0];
        let cellContent = card.children[0];
        cellContent.textContent = randomLetters[i];
    }
}

fillBoard();

function checkIfPair() {
    return cardTapped[0].textContent === cardTapped[1].textContent;
}

function checkIfOver() {
    let numberOfCells = 16;
    for (let i = 0; i < numberOfCells; i++) {
        if (document.getElementsByClassName('cell-content')[i].style.color === 'aqua' || document.getElementsByClassName('cell-content')[i].style.color === '') {
            return false;
        }
    }
    return true;
}

function sendPostWithScore() {
    let data = {'score': tries, 'gameType': 3};
    fetch("/game", {
        method: "POST",
        headers: {'Content-Type': 'application/json'}, 
        body: JSON.stringify(data)
    }).then(res => {
        window.location.replace('/');
    });
}

function checkIfCardTurned() {

}

function cardClicked() {   
    tapCounter++;
    if (tapCounter !== 3) {
        let card = this.children[0];
        let cellContent = card.children[0];
        if ( cellContent.style.color !== 'black') {
            cellContent.style.color = 'black';
            cardTapped.push(card.children[0])
            if (tapCounter === 2) {
                if ( checkIfPair() === true) { // If cards are the same reset counters
                    // If win end game
                    if ( checkIfOver() ) {
                        setTimeout(sendPostWithScore, 2000); // voltar ao menu principal
                    }
    
                    // reset variables
                    tapCounter = 0;
                    tries++;
                    if (checkIfOver()) {
                        document.getElementsByTagName('h2')[0].innerText = 'Guardando resultado:\n' + tries + ' tentativas';
                    } else {
                        document.getElementsByTagName('h2')[0].innerText = 'Tentativas: ' + tries;
                    }
                    cardTapped.pop();
                    cardTapped.pop();    
                }
            }
        } else {
            tapCounter--;
        }
    } else {
        
        // reset turned cards if needed
        if ( checkIfPair() === false) {
            cardTapped[0].style.color = 'aqua';
            cardTapped[1].style.color = 'aqua';      
        }

        // reset variables
        tries++;
        if (checkIfOver()) {
            document.getElementsByTagName('h2')[0].innerText = 'Guardando resultado:\n' + tries + ' tentativas';
        } else {
            document.getElementsByTagName('h2')[0].innerText = 'Tentativas: ' + tries;
        }        cardTapped.pop();
        cardTapped.pop();
        tapCounter = 0;
    }
}

function setListeners() {
    let numberOfCells = 16;
    for (let i = 0; i < numberOfCells; i++) {
        document.getElementsByClassName('cell')[i].onclick = cardClicked;
    }
}

setListeners();

let cardTapped = [];
let tapCounter = 0;
let tries = 0;

document.getElementById('start-game').onclick = function() {
    document.getElementById('start-game').style.display = 'none';
    document.getElementById('content').style.display = 'block';
    document.getElementsByTagName('h2')[0].style.display = 'block';
}
