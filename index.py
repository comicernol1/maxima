import os,tornado.web,tornado.ioloop
import K_HomeHand,F_HomeHand
from settings import settings

if __name__ == "__main__":
    """
    app = tornado.web.Application([
        (r'/.*', MaximaBranch.handler)
    ], **settings)
    """
    application = tornado.web.Application([
        (HostMatches("kelimart.com"), [
            (r"/", K_HomeHand.handler)
        ]),
        (HostMatches("franzar.com"), [
            (r"/", F_HomeHand.handler)
        ])
    ])

    app.listen(80)
    tornado.ioloop.IOLoop.current().start()
