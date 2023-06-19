from tornado.websocket import WebSocketHandler
import json
from sys import byteorder
from yarp import Sound, BufferedPortSound, TypedReaderCallbackSound,Log

class AudioOutHandler(WebSocketHandler,TypedReaderCallbackSound):

    def initialize(self,soundPort: BufferedPortSound):
        self._sampleRate = 1
        self._bytesPerSample = 2
        self._soundPort = soundPort
        self._soundPort.useCallback(self)


    def onRead(self,inputSound: Sound, reader):
        print("Received a sound with samples num: {0}".format(inputSound.getSamples()))
        self._sampleRate = inputSound.getFrequency()
        self._bytesPerSample = inputSound.getBytesPerSample()

        message = {"sampleRate": self._sampleRate, "bytesPerSample": self._bytesPerSample}
        try:
            self.write_message(message)
        except Exception as e:
            print("Writing message failed: {0}".format(e))


    def on_message(self, message):
        return super().on_message(message)
