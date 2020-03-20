import os,tornado.web,tornado.ioloop
from handlers import HomeHand,ContactHand,SignInHand,ForgotPWHand,SignUpHand,VerifyHand
from settings import settings

if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", HomeHand),
        (r"/contact/", ContactHand),
        (r"/sign_in/", SignInHand),
        (r"/forgot_password/", ForgotPWHand),
        (r"/sign_up/", SignUpHand),
        (r"/verify/", VerifyHand)
    ], **settings)

    app.listen(80)
    tornado.ioloop.IOLoop.current().start()
