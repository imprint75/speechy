var record = document.getElementById('record');
var stop = document.getElementById('stop');
var audio = document.querySelector('audio');
var container = document.getElementById('container');
var isFirefox = !!navigator.mozGetUserMedia;
var recordAudio, fileName;

function PostBlob(audioBlob, fileName) {
  var formElement = $("#xsrf").serializeArray();
  var formData = new FormData();
  formData.append('filename', fileName);
  formData.append(formElement[0]['name'], formElement[0]['value']);
  formData.append('file1', audioBlob);
  $.ajax({
    url: '/upload',
    cache: false,
    contentType: false,
    data: formData,
    processData: false,
    type: 'POST'
  }).done(function(jqXHR, textStatus, errorThrown) {
    document.querySelector('h1').innerHTML = 'RecordRTC';
    console.log('Success! I think you said: ' + jqXHR);
    var para = document.createElement("P");
    para.appendChild(document.createTextNode(jqXHR));
    document.querySelector('#recordedText').appendChild(para);
  }).fail(function(jqXHR, textStatus, errorThrown) {
    console.log( "error" );
  }).always(function(jqXHR, textStatus, errorThrown) {
    console.log( "complete" );
  });
}

record.onclick = function() {
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
    alert(JSON.stringify(error, null, '\t'));
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
      PostBlob(recordAudio.getBlob(), fileName);
    });
  }
};
