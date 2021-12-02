from tornado.web import Application

from .skelServer import SkelServer

class CookieServer(SkelServer):

    def __init__(self,handlers,port,cert_path,cert_name,autoreload,cookie_secret,key_version=None):

        SkelServer.__init__(self,handlers,port,cert_path,cert_name,autoreload)
        self.cookieSecret = cookie_secret
        self.keyVersion = key_version


    def configApp(self):

        if self.keyVersion is not None:
            self.tornadoApp = Application(self.handlers,
                                          cookie_secret=self.cookieSecret,
                                          key_version=self.keyVersion,
                                          autoreload=self.autoReload)
        else:
            self.tornadoApp = Application(self.handlers,
                                          cookie_secret=self.cookieSecret,
                                          autoreload=self.autoReload)
