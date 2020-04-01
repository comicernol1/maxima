import os,tornado.web,tornado.ioloop
from handlers import *
from settings import settings

if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", HomeHand),
        (r"/contact/", ContactHand),
        (r"/sign_in/", SignInHand),
        (r"/sign_in/forgot_password/", ForgotPWHand),
        (r"/sign_in/reset_password/", ResetPWHand),
        (r"/sign_up/", SignUpHand),
        (r"/verify/", VerifyHand),
        (r"/account/", AccountHand),
        (r"/product/.*", ProductHand),
        (r"/legal/terms_and_conditions/", TermsConditionsHand),
        (r"/legal/report_a_counterfeit/", CounterfeitHand),
        (r"/.*", NotFoundHand)
    ], **settings)

    app.listen(80)
    tornado.ioloop.IOLoop.current().start()
