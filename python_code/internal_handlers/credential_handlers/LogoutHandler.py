from .BaseLogHandler import *

class LogoutHandler(BaseLogHandler):


    def post(self):
        if self._aur.removeUser(self.current_user.decode()) == LOGOUT_OK:
            self.clear_cookie("user")
            self.clear_cookie("pw")
            self.redirect("/login")
        else:
            self.render(self.absPath,user="{0}".format(self.current_user.decode()),logStatus="error_look")


    def initialize(self, absPath, aur, myPage="/static/html/logout.html", my_db=None):
        BaseLogHandler.initialize(self, absPath, aur, myPage, my_db)

    def get(self):
        self.render(self.absPath,user="{0}".format(self.current_user.decode()),logStatus="")
