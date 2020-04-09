from udf import *

class handler(tornado.web.RequestHandler):
    def get(self):
        UserLanguagesUnclean = re.split(" |,|;",self.request.headers.get("Accept-Language"))
        UserLanguages = []
        for i in UserLanguagesUnclean:
            if len(i) == 2:
                UserLanguages.append(i)
        self.write(str(UserLanguages))
        # VerifyIndex = ServePage(self,"/sign_up/verified.html",False)
        # VerifyIndex = VerifyIndex.replace("<% VerificationMsg %>","<div id=\"rg_block\" hg=\"ue\">This Email is already verified</div>")
        # self.write(VerifyIndex)
    
    def post(self):
        SetCookie(self)
