import os,tornado.web,tornado.ioloop,MaximaBranch
from settings import settings

if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/.*", MaximaBranch)
    ], **settings)

    app.listen(80)
    print(tornado.web.RequestHandler.path_args)
    tornado.ioloop.IOLoop.current().start()
