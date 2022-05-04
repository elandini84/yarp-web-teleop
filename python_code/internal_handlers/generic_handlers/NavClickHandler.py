from tornado.websocket import WebSocketHandler
from yarp import Bottle
import json
import subprocess

class NavClickHandler(WebSocketHandler):

    def initialize(self, webLock, navPort, headPort, mapPort):
        self.webLock = webLock
        self.navPort = navPort
        self.headPort = headPort
        self.mapPort = mapPort
        self._simulating = (self.navPort is None) or (self.headPort is None) or (self.navPort is None)


    def innerPrint(self, message):

        print("NavClickHandler: " + message)


    def on_message(self,message):

        self.webLock.acquire()
        self.innerPrint("Received {0}".format(message))
        options = json.loads(message)
        if not self._simulating:
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
