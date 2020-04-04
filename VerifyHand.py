from udf import *

class handler(tornado.web.RequestHandler):
    def get(self):
        def VerifyEmail(uid,tmpcode):
            VerifyIndex = ServePage(self,"/sign_up/verified.html")
            VE_uid=int(uid)
            VE_tmpcode=int(tmpcode)
            VE_RequestDBSelectVerEmail = "SELECT veremail FROM compacc WHERE userid='{0:d}'".format(VE_uid)
            mycursor.execute(VE_RequestDBSelectVerEmail)
            QueryVerEmailPre = mycursor.fetchone()
            if QueryVerEmailPre:
                if int(QueryVerEmailPre[0]) != 1:
                    VE_token = random.randint(1000000000,9999999999)
                    self.set_cookie("Ft",str(VE_token))
                    VE_RequestDBUpdate = "UPDATE compacc SET veremail='1',tmpcode='',token='{0:d}' WHERE userid='{1:d}' and tmpcode='{2:d}'".format(VE_token,VE_uid,VE_tmpcode)
                    mycursor.execute(VE_RequestDBUpdate)
                    db.commit()
                    if mycursor.rowcount >= 1:
                        VE_AddRulerToCart = "INSERT INTO cart (uid,pid,qty) VALUES('{0:d}','11111110',1)".format(VE_uid)
                        mycursor.execute(VE_AddRulerToCart)
                        db.commit()
                        VerifyIndex = VerifyIndex.replace("<% VerificationMsg %>","<div id=\"rg_block\" hg=\"uc\"><h1>Welcome to Franzar!</h1><div id=\"suc_i\"></div><h3>As a sign of appreciation for making it this far, we've added a FREE tailor's ruler to your cart. You'll need this if you want to order custom tailored clothes from us. To see your cart, you can click the button below or the shopping cart icon in the top-right corner.</h3><a href=\"/cart/\"><button class=\"rgsb\" id=\"Vuc_L\">Open Cart</button></a></div>")
                        self.write(VerifyIndex)
                    else:
                        VerifyIndex = VerifyIndex.replace("<% VerificationMsg %>","<div id=\"rg_block\" hg=\"ue\">(V1) This account could not be found</div>")
                        self.write(VerifyIndex)
                else:
                    VerifyIndex = VerifyIndex.replace("<% VerificationMsg %>","<div id=\"rg_block\" hg=\"ue\">This Email is already verified</div>")
                    self.write(VerifyIndex)
            else:
                VerifyIndex = VerifyIndex.replace("<% VerificationMsg %>","<div id=\"rg_block\" hg=\"ue\">(V2) This account could not be found</div>")
                self.write(VerifyIndex)
        
        if self.get_cookie("Fu"):
            UserInfoFu = int(self.get_cookie("Fu"))
            try:
                VerifyTmpCode = int(self.get_query_argument("e"))
                self.set_cookie("Fv",str(VerifyTmpCode))
                VerifyEmail(UserInfoFu,VerifyTmpCode)
            except tornado.web.MissingArgumentError:
                if self.get_cookie("Fv"):
                    VerifyTmpCode = int(self.get_cookie("Fv"))
                    VerifyEmail(UserInfoFu,VerifyTmpCode)
                else:
                    VerifyIndex = ServePage(self,"/sign_up/verified.html")
                    VerifyIndex = VerifyIndex.replace("<% VerificationMsg %>","<div id=\"rg_block\" hg=\"ue\">This link is invalid</div>")
                    self.write(VerifyIndex)
        else:
            self.redirect("/sign_in/")
    
    def post(self):
        SetCookie(self)
