import os,tornado.web,tornado.ioloop
import HomeHand,ContactHand
import SignInHand,ForgotPWHand,ResetPWHand
import SignUpHand,VerifyHand
import AccountHand
import ProductHand,CartHand
import TermsConditionsHand,CounterfeitHand
import AddToCartAjax,RefreshCartAjax
import TestingHand
import NotFoundHand
from settings import settings

if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", HomeHand.handler),
        (r"/contact/", ContactHand.handler),
        (r"/sign_in/", SignInHand.handler),
        (r"/sign_in/forgot_password/", ForgotPWHand.handler),
        (r"/sign_in/reset_password/", ResetPWHand.handler),
        (r"/sign_up/", SignUpHand.handler),
        (r"/verify/", VerifyHand.handler),
        (r"/account/", AccountHand.handler),
        (r"/product/.*", ProductHand.handler),
        (r"/cart/", CartHand.handler),
        (r"/legal/terms_and_conditions/", TermsConditionsHand.handler),
        (r"/report_a_counterfeit/", CounterfeitHand.handler),
        (r"/add_to_cart/", AddToCartAjax.handler),
        (r"/refresh_cart/", RefreshCartAjax.handler),
        (r"/test/", TestingHand.handler),
        (r"/.*", NotFoundHand.handler)
    ], **settings)

    app.listen(80)
    tornado.ioloop.IOLoop.current().start()
