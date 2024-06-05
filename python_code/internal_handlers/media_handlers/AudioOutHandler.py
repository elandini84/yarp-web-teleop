import json
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
    def initialize(self, network, audioPort):
        print(audioPort)
        self.callback = PeriodicCallback(self.periodic_call, 1000)

        self.sound = yarp.Sound()
    
    
        self.portIn = yarp.BufferedPortSound()
        self.portIn.open('/webAudio:i')
        self.network = network
        self.audioPort = audioPort
        self.connect_to_port()


    def connect_to_port(self):
        if self.audioPort is None or len(self.audioPort) == 0:
            self.connected = False
            print("No valid audio port provided")
        else:
            print("Connecting: {0} with /webAudio:i".format(self.audioPort))
            self.network.connect(self.audioPort, '/webAudio:i')
            self.connected = True


    def periodic_call(self):
        self.sound = self.portIn.read()
        audioBuffer = np.array([self.sound.get(i) for i in range(self.sound.getSamples())]).astype(np.int16)

        self.write_message(audioBuffer.tobytes(), binary=True)


    def play(self, audioPort):
        # Connect to new audio port if it has changed
        if audioPort != self.audioPort:
            if self.connected:
                self.network.disconnect(self.audioPort, '/webAudio:i')
            self.audioPort = audioPort
            self.connect_to_port()

        self.sound = self.portIn.read()
        audioContextConfig = {"numSamples": self.sound.getSamples(), "numChannels": self.sound.getChannels(), "frequency": self.sound.getFrequency()}
        self.write_message(json.dumps(audioContextConfig))

        self.callback.callback_time = (self.sound.getSamples() / self.sound.getFrequency()) * 1000
        self.callback.start() # start streaming
        

    def on_message(self, message):
        if not self.connected:
            pass

        args = json.loads(message)
        
        if args["play"]:
            self.play(args["audioPort"])
        else:
            self.callback.stop()
