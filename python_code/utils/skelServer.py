from tornado.ioloop import IOLoop
from tornado.web import Application
import tornado.httpserver
import os


class SkelServer(object):

    def __init__(self,handlers,port,cert_path,cert_name,autoreload=False):

        self.handlers = handlers
        self.port = port
        self.autoReload = autoreload
        self.cert_path = cert_path
        self.cert_name = cert_name
        self.tornadoApp = None


    def configApp(self):
        self.tornadoApp = Application(self.handlers, autoreload=self.autoReload)


    def start(self):
        self.configApp()
        if self.cert_path is not None:
            http_server = tornado.httpserver.HTTPServer(self.tornadoApp, ssl_options={
                    "certfile": os.path.join(self.cert_path,"{0}.crt".format(self.cert_name)),
                    "keyfile": os.path.join(self.cert_path,"{0}.key".format(self.cert_name)),
                })
            http_server.listen(self.port)
        else:
            self.tornadoApp.listen(self.port)
        IOLoop.instance().start()


    def stop(self):

        IOLoop.instance().stop()
