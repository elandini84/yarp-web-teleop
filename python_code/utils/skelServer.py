from tornado.ioloop import IOLoop
from tornado.web import Application


class SkelServer(object):

    def __init__(self,handlers,port):

        self.handlers = handlers
        self.port = port


    def start(self):

        self.tornadoApp = Application(self.handlers)
        self.tornadoApp.listen(self.port)
        IOLoop.instance().start()


    def stop(self):

        IOLoop.instance().stop()