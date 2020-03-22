import handlers,os,tornado.web,tornado.ioloop
from settings import settings

if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", handlers.HomeHand),
        (r"/contact/", handlers.ContactHand),
        (r"/sign_in/", handlers.SignInHand),
        (r"/sign_in/forgot_password/", handlers.ForgotPWHand),
        (r"/sign_in/reset_password/", handlers.ResetPWHand),
        (r"/sign_up/", handlers.SignUpHand),
        (r"/verify/", handlers.VerifyHand),
        (r"/terms_and_conditions/", handlers.TermsConditionsHand),
        (r"/.*", handlers.NotFoundHand)
    ], **settings)

    app.listen(80)
    tornado.ioloop.IOLoop.current().start()
