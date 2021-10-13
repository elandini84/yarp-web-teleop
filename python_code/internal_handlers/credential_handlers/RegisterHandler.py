from .BaseLogHandler import *

class RegisterHandler(BaseLogHandler):

    def get(self):
        self.write('<html><body><form action="/register" method="post">'
                   'Name: <input type="text" name="name">'
                   '<br/>'
                   'Password: <input type="password" name="passw">'
                   '<input type="submit" value="Register">'
                   '</form></body></html>')


    def post(self):
        if not self.checkUser(self.get_argument("name")):
            query = ['''INSERT INTO users (id, name, password) VALUES (?,?,?)''',(self.countUsers()+1,self.get_argument("name"),self.get_argument("passw"))]
            cursor = self.my_db.cursor()
            cursor.execute(*query)
            self.my_db.commit()
        self.redirect("/login")