let wsspeak = new WebSocket(wsType+window.location.host+"/wsspeak");
wsspeak.binaryType = 'arraybuffer';
let speakOpen = false;

var AudioContext = window.AudioContext || window.webkitAudioContext
var context = new AudioContext()
var time;

wsspeak.onmessage = function(event){
    message = JSON.parse(event.data);
    console.log(message);
}


function connect(){
    time = 0

    wsspeak.onopen = function(){
        document.getElementById("conn").innerHTML=status_on;
        var evt = {"event": "connect", "id" : "test"};
        console.log(JSON.stringify(evt));
        wsspeak.send(JSON.stringify(evt));
        console.log('connected');
    }
    wsspeak.onclose = function(){
        document.getElementById("conn").innerHTML=status_off;
        console.log('disconnected');
        con_btn.innerText = 'Connect';
        con_btn.onclick = function () { connect()};
        ptt_btn.disabled = true;
    }

    wsspeak.onmessage = function(event){
        time = Math.max(context.currentTime, time)
        var input = new Int16Array(event.data)
        if(input.length) {
            var buffer = context.createBuffer(1, input.length, 16000)
            var data = buffer.getChannelData(0)
            for (var i = 0; i < data.length; i++) {
            data[i] = input[i] / 32767
            }
            var source = context.createBufferSource()
            source.buffer = buffer
            source.connect(context.destination)
            source.start(time += buffer.duration)
        }
    }
}

function pttChange(){
    ptt = !ptt;
    if(!ptt){
        wsspeak.send(JSON.stringify({"goOn":true}));
        $("#speakBtn").css("color", "#3b7991");
        $("#speakBtn").css("background-color", "#b7d5e1");
    }
    else{
        $("#speakBtn").css("color", "#b7d5e1");
        $("#speakBtn").css("background-color", "#3b7991");
    }
    console.log($("#speakBtn"));
}
