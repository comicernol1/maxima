import os,tornado.web,tornado.ioloop
from handlers import HomeHand,ContactHand,SignInHand,SignUpHand,VerifyHand
from settings import settings

if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", HomeHand),
        (r"/contact/", ContactHand),
        (r"/sign_in/", SignInHand),
        (r"/sign_up/", SignUpHand),
        (r"/verify/", VerifyHand)
    ], **settings)

    app.listen(80)
    tornado.ioloop.IOLoop.current().start()
