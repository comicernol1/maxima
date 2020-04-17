import os,tornado.web,tornado.ioloop
from tornado.routing import HostMatches
import kelimart.HomeHand
import franzar.HomeHand
from settings import settings

if __name__ == "__main__":
    """
    app = tornado.web.Application([
        (r'/.*', MaximaBranch.handler)
    ], **settings)
    """
    app = tornado.web.Application([
        (HostMatches("kelimart.com"), [
            (r"/", kelimart.HomeHand.handler)
        ]),
        (HostMatches("franzar.com"), [
            (r"/", franzar.HomeHand.handler)
        ])
    ], **settings)

    app.listen(80)
    tornado.ioloop.IOLoop.current().start()
