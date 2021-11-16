from tornado.web import Application

from .skelServer import SkelServer

class CookieServer(SkelServer):

    def __init__(self,handlers,port,autoreload,cookie_secret,key_version):

        SkelServer.__init__(self,handlers,port,autoreload)
        self.cookieSecret = cookie_secret
        self.keyVersion = key_version


    def configApp(self):

        self.tornadoApp = Application(self.handlers,
                                      cookie_secret=self.cookieSecret,
                                      key_version=self.keyVersion,
                                      autoreload=self.autoReload)