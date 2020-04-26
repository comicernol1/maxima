import os
import tornado.web
import tornado.ioloop
from tornado.routing import HostMatches
from settings import settings

import franzar.AboutHand
import franzar.AccountHand
import franzar.AddToCartAjax
import franzar.CartHand
import franzar.ChangeLocalesAjax
import franzar.ContactHand
import franzar.ForgotPWHand
import franzar.HomeHand
import franzar.InfoHand
import franzar.ProductHand
import franzar.RefreshCartAjax
import franzar.ResetPWHand
import franzar.SignInHand
import franzar.SignUpHand
import franzar.TestingHand
import franzar.VerifyHand

import kelimart.HomeHand

class RedirectRemoveWWW_Franzar(tornado.web.RequestHandler):
    def prepare(self):
        self.redirect("https://franzar.com"+self.request.uri)

class RedirectRemoveWWW_Kelimart(tornado.web.RequestHandler):
    def prepare(self):
        self.redirect("https://kelimart.com"+self.request.uri)

if __name__ == "__main__":
    app = tornado.web.Application([
        # (HostMatches(r'(localhost|127\.0\.0\.1)'), []),
        (HostMatches("franzar.com"), [
            (r"/about_us/", franzar.AboutHand.handler),
            (r"/account/", franzar.AccountHand.handler),
            (r"/add_to_cart/", franzar.AddToCartAjax.handler),
            (r"/cart/", franzar.CartHand.handler),
            (r"/account/locales/", franzar.ChangeLocalesAjax.handler),
            (r"/contact/", franzar.ContactHand.handler),
            (r"/sign_in/forgot_password/", franzar.ForgotPWHand.handler),
            (r"/", franzar.HomeHand.handler),
            (r"/legal/terms_and_conditions/", franzar.InfoHand.TermsConditions),
            (r"/report_a_counterfeit/", franzar.InfoHand.Counterfeit),
            (r"/deliveries_and_returns/", franzar.InfoHand.Returns),
            (r"/product/.*", franzar.ProductHand.handler),
            (r"/refresh_cart/", franzar.RefreshCartAjax.handler),
            (r"/sign_in/reset_password/", franzar.ResetPWHand.handler),
            (r"/sign_in/", franzar.SignInHand.handler),
            (r"/sign_up/", franzar.SignUpHand.handler),
            (r"/test/", franzar.TestingHand.handler),
            (r"/verify/", franzar.VerifyHand.handler),
            (r"/.*", franzar.InfoHand.NotFound)
        ]),
        (HostMatches("www.franzar.com"), [
            (r"/.*", RedirectRemoveWWW_Franzar)
        ]),
        (HostMatches("kelimart.com"), [
            (r"/", kelimart.HomeHand.handler)
        ]),
        (HostMatches("www.kelimart.com"), [
            (r"/.*", RedirectRemoveWWW_Kelimart)
        ])
    ], **settings)

    app.listen(80)
    tornado.ioloop.IOLoop.current().start()
