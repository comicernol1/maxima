import os,tornado.web,tornado.ioloop
import HomeHand,AboutHand,ContactHand
import SignInHand,ForgotPWHand,ResetPWHand
import SignUpHand,VerifyHand
import AccountHand,ChangeLocalesAjax
import ProductHand,CartHand
import AddToCartAjax,RefreshCartAjax
import TestingHand
import InfoHand
from settings import settings

if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", HomeHand.handler),
        (r"/about_us/", AboutHand.handler),
        (r"/contact/", ContactHand.handler),
        (r"/sign_in/", SignInHand.handler),
        (r"/sign_in/forgot_password/", ForgotPWHand.handler),
        (r"/sign_in/reset_password/", ResetPWHand.handler),
        (r"/sign_up/", SignUpHand.handler),
        (r"/verify/", VerifyHand.handler),
        (r"/account/", AccountHand.handler),
        (r"/account/locales/", ChangeLocalesAjax.handler),
        (r"/product/.*", ProductHand.handler),
        (r"/cart/", CartHand.handler),
        (r"/legal/terms_and_conditions/", InfoHand.TermsConditions),
        (r"/report_a_counterfeit/", InfoHand.Counterfeit),
        (r"/add_to_cart/", AddToCartAjax.handler),
        (r"/refresh_cart/", RefreshCartAjax.handler),
        (r"/test/", TestingHand.handler),
        (r"/.*", InfoHand.NotFound)
        print(tornado.web.RequestHandler.path_args)
    ], **settings)

    app.listen(80)
    tornado.ioloop.IOLoop.current().start()
