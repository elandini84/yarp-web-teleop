from tornado.websocket import WebSocketHandler
from yarp import Bottle
import json
import subprocess

class ButtonsHandler(WebSocketHandler):

    def initialize(self, webLock, navPort):
        self.webLock = webLock
        self.navPort = navPort
        self._simulating = (self.navPort is None)


    def innerPrint(self, message):

        print("ButtonHandler: " + message)


    def on_message(self,message):

        self.webLock.acquire()
        self.innerPrint("Received {0}".format(message))
        options = json.loads(message)
        if not self._simulating:
            b = Bottle()
            if len(options.keys()) == 2:
                b.addString("base")
                b.addInt(int(options["vel-left"]))
                b.addInt(int(options["vel-right"]))
                self.navPort.write(b)
            elif len(options.keys()) == 1:
                if options["audio"] == "FORBID":
                    subprocess.run(["ssh", "r1-user-vpn@10.8.0.30", "aplay", "/home/r1-user-vpn/forbid.wav"])
                elif options["audio"] == "SAFETY":
                    subprocess.run(["ssh", "r1-user-vpn@10.8.0.30", "aplay", "/home/r1-user-vpn/safety.wav"])
                elif options["audio"] == "ALARM":
                    subprocess.run(["ssh", "r1-user-vpn@10.8.0.30", "aplay", "/home/r1-user-vpn/alarm.wav"])
        else:
            if len(options.keys()) == 1:
                subprocess.run(["ls", "-l"])

        self.webLock.release()
