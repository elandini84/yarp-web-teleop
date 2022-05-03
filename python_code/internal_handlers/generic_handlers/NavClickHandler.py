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


    def on_message(self,message):

        self.webLock.acquire()
        print("Received: {0}", message)
        options = json.loads(message)
        if not self._simulating:
            b = Bottle()
            buttonInvolved = "button" in options.keys()
            if buttonInvolved:
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
            else:
                if len(options.keys()) == 2:
                    b.addString("base")
                    b.addInt(int(options["vel-left"]))
                    b.addInt(int(options["vel-right"]))
                    self.navPort.write(b)
                elif len(options.keys()) == 1:
                    if options["audio"] == "FORBID":
                        subprocess.run(["ssh", "r1-user-vpn@10.8.0.30 aplay /home/r1-user-vpn/forbid.mp3"])
                    elif options["audio"] == "SAFETY":
                        subprocess.run(["ssh", "r1-user-vpn@10.8.0.30 aplay /home/r1-user-vpn/safety.mp3"])
                    elif options["audio"] == "ALARM":
                        subprocess.run(["ssh", "r1-user-vpn@10.8.0.30 aplay /home/r1-user-vpn/alarm.mp3"])
        else:
            if len(options.keys()) == 1:
                print("tutto")
                subprocess.run(["ls", "-l"])

        self.webLock.release()
