let ptt = false; // Define your PTT (push-to-talk) state here
let context;
let downsamplingNode;
let source;
let stream;
let wsa = new WebSocket(wsType+window.location.host+"/wsa");
wsa.binaryType = 'arraybuffer';

async function openMicrophone() {

    // Create an AudioWorkletNode to handle the audio processing
    context = new AudioContext();
    await context.audioWorklet.addModule('static/js/downsampling-processor.js');
    let downsamplingNode = new AudioWorkletNode(context, 'downsampling-processor');
    // Send sample rate to the server
    wsa.send(JSON.stringify({ "sampleRate": context.sampleRate }));

    // Request access to the microphone
    stream = await navigator.mediaDevices.getUserMedia({
        video: false,
        audio: true
    });

    // Listen for messages from the AudioWorkletProcessor
    downsamplingNode.port.onmessage = (event) => {
        if (ptt) {
            wsa.send(event.data);
        }
    };

    // Create a media stream source from the microphone input
    source = context.createMediaStreamSource(stream);
    source.connect(downsamplingNode);
    downsamplingNode.connect(context.destination);
}

function closeMicrophone() {
    if (stream) {
        // Stop all tracks in the stream to stop the microphone
        stream.getTracks().forEach(track => track.stop());
    }

    if (source) {
        source.disconnect();
    }

    if (downsamplingNode) {
        downsamplingNode.disconnect();
    }

    if (context) {
        context.close();
    }
}

// Function to toggle the PTT state
function togglePTT() {
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
}
