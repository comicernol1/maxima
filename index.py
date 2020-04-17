import os,tornado.web,tornado.ioloop,MaximaBranch
from settings import settings

if __name__ == "__main__":
    """
    app = tornado.web.Application([
        (r'/.*', MaximaBranch.handler)
    ], **settings)
    """
    app = tornado.web.Application([
    (HostMatches(r'(localhost|127\.0\.0\.1)'),
        [('/.*', MaximaBranch.handler)]),
    ])

    app.listen(80)
    tornado.ioloop.IOLoop.current().start()
