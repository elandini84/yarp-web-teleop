from tornado.web import RequestHandler

class AuthHandler(RequestHandler) :

    def get(self):
        if not self.current_user:
            self.set_status(401, "User not logged in")
            self.set_header("Prova header", "Error")
        else:
            self.set_status(200, "User correctly logged in")
            self.set_header("Prova header", "Ok")

        self.finish()


    def get_current_user(self):
        return self.get_secure_cookie("user")

