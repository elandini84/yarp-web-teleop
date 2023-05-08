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
        self.render(self.absPath, usrLabel="User name", userName="", pwdLabel="Password", pwdStatus="", secondaryBtnState="secondary-hidden")


    def post(self):
        dbCheck = self.checkPassword(self.get_argument("name"),self.get_argument("password"))
        if dbCheck == LOGIN_OK:
            self.set_secure_cookie("user", self.get_argument("name"))
            self.set_secure_cookie("pw", self.get_argument("password"))
            self._aur.addUser(self.get_argument("name"))
            self.redirect("/")
        elif dbCheck == UNKNOWN_USER:
            self.render(self.absPath, usrLabel="Unknown user. Go to the \"Register\" page", userName="", pwdLabel="Password", pwdStatus="unknown_input", secondaryBtnState="secondary-visible")
        else:
            self.render(self.absPath, usrLabel="User name", userName=self.get_argument("name"), pwdLabel="Password: Wrong password. Try again", pwdStatus="error_input", secondaryBtnState="secondary-hidden")
