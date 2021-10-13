from .BaseLogHandler import *

class LogoutHandler(BaseLogHandler):

    def get(self):
        self.write('<html><body><form action="/logout" method="post">'
                   'Name: {0}'
                   '<br/>'
                   '<input type="submit" value="Log out">'
                   '</form></body></html>'.format(self.current_user))


    def post(self):
        self.clear_cookie("user")
        self.clear_cookie("pw")
        self.redirect("/login")