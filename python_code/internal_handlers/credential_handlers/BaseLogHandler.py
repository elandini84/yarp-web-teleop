from tornado.web import RequestHandler

class BaseLogHandler(RequestHandler):

    def initialize(self, absPath, myPage, my_db=None):
        self.my_db = my_db
        self.absPath = absPath + "/" + myPage


    def getAllFromQuery(self, query):

        cursor = self.my_db.cursor()
        cursor.execute(*query)
        result = cursor.fetchall()

        print(result)

        return result


    def get_current_user(self):
        return self.get_secure_cookie("user")


    def get_user_pw(self):
        return self.get_secure_cookie("pw")


    def getAllUsers(self):
        names = self.getAllFromQuery(['''SELECT name FROM users'''])

        return names


    def checkUser(self,name):
        names = self.getAllUsers()
        response = False

        for data in names:
            response = response or name in data

        return response


    def getEntry(self, name):
        if not self.checkUser(name):
            print(self.getAllFromQuery(['''SELECT * FROM users WHERE name=?''', (name,)]))
            return None
        entry = self.getAllFromQuery(['''SELECT * FROM users WHERE name=?''', (name,)])

        return entry


    def checkPassword(self, name, pw):
        userEntry = self.getEntry(name)
        if userEntry is not None:
            return pw == userEntry[0][2]
        return False


    def countUsers(self):
        return len(self.getAllUsers())
