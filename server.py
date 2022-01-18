from tornado.web import StaticFileHandler
import tornado.httpserver
from yarp import Port, Network, Bottle, ResourceFinder
from threading import Lock
import sqlite3 as sl
import json
import os
import sys
import secrets

from python_code.internal_handlers.generic_handlers.NavClickHandler import NavClickHandler
from python_code.internal_handlers.generic_handlers.IndexHandler import IndexHandler
from python_code.internal_handlers.credential_handlers.LoginHandler import LoginHandler
from python_code.internal_handlers.credential_handlers.RegisterHandler import RegisterHandler
from python_code.internal_handlers.credential_handlers.LogoutHandler import LogoutHandler
from python_code.internal_handlers.credential_handlers.AuthHandler import AuthHandler
from python_code.utils.cookieServer import CookieServer

## Execution example
# python3 server.py --camera_port 10009 --camera_host 192.168.92.109 --map_port 10014 --nav_click_port /click --no_ssl
# python3 server.py --simulate --no_ssl

ABSPATH = os.path.dirname(os.path.realpath(__file__))
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

    NETWORK = Network()
    NETWORK.init()
    RESFINDER = ResourceFinder()
    RESFINDER.configure(sys.argv)
    NAVCLICKPORT = Port()
    MAPCLICKPORT = Port()
    HEADCLICKPORT = Port()
    createUsersTable(loginDb)

    NAVCLICKPORTNAME = RESFINDER.find("nav_click_port").asString() if RESFINDER.check("nav_click_port") else NAVCLICKPORTNAME
    MAPCLICKPORTNAME = RESFINDER.find("map_click_port").asString() if RESFINDER.check("map_click_port") else MAPCLICKPORTNAME
    HEADCLICKPORTNAME = RESFINDER.find("head_click_port").asString() if RESFINDER.check("head_click_port") else HEADCLICKPORTNAME
    if RESFINDER.check("no_ssl"):
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
                                             "simulate":True}),
                        (r'/auth',AuthHandler),
                        (r'/login', LoginHandler,{"absPath": ABSPATH,"my_db": loginDb}),
                        (r'/logout', LogoutHandler,{"absPath": ABSPATH,"my_db": loginDb}),
                        (r'/register', RegisterHandler,{"absPath": ABSPATH,"my_db": loginDb}),
                        (r"/static/(.*)", StaticFileHandler,{'path':'static'})]
    else:
        if RESFINDER.check("server_port"):
            SERVERPORT = RESFINDER.find("server_port").asInt32()
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
        NAVCLICKPORT.open(NAVCLICKPORTNAME)
        MAPCLICKPORT.open(MAPCLICKPORTNAME)
        HEADCLICKPORT.open(HEADCLICKPORTNAME)
        handlersList = [(r'/', IndexHandler,{"inputNetwork": NETWORK,
                                             "cameraPort": CAMERAPORTNAME,
                                             "mapPort": MAPPORTNAME,
                                             "cameraHost": CAMERAHOST,
                                             "resFinder": RESFINDER,
                                             "absPath": ABSPATH,
                                             "mapHost": MAPHOST,
                                             "simulate":False}),
                        (r'/auth',AuthHandler),
                        (r'/login', LoginHandler,{"absPath": ABSPATH,"my_db": loginDb}),
                        (r'/logout', LogoutHandler,{"absPath": ABSPATH,"my_db": loginDb}),
                        (r'/register', RegisterHandler,{"absPath": ABSPATH,"my_db": loginDb}),
                        (r"/static/(.*)", StaticFileHandler,{'path':'static'}),
                        (r"/ws", NavClickHandler, {"webLock": WEBLOCK,
                                                   "navPort": NAVCLICKPORT,
                                                   "headPort": HEADCLICKPORT,
                                                   "mapPort": MAPCLICKPORT})]
    server = CookieServer(handlersList,SERVERPORT,certificates_folder,certificates_name,True,secrets.token_urlsafe())
    server.start()
