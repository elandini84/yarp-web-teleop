from .BaseLogHandler import *
from .AUR import ActiveUsersRegister

class LoginHandler(BaseLogHandler):

    def initialize(self, absPath, aur, myPage="/static/html/login.html", my_db=None):
        BaseLogHandler.initialize(self, absPath, myPage, my_db)
        if not isinstance(aur,ActiveUsersRegister):
            raise TypeError("aur parameter has to be an ActiveUserRegister object")
        self._aur = aur

    def get(self):
        if self.current_user:
            self.redirect("/")
            return
        self.render(self.absPath, userName="", pwdLabel="Password", pwdStatus="")


    def post(self):
        dbCheck = self.checkPassword(self.get_argument("name"),self.get_argument("password"))
        if dbCheck == LOGIN_OK:
            self.set_secure_cookie("user", self.get_argument("name"))
            self.set_secure_cookie("pw", self.get_argument("password"))
            self._aur.addUser(self.get_argument("name"))
            self.redirect("/")
        elif dbCheck == UNKNOWN_USER:
            self.redirect("/register")
        else:
            self.render(self.absPath, userName=self.get_argument("name"), pwdLabel="Password: Wrong password. Try again", pwdStatus="error_input")
