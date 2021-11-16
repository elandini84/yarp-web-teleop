from .BaseLogHandler import *

class LogoutHandler(BaseLogHandler):


    def post(self):
        self.clear_cookie("user")
        self.clear_cookie("pw")
        self.redirect("/login")

    def initialize(self, absPath, myPage="/static/html/logout.html", my_db=None):
        BaseLogHandler.initialize(self, absPath, myPage, my_db)

    def get(self):
        self.render(self.absPath,user="{0}".format(self.current_user))
        #self.write('<html><body><form action="/logout" method="post">'
        #           'Name: {0}'
        #           '<br/>'
        #           '<input type="submit" value="Log out">'
        #           '</form></body></html>'.format(self.current_user))
