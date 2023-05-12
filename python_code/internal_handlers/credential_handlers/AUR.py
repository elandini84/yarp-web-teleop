from datetime import datetime
from .AliasesAndConstants import *

class ActiveUsersRegister(object):

    def __init__(self,verbose=False,execLog=False):

        if execLog:
            print("ActiveUserRegister.__init__ called at: {0}".format(datetime.now()))

        self._activeUsers = {}
        self._execLog = execLog
        self._verbose = verbose


    def addUser(self, userName):
        if self._execLog:
            print("ActiveUserRegister.addUser(self, {1}) called at: {0}".format(datetime.now(),userName))
        temp = datetime.now()
        if userName in self._activeUsers.keys():
            if self._verbose:
                print("User {0} has already logged at: {1}".format(userName,self._activeUsers[userName]))
            return ALREADY_LOGGED

        self._activeUsers[userName] = temp
        if self._verbose:
            print("Current users: {0}".format(self._activeUsers))


    def removeUser(self,userName):
        if self._execLog:
            print("ActiveUserRegister.removeUser(self, {1}) called at: {0}".format(datetime.now(),userName))
        if userName not in self._activeUsers.keys():
            return NOT_LOGGED
        del self._activeUsers[userName]
        return LOGOUT_OK
