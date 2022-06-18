function setPermission() {
    navigator.permissions.query({name: 'microphone'}).then(function (result) {
        document.getElementsByTagName('p')[1].textContent = 'Grave a sua voz para cada uma das letras pedidas.';
        if (result.state == 'granted') {
            // Do nothing and keep opened
            navigator.mediaDevices.getUserMedia({audio: true}).then(stream => { handlerFunction(stream) });
        } else if (result.state == 'prompt') {
            navigator.mediaDevices.getUserMedia({ audio: true })
            .then(_ => {
                document.getElementsByTagName('p')[1].textContent = 'Grave a sua voz para cada uma das letras pedidas.';
                navigator.mediaDevices.getUserMedia({audio: true}).then(stream => { handlerFunction(stream) });
            })
            .catch(_ => {
                document.getElementsByTagName('p')[0].textContent = 'Sem permissões de microfone.';
                document.getElementsByTagName('p')[0].textContent = 'Voltando ao menu inicial...';
                document.getElementById('start-game').style.display = 'none';
                document.getElementById('exit-game').style.display = 'none';
                setTimeout(_ => {
                    window.location.replace('/backToMain');
                }, 5000)
            });

        } else if (result.state == 'denied') {
            document.getElementsByTagName('p')[0].textContent = 'Sem permissões de microfone.';
            document.getElementsByTagName('p')[0].textContent = 'Voltando ao menu inicial...';
            document.getElementById('start-game').style.display = 'none';
            document.getElementById('exit-game').style.display = 'none';
            setTimeout(_ => {
                window.location.replace('/backToMain');
            }, 5000)
        };
    });
}
setPermission();

function handlerFunction(stream) {
    rec = new MediaRecorder(stream);
    rec.ondataavailable = e => {
        audioChunks.push(e.data);
        if (rec.state == "inactive") {
            let blob = new Blob(audioChunks, {type: 'audio/mp3'});
            sendData(blob);
        }
    }
}

function sendData(data) {
    var reader = new FileReader();
    reader.readAsDataURL(data)
    reader.onloadend = function() {
        var base64data = reader.result;
        let data = {'gameType': 6, 'audio': base64data};
        fetch("/game", {
            method: "POST",
            headers: {'Content-Type': 'application/json'}, 
            body: JSON.stringify(data)
        }).then(res => {
            window.location.replace('/');
        });
    }
}

let recording = false;
document.getElementById('record').onclick = e => {
    audioChunks = [];
    if (!recording) {
        rec.start();
        recording = true;
    }
    document.getElementById('record').textContent = 'Gravando';
    document.getElementById('record').style.backgroundColor = 'rgb(207, 72, 62)';
    setTimeout(function () { // Parar ao fim de 5 segundos
        rec.stop();
        document.getElementById('record').textContent = 'Guardando';
        document.getElementById('record').style.backgroundColor = '#5995fd';
    }, 5000);
};

function startGame6() {
    document.getElementsByTagName('p')[1].textContent = 'Diga a letra A continuamente quando começar a gravar.';
    document.getElementById('start-game').style.display = 'none';
    document.getElementById('exit-game').style.display = 'none';
    document.getElementById('container').style.display = 'block';
}
    
// Menu inicial
document.getElementById('exit-game').onclick = function() {
    window.location.replace('/backToMain')
}

document.getElementById('start-game').onclick = function(e) {
    e.preventDefault();
    startGame6();
}