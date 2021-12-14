from tornado.websocket import WebSocketHandler
from yarp import Bottle
import json

class NavClickHandler(WebSocketHandler):

    def initialize(self, webLock, navPort, headPort, mapPort):
        self.webLock = webLock
        self.navPort = navPort
        self.headPort = headPort
        self.mapPort = mapPort


    def on_message(self,message):

        self.webLock.acquire()
        print("Received: {0}", message)
        options = json.loads(message)
        b = Bottle()
        if len(options.keys()) > 4:
            b.addInt(int(options["x-start"]))
            b.addInt(int(options["y-start"]))
            b.addInt(int(options["x-end"]))
            b.addInt(int(options["y-end"]))
        else:
            b.addInt(int(options["x"]))
            b.addInt(int(options["y"]))
        if options["button"] == 0:
            if options["is_robot"]:
                self.navPort.write(b)
            else:
                self.mapPort.write(b)
        elif options["button"] == 2:
            if options["is_robot"]:
                self.headPort.write(b)
        self.webLock.release()
