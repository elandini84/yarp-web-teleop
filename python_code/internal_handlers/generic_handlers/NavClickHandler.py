from tornado.websocket import WebSocketHandler
from yarp import Bottle
import json

class NavClickHandler(WebSocketHandler):

    def initialize(self, webLock, clickPort):
        self.webLock = webLock
        self.clickPort = clickPort


    def on_message(self,message):

        self.webLock.acquire()
        options = json.loads(message)
        b = Bottle()
        if len(options.keys()) > 2:
            b.addInt(int(options["x-start"]))
            b.addInt(int(options["y-start"]))
            b.addInt(int(options["x-end"]))
            b.addInt(int(options["y-end"]))
        else:
            print("NOT FULLY SUPPORTED: {0}", message)
            b.addInt(int(options["x"]))
            b.addInt(int(options["y"]))
        self.clickPort.write(b)
        self.webLock.release()
