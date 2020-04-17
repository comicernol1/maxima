import os,tornado.web,tornado.ioloop,MaximaBranch
from settings import settings

if __name__ == "__main__":
    app = tornado.web.Application(r'(localhost|127\.0\.0\.1)', [
        (r'/.*', MaximaBranch.handler)
    ], **settings)

    app.listen(80)
    tornado.ioloop.IOLoop.current().start()
