from .BaseLogHandler import *

class RegisterHandler(BaseLogHandler):

    def initialize(self, absPath, myPage="/static/html/register.html", my_db=None,adminkey=None):
        BaseLogHandler.initialize(self, absPath, myPage, my_db)
        self._adminKey = "" if adminkey is None else adminkey

    def get(self):
        self.render(self.absPath,logaction = "Log out" if self.current_user else "Log in",loglink = "logout" if self.current_user else "login")


    def post(self):
        if not self.checkUser(self.get_argument("name")):
            if len(self.get_argument("password")) <= 0:
                self.redirect("/register")
                return
            if self.get_argument("admin_key") != self._adminKey and self._adminKey != "":
                self.redirect("/register")
                return
            query = ['''INSERT INTO users (id, name, password) VALUES (?,?,?)''',(self.countUsers()+1,self.get_argument("name"),self.get_argument("password"))]
            cursor = self.my_db.cursor()
            cursor.execute(*query)
            self.my_db.commit()
        self.redirect("/login")
