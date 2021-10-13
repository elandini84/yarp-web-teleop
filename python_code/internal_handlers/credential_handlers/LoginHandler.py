from .BaseLogHandler import *

class LoginHandler(BaseLogHandler):

    def get(self):
        self.write('<html><body><form action="/login" method="post">'
                   'Name: <input type="text" name="name">'
                   '<br/>'
                   'Password: <input type="password" name="passw">'
                   '<input type="submit" value="Sign in">'
                   '</form></body></html>')


    def post(self):
        if self.checkPassword(self.get_argument("name"),self.get_argument("passw")):
            self.set_secure_cookie("user", self.get_argument("name"))
            self.set_secure_cookie("pw", self.get_argument("passw"))
            self.redirect("/")
        else:
            self.redirect("/register")