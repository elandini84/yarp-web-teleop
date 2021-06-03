import tornado.ioloop
import tornado.web
import json
import os

class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

path = os.path.join(os.getcwd())
if __name__ == "__main__":
    application = tornado.web.Application(
        [
            (r'/', HomeHandler),
            (r'/(.*\..*)', tornado.web.StaticFileHandler, {'path': path})
        ],
        template_path=os.path.dirname(__file__),
        debug=True
    )
    application.listen(16001)
    tornado.ioloop.IOLoop.current().start()