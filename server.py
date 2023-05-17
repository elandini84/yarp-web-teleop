from tornado.web import StaticFileHandler
import tornado.httpserver
import yarp
from threading import Lock
import sqlite3 as sl
import json
import os
import signal, sys, threading
import secrets

from python_code.internal_handlers.generic_handlers.NavClickHandler import NavClickHandler
from python_code.internal_handlers.generic_handlers.ButtonsHandler import ButtonsHandler
from python_code.internal_handlers.generic_handlers.IndexHandler import IndexHandler
from python_code.internal_handlers.media_handlers.AudioInHandler import AudioInHandler
from python_code.internal_handlers.credential_handlers.LoginHandler import LoginHandler, ActiveUsersRegister
from python_code.internal_handlers.credential_handlers.RegisterHandler import RegisterHandler
from python_code.internal_handlers.credential_handlers.LogoutHandler import LogoutHandler
from python_code.internal_handlers.credential_handlers.AuthHandler import AuthHandler
from python_code.utils.cookieServer import CookieServer

## Execution example
# python3 server.py --camera_port 10009 --camera_host 192.168.92.109 --map_port 10014 --no_ssl
# python3 server.py --camera_port 10010 --camera_host 192.168.20.162 --map_port 10010 --no_ssl
# python3 server.py --simulate --no_ssl
# python3 server.py --simulate

ABSPATH = os.path.dirname(os.path.realpath(__file__))
ADMINKEY = "1234qwer"
SERVERPORT = 16001
NETWORK = None
RESFINDER = None
NAVCLICKPORT = None
HEADCLICKPORT = None
MAPCLICKPORT = None
NAVCLICKPORTNAME = "/webview/navClick:o"
HEADCLICKPORTNAME = "/webview/headClick:o"
MAPCLICKPORTNAME = "/webview/mapClick:o"
WEBLOCK = Lock()
dirname = os.path.dirname(__file__)
dbPath = os.path.join(dirname, "static/sql_db/users.db")
certificates_folder = os.path.join(dirname, "resources/certificates")
certificates_name = "host"
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

    RESFINDER = yarp.ResourceFinder()
    RESFINDER.configure(sys.argv)
    createUsersTable(loginDb)
    commonAUR = ActiveUsersRegister(True,True)

    if RESFINDER.check("no_ssl") or RESFINDER.check("traefik"):
        certificates_folder = None
        certificates_name = None
    else:
        certificates_folder = RESFINDER.find("certificates_path").asString() if RESFINDER.check("certificates_path") else certificates_folder
        certificates_name = RESFINDER.find("certificates_name").asString() if RESFINDER.check("certificates_name") else certificates_name
    if RESFINDER.check("simulate"):
        handlersList = [(r'/', IndexHandler,{"inputNetwork": NETWORK,
                                             "cameraPort": "",
                                             "mapPort": "",
                                             "cameraHost": "",
                                             "resFinder": None,
                                             "absPath": ABSPATH,
                                             "mapHost": "",
                                             "simulate":True,
                                             "isSsl": (not RESFINDER.check("no_ssl")) or RESFINDER.check("traefik")}),
                        (r'/auth',AuthHandler),
                        (r'/wsa',AudioInHandler),
                        (r'/login', LoginHandler,{"absPath": ABSPATH,"aur": commonAUR,"my_db": loginDb}),
                        (r'/logout', LogoutHandler,{"absPath": ABSPATH,"aur": commonAUR,"my_db": loginDb}),
                        (r'/register', RegisterHandler,{"absPath": ABSPATH,"aur": commonAUR,"my_db": loginDb,"adminkey": ADMINKEY}),
                        (r"/static/(.*)", StaticFileHandler,{'path':'static'}),
                        (r"/ws", NavClickHandler, {"webLock": WEBLOCK,
                                                   "navPort": NAVCLICKPORT,
                                                   "headPort": HEADCLICKPORT,
                                                   "mapPort": MAPCLICKPORT}),
                        (r"/wsb", ButtonsHandler, {"webLock": WEBLOCK,
                                                   "navPort": NAVCLICKPORT})]
    else:
        NETWORK = yarp.Network()
        NETWORK.init()
        NAVCLICKPORT = yarp.Port()
        MAPCLICKPORT = yarp.Port()
        HEADCLICKPORT = yarp.Port()

        NAVCLICKPORTNAME = RESFINDER.find("nav_click_port").asString() if RESFINDER.check("nav_click_port") else NAVCLICKPORTNAME
        MAPCLICKPORTNAME = RESFINDER.find("map_click_port").asString() if RESFINDER.check("map_click_port") else MAPCLICKPORTNAME
        HEADCLICKPORTNAME = RESFINDER.find("head_click_port").asString() if RESFINDER.check("head_click_port") else HEADCLICKPORTNAME

        NAVCLICKPORT.open(NAVCLICKPORTNAME)
        MAPCLICKPORT.open(MAPCLICKPORTNAME)
        HEADCLICKPORT.open(HEADCLICKPORTNAME)

        if RESFINDER.check("server_port"):
            SERVERPORT = RESFINDER.find("server_port").asInt32()

        MAPPORT = None
        CAMERAPORT = None
        MAPHOST = None
        CAMERAHOST = None

        if RESFINDER.check("camera_name"):
            tempConn = yarp.NetworkBase_queryName(RESFINDER.find("camera_name").toString())
            CAMERAPORT = str(tempConn.getPort())
            CAMERAHOST = tempConn.getHost()
        if RESFINDER.check("map_name"):
            tempConn = yarp.NetworkBase_queryName(RESFINDER.find("map_name").toString())
            MAPPORT = str(tempConn.getPort())
            MAPHOST = tempConn.getHost()

        if RESFINDER.check("camera_port"):
            CAMERAPORT = RESFINDER.find("camera_port").toString()
        else:
            if CAMERAPORT is None:
                print("Error! Camera port not found")
                sys.exit()
        if RESFINDER.check("map_port"):
            MAPPORT = RESFINDER.find("map_port").toString()
        else:
            if MAPPORT is None:
                print("Error! Map port not found")
                sys.exit()
        if RESFINDER.check("camera_host"):
            CAMERAHOST = RESFINDER.find("camera_host").asString()
        else:
            if CAMERAHOST is None:
                print("Error! Camera host not found")
                sys.exit()
        if RESFINDER.check("map_host"):
            MAPHOST = RESFINDER.find("map_host").asString()

        handlersList = [(r'/', IndexHandler,{"inputNetwork": NETWORK,
                                             "cameraPort": CAMERAPORT,
                                             "mapPort": MAPPORT,
                                             "cameraHost": CAMERAHOST,
                                             "resFinder": RESFINDER,
                                             "absPath": ABSPATH,
                                             "mapHost": MAPHOST,
                                             "isSsl": (not RESFINDER.check("no_ssl")) or RESFINDER.check("traefik"),
                                             "simulate": False}),
                        (r'/auth',AuthHandler),
                        (r'/wsa',AudioInHandler),
                        (r'/login', LoginHandler,{"absPath": ABSPATH, "aur": commonAUR,"my_db": loginDb}),
                        (r'/logout', LogoutHandler,{"absPath": ABSPATH,"aur": commonAUR,"my_db": loginDb}),
                        (r'/register', RegisterHandler,{"absPath": ABSPATH,"aur": commonAUR,"my_db": loginDb,"adminkey": ADMINKEY}),
                        (r"/static/(.*)", StaticFileHandler,{'path':'static'}),
                        (r"/ws", NavClickHandler, {"webLock": WEBLOCK,
                                                   "navPort": NAVCLICKPORT,
                                                   "headPort": HEADCLICKPORT,
                                                   "mapPort": MAPCLICKPORT}),
                        (r"/wsb", ButtonsHandler, {"webLock": WEBLOCK,
                                                   "navPort": NAVCLICKPORT})]
    server = CookieServer(handlersList,SERVERPORT,certificates_folder,certificates_name,True,secrets.token_urlsafe())

    def signal_handler(signal, frame):
        print('exiting')
        server.stop()
        print('before exit')
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGHUP, signal_handler)

    print('Running on port %d' % SERVERPORT)
    print('Press Ctrl+C to stop')
    #signal.pause()
    server.start()
