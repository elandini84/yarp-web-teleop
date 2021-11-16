from tornado.ioloop import IOLoop
from tornado.web import Application


class SkelServer(object):

    def __init__(self,handlers,port,autoreload=False):

        self.handlers = handlers
        self.port = port
        self.autoReload = autoreload
        self.tornadoApp = None


    def configApp(self):
        self.tornadoApp = Application(self.handlers, autoreload=self.autoReload)


    def start(self):
        self.configApp()
        self.tornadoApp.listen(self.port)
        IOLoop.instance().start()


    def stop(self):

        IOLoop.instance().stop()
