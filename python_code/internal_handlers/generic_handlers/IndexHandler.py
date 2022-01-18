from tornado.web import RequestHandler
import os

class IndexHandler(RequestHandler):

    def initialize(self,inputNetwork,cameraPort,mapPort,cameraHost,resFinder,absPath,mapHost=None,simulate=False):
        self.yarpNet = inputNetwork
        self.cameraPort = cameraPort
        self.cameraHost = cameraHost
        self.mapPort = mapPort
        self.mapHost = mapHost if mapHost is not None else cameraHost
        self.resFinder = resFinder
        self.absPath = absPath
        self.simulate = simulate


    def get_current_user(self):
        return self.get_secure_cookie("user")


    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return
        if self.simulate:
            self.render(self.absPath + '{0}static{0}html{0}index.html'.format(os.sep),
                        porta1="https://cdn.pixabay.com/photo/2021/04/28/21/59/kingfisher-6215073_960_720.jpg",
                        porta2="https://cdn.pixabay.com/photo/2021/04/28/21/59/kingfisher-6215073_960_720.jpg")
        else:
            self.render(self.absPath + '{0}static{0}html{0}index.html'.format(os.sep),
                        porta1="http://"+self.cameraHost+":"+str(self.cameraPort)+"/?ac",
                        porta2="http://"+self.mapHost+":"+str(self.mapPort)+"/?ac")
