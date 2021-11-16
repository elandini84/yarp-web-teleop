from .BaseLogHandler import *

class LoginHandler(BaseLogHandler):

    def initialize(self, absPath, myPage="/static/html/login.html", my_db=None):
        BaseLogHandler.initialize(self, absPath, myPage, my_db)

    def get(self):
        if self.current_user:
            self.redirect("/")
        self.render(self.absPath)
#        self.write('<html><body><form action="/login" method="post">'
#                   'Name: <input type="text" name="name">'
#                   '<br/>'
#                   'Password: <input type="password" name="passw">'
#                   '<input type="submit" value="Sign in">'
#                   '</form></body></html>')


    def post(self):
        print("Got: {0} - {1}".format(self.get_argument("name"),self.get_argument("password")))
        if self.checkPassword(self.get_argument("name"),self.get_argument("password")):
            self.set_secure_cookie("user", self.get_argument("name"))
            self.set_secure_cookie("pw", self.get_argument("password"))
            self.redirect("/")
        else:
            self.redirect("/register")
