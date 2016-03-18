var record = document.getElementById('record');
var stop = document.getElementById('stop');
var audio = document.querySelector('audio');
var container = document.getElementById('container');
var progress = document.getElementById('progress');
var isFirefox = !!navigator.mozGetUserMedia;
var recordAudio, fileName;

function pollForUpdates(taskId) {
  var ws = new WebSocket("wss://192.168.33.103/status");
  ws.onopen = function() {
    ws.send(taskId);
  };

  ws.onmessage = function (evt) {
    var p = document.createElement("P");
    p.appendChild(document.createTextNode(evt.data));
    document.querySelector('#recordedText').appendChild(p);
    console.log(evt.data);
    ws.close();
  };
}

function sendFile(formData) {
  var xhr = new XMLHttpRequest();
  xhr.addEventListener("load", transferComplete);
  xhr.upload.addEventListener("progress", updateProgress);
  xhr.upload.addEventListener("error", transferFailed);
  xhr.open('POST', '/upload');
  xhr.send(formData);
}

function transferComplete() {
  document.querySelector('h1').innerHTML = 'RecordRTC';
  progress.classList.toggle('hidden');
  progress.children[0].style.width = '0%';
  pollForUpdates(this.responseText);
}

function updateProgress(oEvent) {
  if (oEvent.lengthComputable) {
    var percentComplete = (oEvent.loaded / oEvent.total) * 100;
    progress.children[0].style.width = Math.ceil(percentComplete) + '%';
  } else {
    // Unable to compute progress information since the total size is unknown
    console.log( "updateProgress:: error..." );
  }
}

function transferFailed() {
  console.log( "transferFailed:: error" );
}

function postBlob(audioBlob, fileName) {
  var formData = new FormData();
  formData.append('filename', fileName);
  var xsrfForm = document.getElementById("xsrf").elements;
  formData.append(xsrfForm['_xsrf'].name, xsrfForm['_xsrf'].value);
  formData.append('file1', audioBlob);
  sendFile(formData);
}

record.onclick = function() {
  progress.classList.toggle('hidden');
  record.disabled = true;
  if(window.stream){
    delete window.stream;
  }
  !window.stream && navigator.getUserMedia({
    audio: true,
    video: false
  }, function(stream) {
    window.stream = stream;
    onstream();
  }, function(error) {
    console.log(JSON.stringify(error, null, '\t'));
  });
  window.stream && onstream();
  function onstream() {
    recordAudio = RecordRTC(stream, {
      // bufferSize: 16384,
      onAudioProcessStarted: function() {
        if (!isFirefox) {
          document.querySelector('h1').innerHTML = 'Recording...';
        }
      }
    });
    recordAudio.startRecording();
    stop.disabled = false;
  }
};

stop.onclick = function() {
  record.disabled = false;
  stop.disabled = true;
  fileName = Math.round(Math.random() * 99999999) + 99999999;
  if (!isFirefox) {
    recordAudio.stopRecording(function() {
      window.stream.getAudioTracks().forEach(function(track){track.stop();});
      document.querySelector('h1').innerHTML = 'Got audio...';
      postBlob(recordAudio.getBlob(), fileName);
    });
  }
};
