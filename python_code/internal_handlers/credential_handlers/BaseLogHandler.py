from tornado.web import RequestHandler
from .AUR import *

class BaseLogHandler(RequestHandler):

    def initialize(self, absPath, aur, myPage, my_db=None):
        self.my_db = my_db
        self.absPath = absPath + "/" + myPage
        if not isinstance(aur,ActiveUsersRegister):
            raise TypeError("aur parameter has to be an ActiveUserRegister object")
        self._aur = aur


    def getAllFromQuery(self, query):

        cursor = self.my_db.cursor()
        cursor.execute(*query)
        result = cursor.fetchall()

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
            return None
        entry = self.getAllFromQuery(['''SELECT * FROM users WHERE name=?''', (name,)])

        return entry


    def checkPassword(self, name, pw):
        userEntry = self.getEntry(name)
        if userEntry is not None:
            return LOGIN_OK if pw == userEntry[0][2] else WRONG_PWD
        return UNKNOWN_USER


    def countUsers(self):
        return len(self.getAllUsers())
