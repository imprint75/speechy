var record = document.getElementById('record');
var stop = document.getElementById('stop');
var audio = document.querySelector('audio');
var recordVideo = document.getElementById('record-video');
var preview = document.getElementById('preview');
var container = document.getElementById('container');
var isFirefox = !!navigator.mozGetUserMedia;
var recordAudio, recordVideo, fileName;

function PostBlob(audioBlob, videoBlob, fileName) {
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
    console.log( "success" );
  }).fail(function(jqXHR, textStatus, errorThrown) {
    console.log( "error" );
  }).always(function(jqXHR, textStatus, errorThrown) {
    console.log( "complete" );
  });
}

record.onclick = function() {
  record.disabled = true;
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
    preview.src = window.URL.createObjectURL(stream);
    preview.play();
    preview.muted = true;
    recordAudio = RecordRTC(stream, {
      // bufferSize: 16384,
      onAudioProcessStarted: function() {
        if (!isFirefox) {
          recordVideo.startRecording();
        }
      }
    });
    recordVideo = RecordRTC(stream, {
      type: 'video'
    });
    recordAudio.startRecording();
    stop.disabled = false;
  }
};

stop.onclick = function() {
  document.querySelector('h1').innerHTML = 'Getting Blobs...';
  record.disabled = false;
  stop.disabled = true;
  preview.src = '';
  preview.poster = 'ajax-loader.gif';
  fileName = Math.round(Math.random() * 99999999) + 99999999;
  if (!isFirefox) {
    recordAudio.stopRecording(function() {
      document.querySelector('h1').innerHTML = 'Got audio-blob. Getting video-blob...';
      recordVideo.stopRecording(function() {
        document.querySelector('h1').innerHTML = 'Uploading to server...';
        PostBlob(recordAudio.getBlob(), recordVideo.getBlob(), fileName);
      });
    });
  }
};
