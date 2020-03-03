import os,tornado.web,tornado.ioloop
from handlers import FranzarHomeHand,FranzarSignInHand,FranzarSignUpHand
from settings import settings

if __name__ == "__main__":
    app = tornado.web.Application([
        (HostMatches("kelimart.com"), [
            (r"/", FranzarHomeHand),
            (r"/sign_in/", FranzarSignInHand),
            (r"/sign_up/", FranzarSignUpHand)
        ]),
        (HostMatches("selvetti.com"), [
            (r"/", SelvettiHomeHand),
            (r"/sign_in/", SelvettiSignInHand),
            (r"/sign_up/", SelvettiSignUpHand)
        ])
    ], **settings)

    app.listen(80)
    tornado.ioloop.IOLoop.current().start()
