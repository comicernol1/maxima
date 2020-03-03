import os,tornado.web,tornado.ioloop
from handlers import HomeHand,SignInHand,SignUpHand
from settings import settings

if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", HomeHand),
        (r"/sign_in/", SignInHand),
        (r"/sign_up/", SignUpHand)
    ], **settings)

    app.listen(80)
    tornado.ioloop.IOLoop.current().start()
