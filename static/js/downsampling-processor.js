class DownsamplingProcessor extends AudioWorkletProcessor {
    constructor() {
        super();
        this.downsampled = new Int16Array(2048);
        this.downsample_offset = 0;
        this.sampleRateRatio = sampleRate / 16000;
    }

    process(inputs, outputs, parameters) {
        const input = inputs[0];
        if (input.length > 0) {
            const inputData = input[0];
            for (let i = 0; i < inputData.length; i += this.sampleRateRatio) {
                const sidx = Math.floor(i);
                const tidx = Math.floor(i / this.sampleRateRatio);
                this.downsampled[this.downsample_offset + tidx] = inputData[sidx] * 32767;
            }
            this.downsample_offset += Math.floor(inputData.length / this.sampleRateRatio);
            if (this.downsample_offset > audioBufferLen) {
                this.processSamples();
            }
        }
        return true; // Keep processor alive
    }

    processSamples() {
        while (this.downsample_offset > audioBufferLen) {
            const output = this.downsampled.slice(0, audioBufferLen);
            this.downsampled.copyWithin(0, audioBufferLen);
            this.downsample_offset -= audioBufferLen;
            if (self.ptt === true) {
                self.port.postMessage(output.buffer);
            }
        }
    }
}

registerProcessor('downsampling-processor', DownsamplingProcessor);
