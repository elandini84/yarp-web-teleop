from datetime import datetime

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
        temp = [datetime.now()]
        if userName not in self._activeUsers.keys():
            self._activeUsers[userName] = temp
        else:
            self._activeUsers[userName] = temp + self._activeUsers[userName]
        if self._verbose:
            print("Current users: {0}".format(self._activeUsers))