let wsc = new WebSocket(wsType+window.location.host+"/wsc");
wsc.binaryType = 'arraybuffer';


let audioHandler = {
  audioContext: null,
  playing: false,
  myArrayBuffer: null,
  numChannels: 0,
  numSamples: 0,

  setup(numChannels, numSamples, frequency) {
    this.numChannels = numChannels
    this.numSamples = numSamples
    this.myArrayBuffer = this.audioContext.createBuffer(numChannels, numSamples, frequency)
  },

  int16ArrayToAudioBuffer(int16Array) {
  
    for (let channel = 0; channel < this.numChannels; channel++) {
      const channelData = this.myArrayBuffer.getChannelData(channel)
  
      for (let i = 0; i < this.numSamples; i++) {
        channelData[i] = int16Array[i + (channel * this.numSamples)] / 32768.0
      }
    }
  },

  playAudio(audioData) {
    rawAudio = new Int16Array(audioData)
    this.int16ArrayToAudioBuffer(rawAudio)
    let source = this.audioContext.createBufferSource()
    source.buffer = this.myArrayBuffer
    source.connect(this.audioContext.destination)
    source.start();
  }
}


function toggleAudio() {
  audioHandler.playing = !audioHandler.playing
  args = {
    play: audioHandler.playing,
    audioPort: document.getElementById("audioListenBox").value
  }
  
  if (audioHandler.playing) {
    audioHandler.audioContext = new AudioContext()
  }
  
  wsc.send(JSON.stringify(args))

  if (audioHandler.playing) {
    $("#listenBtn").css({ color: "#b7d5e1", backgroundColor: "#3b7991" })
  } else {
    $("#listenBtn").css({ color: "#3b7991", backgroundColor: "#b7d5e1" })
  }
}


wsc.addEventListener("message", (event) => {
  if (event.data instanceof ArrayBuffer) {
    audioHandler.playAudio(event.data)
  } 
  else {
    config = JSON.parse(event.data)
    audioHandler.setup(config.numChannels, config.numSamples, config.frequency)
  }
})