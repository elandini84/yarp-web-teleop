let wsa = new WebSocket(wsType+window.location.host+"/wsa");
wsa.binaryType = 'arraybuffer';
let micOpen = false;

var ptt=false;
var AudioContext = window.AudioContext || window.webkitAudioContext
var context = new AudioContext()
var time;


function connect(){
    time = 0

    wsa.onopen = function(){
        document.getElementById("conn").innerHTML=status_on;
        var evt = {"event": "connect", "id" : "test"};
        console.log(JSON.stringify(evt));
        wsa.send(JSON.stringify(evt));
        console.log('connected');
    }
    wsa.onclose = function(){
        document.getElementById("conn").innerHTML=status_off;
        console.log('disconnected');
        con_btn.innerText = 'Connect';
        con_btn.onclick = function () { connect()};
        ptt_btn.disabled = true;
    }

    wsa.onmessage = function(event){
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
        wsa.send(JSON.stringify({"goOn":true}));
        $("#speakBtn").css("color", "#3b7991");
        $("#speakBtn").css("background-color", "#b7d5e1");
    }
    else{
        $("#speakBtn").css("color", "#b7d5e1");
        $("#speakBtn").css("background-color", "#3b7991");
    }
    console.log($("#speakBtn"));
}

function openMicrophone(){
    wsa.send(JSON.stringify({"sampleRate": context.sampleRate}));
    navigator.mediaDevices.getUserMedia({
        video: false,
        audio: true
    })
    .then( stream => {
        var source = context.createMediaStreamSource(stream)
        var processor = context.createScriptProcessor(1024, 1, 1)
        var downsampled = new Int16Array(2048)
        var downsample_offset = 0
        function process_samples(){
            while(downsample_offset > audioBufferLen) {
                var output = downsampled.slice(0, audioBufferLen)
                downsampled.copyWithin(0, audioBufferLen)
                downsample_offset -= audioBufferLen
                if(ptt == true) {
                    wsa.send(output.buffer)
                }
            }
        }
        var sampleRatio = context.sampleRate / 16000
        processor.onaudioprocess = (audioProcessingEvent) => {
            var inputBuffer = audioProcessingEvent.inputBuffer
            var outputBuffer = audioProcessingEvent.outputBuffer
            var inputData = inputBuffer.getChannelData(0)
            var outputData = outputBuffer.getChannelData(0)
            for (var i = 0; i < inputData.length; i += sampleRatio) {
                var sidx = Math.floor(i)
                var tidx = Math.floor(i/sampleRatio)
                downsampled[downsample_offset + tidx] = inputData[sidx] * 32767
            }
            downsample_offset += ~~(inputData.length/sampleRatio)
            if(downsample_offset > audioBufferLen) {
                process_samples()
            }
            for (var sample = 0; sample < inputBuffer.length; sample++) {
                // Silence the output
                outputData[sample] = 0
            }
        }
        source.connect(processor)
        processor.connect(context.destination)
    })
}
