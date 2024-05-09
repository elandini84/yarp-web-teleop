import io
import time
from typing import Dict
from tornado.concurrent import Future
from tornado.websocket import WebSocketHandler
from tornado.ioloop import PeriodicCallback
import numpy as np
import yarp
from sys import byteorder
from random import randint
from yarp import Sound
from numpy import int16, frombuffer
from datetime import datetime

class AudioOutHandler(WebSocketHandler):
    def open(self):
        print('WebSocket opened!!!!!!!!!!!!!!!')
        
    def initialize(self,network):
        self.callback = PeriodicCallback(self.periodic_call, 1000, )  # Call every 1 second
        self.callback.start()

        self.sound = yarp.Sound()
    
        self.audio_buffer = []
        self.portIn = yarp.BufferedPortSound()
        self.portIn.open('/test:i')
        self.network = network
        self.network.connect('/audioRecorder_nws/audio:o', '/test:i')

    def periodic_call(self):
        self.sound = self.portIn.read()
        audioBuffer = np.array([self.sound.get(i) for i in range(self.sound.getSamples())]).astype(np.int16)
        print(audioBuffer)

        
        self.write_message(audioBuffer.tobytes(), binary=True)
