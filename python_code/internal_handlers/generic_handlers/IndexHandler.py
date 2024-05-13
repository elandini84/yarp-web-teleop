from tornado.web import RequestHandler
import os

class IndexHandler(RequestHandler):

    def initialize(self,inputNetwork,cameraPort,mapPort,audioPort,cameraHost,resFinder,absPath,audioBufferLen,mapHost=None,isSsl=False,simulate=False):
        self.yarpNet = inputNetwork
        self.cameraPort = cameraPort
        self.cameraHost = cameraHost
        self.mapPort = mapPort
        self.mapHost = mapHost if mapHost is not None else cameraHost
        self.audioPort = audioPort
        self.resFinder = resFinder
        self.absPath = absPath
        self.simulate = simulate
        self._ssl = isSsl
        self._audioBufferLen = audioBufferLen


    def get_current_user(self):
        return self.get_secure_cookie("user")


    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return
        if self.simulate:
            self.render(self.absPath + '{0}static{0}html{0}index.html'.format(os.sep),
                        porta1='..{0}static{0}images{0}camera.png'.format(os.sep),
                        porta2='..{0}static{0}images{0}map.png'.format(os.sep),
                        wsType="wss://" if self._ssl else "ws://",
                        audioBufferLen=self._audioBufferLen)
        else:
            self.render(self.absPath + '{0}static{0}html{0}index.html'.format(os.sep),
                        porta1="http://"+self.cameraHost+":"+str(self.cameraPort)+"/?ac",
                        porta2="http://"+self.mapHost+":"+str(self.mapPort)+"/?ac",
                        wsType="wss://" if self._ssl else "ws://",
                        audioBufferLen=self._audioBufferLen)
