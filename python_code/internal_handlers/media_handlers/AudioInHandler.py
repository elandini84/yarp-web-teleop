import io
from tornado.websocket import WebSocketHandler
import wave
import json
from random import randint

class AudioInHandler(WebSocketHandler):

    def initialize(self):
        self._frameRate = 1
        self._count = randint(0,10)
        self._data = b''

    def on_message(self,message):
        #print("Got {0} of type {1}".format(message,type(message)))
        if type(message) == str:
            options = json.loads(message)
            if "sampleRate" in options.keys():
                print("porcodio")
                self._frameRate = options["sampleRate"]
                self._data = b''
            else:
                if options["goOn"]:
                    waveToFile = wave.open('/home/elandini/mainData/sound_{0}.wav'.format(self._count),'wb')
                    waveToFile.setnchannels(1)
                    waveToFile.setframerate(self._frameRate/3)
                    waveToFile.setsampwidth(2)
                    waveToFile.writeframes(self._data)
                    waveToFile.close()
                    self._data = b''
                    self._count += 1
        else:
            self._data += message
            print(len(self._data))
