let wsc = new WebSocket(wsType+window.location.host+"/wsc");
wsc.binaryType = 'arraybuffer';

let audioContext = new AudioContext();
let myArrayBuffer = audioContext.createBuffer(
    1,
    16000 * 3,
    16000,
  );


function int16ArrayToAudioBuffer(int16Array, arrayBuffer) {
  const numberOfChannels = 1;
  const numberOfFrames = int16Array.length;

  for (let channel = 0; channel < numberOfChannels; channel++) {
    const channelData = arrayBuffer.getChannelData(channel);
    for (let i = 0; i < numberOfFrames; i++) {
      channelData[i] = int16Array[i * numberOfChannels + channel] / 32768.0;
    }
  }

}


wsc.onmessage = function(event){
    rawAudio = new Int16Array(event.data)
    int16ArrayToAudioBuffer(rawAudio, myArrayBuffer)
    let source = audioContext.createBufferSource();
    source.buffer = myArrayBuffer;
    source.connect(audioContext.destination);
    source.start();
    console.log(rawAudio)
}
