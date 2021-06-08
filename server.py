from tornado.web import RequestHandler, StaticFileHandler
from tornado.websocket import WebSocketHandler
from yarp import Port, Network, Bottle
from threading import Lock
import json
import os
import sys

from python_code.skelServer import SkelServer

ABSPATH = os.path.dirname(os.path.realpath(__file__))
NETWORK = None
CLICKPORT = None
CLICKPORTNAME = "/webview/click:o"
CAMERAPORT = "/freeFloorViewer/floorEnhanced:o"
MAPPORT = "/navigationGui/map:o"
WEBLOCK = Lock()
DUMBTEST = 0

class IndexHandler(RequestHandler):
    def get(self):
        global NETWORK
        global CAMERAPORT
        global MAPPORT
        if len(sys.argv) >= 3:
            contactCamera = NETWORK.queryName(sys.argv[1])
            contactMap = NETWORK.queryName(sys.argv[2])
        else:
            contactCamera = NETWORK.queryName(CAMERAPORT)
            contactMap = NETWORK.queryName(MAPPORT)
        self.render(ABSPATH + '{0}static{0}html{0}index.html'.format(os.sep),
                    porta1 = contactCamera.getHost()+":"+str(contactCamera.getPort()),
                    porta2 = contactMap.getHost()+":"+str(contactMap.getPort()))


class wsHandler(WebSocketHandler):

    def on_message(self,message):

        global WEBLOCK
        WEBLOCK.acquire()
        global CLICKPORT
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
        CLICKPORT.write(b)
        WEBLOCK.release()


if __name__ == "__main__":

    NETWORK = Network()
    NETWORK.init()
    CLICKPORT = Port()
    CLICKPORT.open(CLICKPORTNAME)
    handlersList = [(r'/', IndexHandler),
                    (r"/static/(.*)", StaticFileHandler,{'path':'static'}),
                    (r"/ws", wsHandler)]
    server = SkelServer(handlersList,16001)
    server.start()