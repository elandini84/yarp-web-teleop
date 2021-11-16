from tornado.web import RequestHandler, StaticFileHandler
from tornado.websocket import WebSocketHandler
from yarp import Port, Network, Bottle, ResourceFinder
from threading import Lock
import sqlite3 as sl
import json
import os
import sys

from python_code.internal_handlers.generic_handlers.NavClickHandler import NavClickHandler
from python_code.internal_handlers.generic_handlers.IndexHandler import IndexHandler
from python_code.internal_handlers.credential_handlers.LoginHandler import LoginHandler
from python_code.internal_handlers.credential_handlers.RegisterHandler import RegisterHandler
from python_code.internal_handlers.credential_handlers.LogoutHandler import LogoutHandler
from python_code.utils.cookieServer import CookieServer

ABSPATH = os.path.dirname(os.path.realpath(__file__))
NETWORK = None
RESFINDER = None
CLICKPORT = None
CLICKPORTNAME = "/webview/click:o"
WEBLOCK = Lock()
dirname = os.path.dirname(__file__)
dbPath = os.path.join(dirname, "static/sql_db/users.db")
loginDb = sl.connect(dbPath)


def createUsersTable(inputDb):
    sql_create_projects_table = ''' CREATE TABLE IF NOT EXISTS users (
                                        id integer primary key,
                                        name text not null,
                                        password text not null) '''
    try:
        c = inputDb.cursor()
        c.execute(sql_create_projects_table)
    except Exception as e:
        print("This is an error")
        print(e)


if __name__ == "__main__":

    NETWORK = Network()
    NETWORK.init()
    RESFINDER = ResourceFinder()
    RESFINDER.configure(sys.argv)
    CLICKPORT = Port()
    createUsersTable(loginDb)

    CLICKPORTNAME = RESFINDER.find("click_port").asString() if RESFINDER.check("click_port") else CLICKPORTNAME
    if RESFINDER.check("camera_port"):
        CAMERAPORTNAME = RESFINDER.find("camera_port").toString()
    else:
        print("Error! Camera port not found")
        sys.exit()
    if RESFINDER.check("map_port"):
        MAPPORTNAME = RESFINDER.find("map_port").toString()
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
                    (r'/login', LoginHandler,{"absPath": ABSPATH,"my_db": loginDb}),
                    (r'/logout', LogoutHandler,{"absPath": ABSPATH,"my_db": loginDb}),
                    (r'/register', RegisterHandler,{"absPath": ABSPATH,"my_db": loginDb}),
                    (r"/static/(.*)", StaticFileHandler,{'path':'static'}),
                    (r"/ws", NavClickHandler, {"webLock": WEBLOCK,
                                               "clickPort": CLICKPORT})]
    server = CookieServer(handlersList,16001,True,{1:"firsttry",2:"secondtry"},1)
    server.start()
