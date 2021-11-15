from tornado.web import RequestHandler, StaticFileHandler
from tornado.websocket import WebSocketHandler
from yarp import Port, Network, Bottle, ResourceFinder
from threading import Lock
import json
import os
import sys

from python_code.internal_handlers.generic_handlers.NavClickHandler import NavClickHandler
from python_code.internal_handlers.generic_handlers.IndexHandler import IndexHandler
from python_code.utils.skelServer import SkelServer

ABSPATH = os.path.dirname(os.path.realpath(__file__))
NETWORK = None
RESFINDER = None
CLICKPORT = None
CLICKPORTNAME = "/webview/click:o"
WEBLOCK = Lock()
DUMBTEST = 0


if __name__ == "__main__":

    NETWORK = Network()
    NETWORK.init()
    RESFINDER = ResourceFinder()
    RESFINDER.configure(sys.argv)
    CLICKPORT = Port()

    CLICKPORTNAME = RESFINDER.find("click_port").asString() if RESFINDER.check("click_port") else CLICKPORTNAME
    if RESFINDER.check("camera_port"):
        CAMERAPORTNAME = RESFINDER.find("camera_port").asString()
    else:
        print("Error! Camera port not found")
        sys.exit()
    if RESFINDER.check("map_port"):
        MAPPORTNAME = RESFINDER.find("map_port").asString()
    else:
        print("Error! Map port not found")
        sys.exit()
    if RESFINDER.check("camera_host"):
        CAMERAHOST = RESFINDER.find("camera_host").asString()
    else:
        print("Error! Camera host not found")
        sys.exit()
    if RESFINDER.check("map_host"):
        MAPHOST = RESFINDER.find("map_host").asString()
    else:
        MAPHOST = None
    CLICKPORT.open(CLICKPORTNAME)
    handlersList = [(r'/', IndexHandler,{"inputNetwork": NETWORK,
                                         "cameraPort": CAMERAPORTNAME,
                                         "mapPort": MAPPORTNAME,
                                         "cameraHost": CAMERAHOST,
                                         "resFinder": RESFINDER,
                                         "absPath": ABSPATH,
                                         "mapHost": MAPHOST}),
                    (r"/static/(.*)", StaticFileHandler,{'path':'static'}),
                    (r"/ws", NavClickHandler, {"webLock": WEBLOCK,
                                               "clickPort": CLICKPORT})]
    server = SkelServer(handlersList,16001,True)
    server.start()
