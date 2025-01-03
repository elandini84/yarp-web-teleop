from tornado.websocket import WebSocketHandler
from yarp import Bottle
import json
import subprocess
from datetime import datetime

class ButtonsHandler(WebSocketHandler):

    def initialize(self, webLock, navPort):
        self.webLock = webLock
        self.navPort = navPort
        self._simulating = (self.navPort is None)


    def innerPrint(self, message):

        print("ButtonHandler: " + message)


    def on_message(self,message):

        self.webLock.acquire()
        self.innerPrint("Received {0} - {1}".format(message,datetime.now()))
        options = json.loads(message)
        if not self._simulating:
            b = Bottle()
            if len(options.keys()) == 3:
                b.addString("base")
                b.addInt32(int(options["vel-left"]))
                b.addInt32(int(options["vel-right"]))
                b.addInt32(int(options["vel-forward"]))
                b.addInt32(0)
                self.navPort.write(b)
            elif len(options.keys()) == 1:
                if options["audio"] == "FORBID":
                    subprocess.run(["ssh", "-o", "ConnectionTimeout=2", "r1-user-vpn@10.8.0.30", "aplay", "/home/r1-user-vpn/forbid.wav"])
                elif options["audio"] == "SAFETY":
                    subprocess.run(["ssh", "-o", "ConnectionTimeout=2", "r1-user-vpn@10.8.0.30", "aplay", "/home/r1-user-vpn/safety.wav"])
                elif options["audio"] == "ALARM":
                    subprocess.run(["ssh", "-o", "ConnectionTimeout=2", "r1-user-vpn@10.8.0.30", "aplay", "/home/r1-user-vpn/alarm.wav"])
        else:
            if len(options.keys()) == 1:
                subprocess.run(["ls", "-l"])

        self.webLock.release()
