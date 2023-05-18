import io
from tornado.websocket import WebSocketHandler
import wave
import json
import sys
from random import randint
from yarp import Sound

class AudioInHandler(WebSocketHandler):

    def initialize(self,soundPort):
        self._sampleRate = 1
        self._count = randint(0,10)
        self._data = b''
        self._soundPort = soundPort

    def on_message(self,message):
        #print("Got {0} of type {1}".format(message,type(message)))
        if type(message) == str:
            options = json.loads(message)
            if "sampleRate" in options.keys():
                self._sampleRate = int(options["sampleRate"]/3)
                self._data = b''
            else:
                if options["goOn"]:
                    waveToFile = wave.open('/home/elandini/mainData/sound_{0}.wav'.format(self._count),'wb')
                    waveToFile.setnchannels(1)
                    waveToFile.setframerate(self._sampleRate)
                    waveToFile.setsampwidth(2)

                    print("\n\nwaveToFile: {0} {1}\n\n".format(waveToFile.getframerate(),waveToFile.getsampwidth()))

                    waveToFile.writeframes(self._data)
                    waveToFile.close()
                    self._data = b''
                    self._count += 1
        else:
            #sosso = Sound()
            self._data += message
            tempSound = self._soundPort.prepare()
            tempSound.resize(len(message),1)
            tempSound.setFrequency(self._sampleRate)
            print("tempSound: {0} {1}".format(tempSound.getFrequency(),tempSound.getBytesPerSample()))
            i = 0
            for b in message:
                tempSound.set(b,i,0)
            print("Sound ready: {0}".format(tempSound.getSamples()))
            self._soundPort.write()
