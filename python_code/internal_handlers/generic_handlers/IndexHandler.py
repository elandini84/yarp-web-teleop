from tornado.web import RequestHandler
import os

class IndexHandler(RequestHandler):

    def initialize(self,inputNetwork,cameraPort,mapPort,resFinder,absPath):
        self.yarpNet = inputNetwork
        self.cameraPort = cameraPort
        self.mapPort = mapPort
        self.resFinder = resFinder
        self.absPath = absPath


    def get(self):
        contactCamera = self.yarpNet.queryName(self.resFinder.find("camera_port").asString() if self.resFinder.check("camera_port") else self.cameraPort)
        contactMap = self.yarpNet.queryName(self.resFinder.find("map_port").asString() if self.resFinder.check("map_port") else self.mapPort)
        self.render(self.absPath + '{0}static{0}html{0}index.html'.format(os.sep),
                    porta1 = contactCamera.getHost()+":"+str(contactCamera.getPort()),
                    porta2 = contactMap.getHost()+":"+str(contactMap.getPort()))