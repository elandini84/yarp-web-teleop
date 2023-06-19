import websocket
from datetime import datetime
import json
from threading import Thread
from sys import byteorder
from yarp import Sound, BufferedPortSound, TypedReaderCallbackSound,Log

class Yarp2WebSoundRedirect(TypedReaderCallbackSound):

    def __init__(self, webSockAddr: str, execlog=False, verbose=False):
        TypedReaderCallbackSound.__init__(self)
        if execlog:
            #Log.info("Yarp2WebSoundRedirect.__init__ called at: {0}".format(datetime.now()))
            print("Yarp2WebSoundRedirect.__init__ called at: {0}".format(datetime.now()))
        self._webSockAddr = webSockAddr
        try:
            self._webSocket = websocket.create_connection(self._webSockAddr)
        except Exception as e:
            #Log.error("Connection to {0} failed due to: {1}".format(self._webSockAddr,e))
            print("Connection to {0} failed due to: {1}".format(self._webSockAddr,e))
            self._webSocket = None
        self._execLog = execlog
        self._verbose = verbose


    def onRead(self, inputSound: Sound, reader):

        if self._execLog:
            #Log.info("Yarp2WebSoundRedirect.onRead called at: {0}".format(datetime.now()))
            print("Yarp2WebSoundRedirect.onRead called at: {0}".format(datetime.now()))
        if self._webSocket is None:
            try:
                self._webSocket = websocket.create_connection(self._webSockAddr)
                if self._verbose:
                    print("Connection succeeded")
            except Exception as e:
                #Log.error("Connection to {0} failed due to: {1}".format(self._webSockAddr,e))
                print("Connection to {0} failed due to: {1}".format(self._webSockAddr,e))
                self._webSocket = None

        try:
            self._webSocket.send("franco_{0}_{1}".format(inputSound.getSamples(),inputSound.getFrequency()))
        except Exception as e:
            #Log.error("Sending message to {0} failed due to: {1}".format(self._webSockAddr,e))
            print("Sending message to {0} failed due to: {1}".format(self._webSockAddr,e))
