from .BaseLogHandler import *

class RegisterHandler(BaseLogHandler):

    def initialize(self, absPath, myPage="/static/html/register.html", my_db=None):
        BaseLogHandler.initialize(self, absPath, myPage, my_db)

    def get(self):
        self.render(self.absPath,logaction = "Log out" if self.current_user else "Log in")


    def post(self):
        if not self.checkUser(self.get_argument("name")):
            query = ['''INSERT INTO users (id, name, password) VALUES (?,?,?)''',(self.countUsers()+1,self.get_argument("name"),self.get_argument("password"))]
            cursor = self.my_db.cursor()
            cursor.execute(*query)
            self.my_db.commit()
        self.redirect("/login")
