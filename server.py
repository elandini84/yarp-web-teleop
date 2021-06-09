from tornado.web import RequestHandler, StaticFileHandler
from tornado.websocket import WebSocketHandler
from yarp import Port, Network, Bottle, ResourceFinder
from threading import Lock
import json
import os
import sys

from python_code.skelServer import SkelServer

ABSPATH = os.path.dirname(os.path.realpath(__file__))
NETWORK = None
RESFINDER = None
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
        global RESFINDER
        contactCamera = NETWORK.queryName(RESFINDER.find("camera_port").asString() if RESFINDER.check("camera_port") else CAMERAPORT)
        contactMap = NETWORK.queryName(RESFINDER.find("map_port").asString() if RESFINDER.check("map_port") else MAPPORT)
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
    RESFINDER = ResourceFinder()
    RESFINDER.configure(sys.argv)
    CLICKPORT = Port()
    CLICKPORTNAME = RESFINDER.find("click_port").asString if RESFINDER.check("click_port") else CLICKPORTNAME
    CLICKPORT.open(CLICKPORTNAME)
    handlersList = [(r'/', IndexHandler),
                    (r"/static/(.*)", StaticFileHandler,{'path':'static'}),
                    (r"/ws", wsHandler)]
    server = SkelServer(handlersList,16001)
    server.start()