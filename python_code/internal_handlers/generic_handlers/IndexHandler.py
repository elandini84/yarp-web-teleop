from tornado.web import RequestHandler
import os

class IndexHandler(RequestHandler):

    def initialize(self,inputNetwork,cameraPort,mapPort,cameraHost,resFinder,absPath,mapHost=None):
        self.yarpNet = inputNetwork
        self.cameraPort = cameraPort
        self.cameraHost = cameraHost
        self.mapPort = mapPort
        self.mapHost = mapHost if mapHost is not None else cameraHost
        self.resFinder = resFinder
        self.absPath = absPath


    def get_current_user(self):
        return self.get_secure_cookie("user")


    def get(self):
        contactCamera = self.yarpNet.queryName(self.resFinder.find("camera_port").asString() if self.resFinder.check("camera_port") else self.cameraPort)
        contactMap = self.yarpNet.queryName(self.resFinder.find("map_port").asString() if self.resFinder.check("map_port") else self.mapPort)
        if not self.current_user:
            self.redirect("/login")
            return
        self.render(self.absPath + '{0}static{0}html{0}index.html'.format(os.sep),
                    porta1 = self.cameraHost+":"+str(self.cameraPort),
                    porta2 = self.mapHost+":"+str(self.mapPort))