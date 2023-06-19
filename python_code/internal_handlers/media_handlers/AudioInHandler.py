from tornado.websocket import WebSocketHandler
import wave
import json
from sys import byteorder
from random import randint
from yarp import Sound
from numpy import int16, frombuffer
from datetime import datetime

class AudioInHandler(WebSocketHandler):

    def initialize(self,soundPort):
        self._sampleRate = 1
        self._data = b''
        self._soundPort = soundPort
        self._sentData = 0

    def on_message(self,message):
        if type(message) == str:
            options = json.loads(message)
            if "sampleRate" in options.keys():
                self._sampleRate = int(options["sampleRate"]/3)
                self._data = b''
                self._sampleWidth = 2
            else:
                if options["goOn"]:
                    now_ = datetime.now()
                    timeStamp = "{0}_{1}_{2}".format(now_.hour,now_.minute,now_.second)
                    waveToFile = wave.open('sound_{0}.wav'.format(timeStamp),'wb')
                    waveToFile.setnchannels(1)
                    waveToFile.setframerate(self._sampleRate)
                    waveToFile.setsampwidth(self._sampleWidth)
                    waveToFile.writeframes(self._data)
                    waveToFile.close()

                    print("Data saved: {0}\nData send: {1}".format(waveToFile.getnframes(),self._sentData))

                    self._data = b''
        else:
            self._data += message
            if self._soundPort is not None:
                tempSound = self._soundPort.prepare()
                tempSound.resize(int(len(message)/self._sampleWidth),1)
                tempSound.setFrequency(self._sampleRate)
                for i in range(int(len(message)/self._sampleWidth)):
                    ind = i+i*(self._sampleWidth-1)
                    b = int(frombuffer(message[ind:(ind+self._sampleWidth)],int16)[0])
                    try:
                        tempSound.set(b,i,0)
                    except Exception as e:
                        print("{0}-{1} = {2} ({3} - {4})".format(ind,ind+self._sampleWidth,b,type(b),byteorder))
                        print("{0} - {1}".format(type(message[i]), message[ind:(ind+self._sampleWidth)]))
                        print(e)
                self._soundPort.write()
                self._sentData += int(len(message)/self._sampleWidth)
