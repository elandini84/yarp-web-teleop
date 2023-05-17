let wsa = new WebSocket(wsType+window.location.host+"/wsa");
wsa.binaryType = 'arraybuffer';
let micOpen = false;

class Recorder {
    constructor(source) {
        const audioContext = source.context;
        const processor = audioContext.createScriptProcessor(2048, 1, 1);
        processor.connect(audioContext.destination);
        source.connect(processor);
        this.audioContext = audioContext;
        this.processor = processor;
        this.buffer = [];
        this.counter = 0;
    }

    record() {
        this.processor.onaudioprocess = e => {
            this.buffer.push(e.inputBuffer.getChannelData(0));
        };
    }

    stop() {
        this.processor.onaudioprocess = null;
    }

    getAudio() {
        const buffer = this.buffer.reduce((acc, val) => acc.concat(val), []);
        const arrayBuffer = new ArrayBuffer(buffer.length * 2);
        const view = new DataView(arrayBuffer);
        buffer.forEach((val, i) => {
            view.setInt16(i * 2, val * 0x7fff, true);
        });
        window.alert(this.audioContext.sampleRate);
        return arrayBuffer;
    }

    getSampleRate() {
        return this.audioContext.sampleRate;
    }
}

function openMicrophone(){
    if(micOpen) return;
    navigator.mediaDevices.getUserMedia({ audio: true })
    .then(stream => {
        const audioContext = new AudioContext();
        const input = audioContext.createMediaStreamSource(stream);
        const recorder = new Recorder(input);
        console.log("El microfono esta abierto");

        document.getElementById("shoutBtn").addEventListener("click", () => {
            console.log("El microfono esta aquisiendo");
            recorder.record();
        });

        document.getElementById("quietBtn").addEventListener("click", () => {
            recorder.stop();

            var audio = recorder.getAudio();
            console.log(audio);
            var marco = {"data": audio, "sampleRate": recorder.getSampleRate()};
            //wsa.send(JSON.stringify(marco));
            wsa.send(audio);
        });
    });
    micOpen = true;
}
