from tornado.websocket import WebSocketHandler
import json
from sys import byteorder
from yarp import Sound, BufferedPortSound, TypedReaderCallbackSound,Log
import asyncio
from threading import Thread

class AudioOutHandler(WebSocketHandler,TypedReaderCallbackSound):

    def initialize(self,soundPort: BufferedPortSound):
        self._sampleRate = 1
        self._bytesPerSample = 2
        self._soundPort = soundPort
        self._soundPort.useCallback(self)


    def onRead(self,inputSound: Sound, reader):
        self._sampleRate = inputSound.getFrequency()
        self._bytesPerSample = inputSound.getBytesPerSample()

        samples = []
        for s in range(inputSound.getSamples()):
            samples.append(inputSound.getSafe(s,0))
        message = {"sampleRate": self._sampleRate, "bytesPerSample": self._bytesPerSample,"sound": samples}
        try:
            eventLoop = asyncio.new_event_loop()
            asyncio.set_event_loop(eventLoop)
            async def deliver_message():
                self.write_message(json.dumps(message))
            asyncio.get_event_loop().run_until_complete(deliver_message())
            eventLoop.close()
        except Exception as e:
            print("Writing message failed: {0}".format(e))


    def on_message(self, message):
        return super().on_message(message)
