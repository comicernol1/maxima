import os
import tornado.web
import tornado.ioloop
from tornado.routing import HostMatches
from settings import settings

import kelimart
import franzar

class RedirectRemoveWWW(tornado.web.RequestHandler):
    def prepare(self):
        self.redirect("https://kelimart.com"+self.request.uri)

if __name__ == "__main__":
    app = tornado.web.Application([
        # (HostMatches(r'(localhost|127\.0\.0\.1)'), []),
        (HostMatches("kelimart.com"), [
            (r"/about_us/", kelimart.AboutHand.handler),
            (r"/account/", kelimart.AccountHand.handler),
            (r"/add_to_cart/", kelimart.AddToCartAjax.handler),
            (r"/cart/", kelimart.CartHand.handler),
            (r"/account/locales/", kelimart.ChangeLocalesAjax.handler),
            (r"/contact/", kelimart.ContactHand.handler),
            (r"/sign_in/forgot_password/", kelimart.ForgotPWHand.handler),
            (r"/", kelimart.HomeHand.handler),
            (r"/legal/terms_and_conditions/", kelimart.InfoHand.TermsConditions),
            (r"/report_a_counterfeit/", kelimart.InfoHand.Counterfeit),
            (r"/product/.*", kelimart.ProductHand.handler),
            (r"/refresh_cart/", kelimart.RefreshCartAjax.handler),
            (r"/sign_in/reset_password/", kelimart.ResetPWHand.handler),
            (r"/sign_in/", kelimart.SignInHand.handler),
            (r"/sign_up/", kelimart.SignUpHand.handler),
            (r"/test/", kelimart.TestingHand.handler),
            (r"/verify/", kelimart.VerifyHand.handler),
            (r"/.*", kelimart.InfoHand.NotFound)
        ]),
        (HostMatches("www.kelimart.com"), [
            (r"/.*", RedirectRemoveWWW)
        ]),
        
        """
        (HostMatches("company.kelimart.com"), [
            (r"/", company_kelimart.HomeHand.handler)
        ]),
        (HostMatches("www.company.kelimart.com"), [
            (r"/.*", RedirectRemoveWWW)
        ]),
        """
        
        (HostMatches("franzar.com"), [
            (r"/", franzar.HomeHand.handler)
        ]),
        (HostMatches("www.franzar.com"), [
            (r"/.*", RedirectRemoveWWW)
        ])
    ], **settings)

    app.listen(80)
    tornado.ioloop.IOLoop.current().start()
