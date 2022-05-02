from tornado.websocket import WebSocketHandler
from yarp import Bottle
import json

class NavClickHandler(WebSocketHandler):

    def initialize(self, webLock, navPort, headPort, mapPort):
        self.webLock = webLock
        self.navPort = navPort
        self.headPort = headPort
        self.mapPort = mapPort
        self._simulating = (self.navPort is None) or (self.headPort is None) or (self.navPort is None)


    def on_message(self,message):

        self.webLock.acquire()
        print("Received: {0}", message)
        if not self._simulating:
            options = json.loads(message)
            b = Bottle()
            if len(options.keys()) > 4:
                b.addInt(int(options["x-start"]))
                b.addInt(int(options["y-start"]))
                b.addInt(int(options["x-end"]))
                b.addInt(int(options["y-end"]))
            elif len(options.keys()) == 2:
                b.addString("base")
                b.addInt(int(options["vel-left"]))
                b.addInt(int(options["vel-right"]))
            else:
                b.addInt(int(options["x"]))
                b.addInt(int(options["y"]))
            if "button" in options.keys():
                if options["button"] == 0:
                    if options["is_robot"]:
                        self.navPort.write(b)
                    else:
                        self.mapPort.write(b)
                elif options["button"] == 2:
                    if options["is_robot"]:
                        self.headPort.write(b)
        self.webLock.release()
