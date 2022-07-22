var gumStream; 						//stream from getUserMedia()
var rec; 							//Recorder.js object
var input; 							//MediaStreamAudioSourceNode we'll be recording

// shim for AudioContext when it's not avb. 
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext //audio context to help us record

function endGamePermissions() {
    document.getElementsByTagName('p')[0].textContent = 'Sem permissões de microfone.';
    document.getElementsByTagName('p')[0].textContent = 'Voltando ao menu inicial...';
    document.getElementById('option-div').style.display = 'none';
    setTimeout(_ => {
        window.location.replace('/backToMain');
    }, 5000)
}

function setPermission() {
    try {
        navigator.permissions.query({name: 'microphone'}).then(function (result) {
            document.getElementsByTagName('p')[1].textContent = 'Grave a sua voz para cada uma das letras pedidas.';
            if (result.state == 'granted') {
                // Do nothing and keep opened
            } else if (result.state == 'prompt') {
                navigator.mediaDevices.getUserMedia({ audio: true })
                .then(_ => {
                    // Do nothing and keep opened
                })
                .catch(_ => {
                    endGamePermissions();
                });

            } else if (result.state == 'denied') {
                endGamePermissions();
            };
        });
    } catch(_) {
        endGamePermissions();
    }
}
setPermission();

function startRecording() {

    var constraints = { audio: true, video:false }

	navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {

		audioContext = new AudioContext();
		/*  assign to gumStream for later use  */
		gumStream = stream;
		/* use the stream */
		input = audioContext.createMediaStreamSource(stream);
		/* 
			Create the Recorder object and configure to record mono sound (1 channel)
			Recording 2 channels  will double the file size
		*/
		rec = new Recorder(input,{numChannels:1})
		//start the recording process
		rec.record()

	}).catch(function(err) {
	  	//enable the record button if getUserMedia() fails
    	endGamePermissions();
	});
}

function stopRecording() {
	
	//tell the recorder to stop the recording
	rec.stop();
	//stop microphone access
	gumStream.getAudioTracks()[0].stop();

	//create the wav blob and pass it on to createDownloadLink
	rec.exportWAV(createDownloadLink);
}

function createDownloadLink(blob) {
	
	//name of .wav file to use during upload and download (without extendion)
	var filename = new Date().toISOString();

	// create form
	var fd=new FormData();
	fd.append("audio_data",blob, filename);
    // send request
    fetch("/game", {
        method: "POST",
        body: fd
    }).then(res => {
        setTimeout(() => {
            window.location.replace('/');
        }, 2000);
    });
}

let recording = false;
document.getElementById('record').onclick = e => {
    if (!recording) {
        startRecording()
        document.getElementById('record').textContent = 'Gravando';
        document.getElementById('record').style.backgroundColor = 'rgb(207, 72, 62)';
        console.log(new Date())
        setTimeout(function () { // Parar ao fim de 5.5 segundos
            stopRecording();
            console.log(new Date())
            document.getElementById('record').textContent = 'Guardando';
            document.getElementById('record').style.backgroundColor = '#5995fd';
        }, 6500);
    }
};

function startGame6() {
    document.getElementsByTagName('p')[1].textContent = 'Diga a letra A continuamente quando começar a gravar.';
    document.getElementById('option-div').style.display = 'none';
    document.getElementById('record-div').style.display = 'flex';
}
    
// Menu inicial
document.getElementById('exit-game').onclick = function() {
    window.location.replace('/backToMain')
}

document.getElementById('start-game').onclick = function(e) {
    e.preventDefault();
    startGame6();
}