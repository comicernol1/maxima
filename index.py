import os,tornado.web,tornado.ioloop
from tornado.routing import HostMatches
import maxima.K_HomeHand
from settings import settings

if __name__ == "__main__":
    """
    app = tornado.web.Application([
        (r'/.*', MaximaBranch.handler)
    ], **settings)
    """
    app = tornado.web.Application([
        (HostMatches("kelimart.com"), [
            (r"/", K_HomeHand.handler)
        ]),
        (HostMatches("franzar.com"), [
            (r"/", F_HomeHand.handler)
        ])
    ], **settings)

    app.listen(80)
    tornado.ioloop.IOLoop.current().start()
