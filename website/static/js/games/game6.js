URL = window.URL || window.webkitURL;

var gumStream; 						//stream from getUserMedia()
var rec; 							//Recorder.js object
var input; 							//MediaStreamAudioSourceNode we'll be recording

// shim for AudioContext when it's not avb. 
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext //audio context to help us record

function setPermission() {
    try {
    navigator.permissions.query({name: 'microphone'}).then(function (result) {
        document.getElementsByTagName('p')[1].textContent = 'Grave a sua voz para cada uma das letras pedidas.';
        if (result.state == 'granted') {
            // Do nothing and keep opened
            //navigator.mediaDevices.getUserMedia({audio: true}).then(stream => { handlerFunction(stream) });
        } else if (result.state == 'prompt') {
            navigator.mediaDevices.getUserMedia({ audio: true })
            .then(_ => {
                navigator.mediaDevices.getUserMedia({audio: true}).then(stream => { handlerFunction(stream) });
            })
            .catch(_ => {
                document.getElementsByTagName('p')[0].textContent = 'Sem permissões de microfone.';
                document.getElementsByTagName('p')[0].textContent = 'Voltando ao menu inicial...';
                document.getElementById('option-div').style.display = 'none';
                setTimeout(_ => {
                    window.location.replace('/backToMain');
                }, 5000)
            });

        } else if (result.state == 'denied') {
            document.getElementsByTagName('p')[0].textContent = 'Sem permissões de microfone.';
            document.getElementsByTagName('p')[0].textContent = 'Voltando ao menu inicial...';
            document.getElementById('option-div').style.display = 'none';
            setTimeout(_ => {
                window.location.replace('/backToMain');
            }, 5000)
        };
    });
    } catch(_) {
        document.getElementsByTagName('p')[0].textContent = 'Jogo não disponível para este dispositivo.';
        document.getElementsByTagName('p')[1].textContent = 'Voltando ao menu inicial...';
        document.getElementById('option-div').style.display = 'none';
        setTimeout(_ => {
            window.location.replace('/backToMain');
        }, 5000)
    }
}
setPermission();

function startRecording() {

    var constraints = { audio: true, video:false }

 	/*
    	Disable the record button until we get a success or fail from getUserMedia() 
	*/

	/*
    	We're using the standard promise based getUserMedia() 
    	https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia
	*/

	navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
		/*
			create an audio context after getUserMedia is called
			sampleRate might change after getUserMedia is called, like it does on macOS when recording through AirPods
			the sampleRate defaults to the one set in your OS for your playback device
		*/
		audioContext = new AudioContext();
        console.log(1)
		//update the format 
        console.log(audioContext.sampleRate)
        console.log(2)
		/*  assign to gumStream for later use  */
		gumStream = stream;
		console.log(3)
		/* use the stream */
		input = audioContext.createMediaStreamSource(stream);
        console.log(4)
		/* 
			Create the Recorder object and configure to record mono sound (1 channel)
			Recording 2 channels  will double the file size
		*/
		rec = new Recorder(input,{numChannels:1})
        console.log(5)
		//start the recording process
		rec.record()
        console.log(6)

	}).catch(function(err) {
	  	//enable the record button if getUserMedia() fails
    	console.log(err)
        //window.location.replace('/backToMain');
	});
}

function stopRecording() {
	console.log("stopButton clicked");
	
	//tell the recorder to stop the recording
	rec.stop();

	//stop microphone access
	gumStream.getAudioTracks()[0].stop();

	//create the wav blob and pass it on to createDownloadLink
	rec.exportWAV(createDownloadLink);
}

function createDownloadLink(blob) {
	
	var url = URL.createObjectURL(blob);

	//name of .wav file to use during upload and download (without extendion)
	var filename = new Date().toISOString();

	//upload link
	var fd=new FormData();
	fd.append("audio_data",blob, filename);

    fetch("/game", {
        method: "POST",
        cache: "no-cache",
        body: fd
    }).then(res => {
        //window.location.replace('/');
    });

}

let recording = false;
document.getElementById('record').onclick = e => {
    audioChunks = [];
    if (!recording) {
        startRecording()
        document.getElementById('record').textContent = 'Gravando';
        document.getElementById('record').style.backgroundColor = 'rgb(207, 72, 62)';
        setTimeout(function () { // Parar ao fim de 5.5 segundos
            stopRecording();
            document.getElementById('record').textContent = 'Guardando';
            document.getElementById('record').style.backgroundColor = '#5995fd';
        }, 5500);
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