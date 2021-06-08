import tornado.ioloop
import tornado.web
#from yarp import Port, Network, Bottle
import json
import os

ABSPATH = os.path.dirname(os.path.realpath(__file__))

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(ABSPATH + '{0}static{0}html{0}index.html'.format(os.sep),
                    porta1 = "192.168.1.12:10006",
                    porta2 = "192.168.1.12:10005")


if __name__ == "__main__":
    application = tornado.web.Application(
        [
            (r'/', IndexHandler),
            (r"/static/(.*)", tornado.web.StaticFileHandler,{'path':'static'})
        ],
        template_path=os.path.dirname(__file__),
        debug=True
    )
    application.listen(16001)
    tornado.ioloop.IOLoop.current().start()