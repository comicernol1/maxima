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
                        VerifyIndex = VerifyIndex.replace("<% VerificationMsg %>","Your Email has been verified")
                        self.write(VerifyIndex)
                    else:
                        VerifyIndex = VerifyIndex.replace("<% VerificationMsg %>","(V1) This account could not be found")
                        self.write(VerifyIndex)
                else:
                    VerifyIndex = VerifyIndex.replace("<% VerificationMsg %>","This Email is already verified")
                    self.write(VerifyIndex)
            else:
                VerifyIndex = VerifyIndex.replace("<% VerificationMsg %>","(V2) This account could not be found")
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
                    VerifyIndex = VerifyIndex.replace("<% VerificationMsg %>","This link is invalid")
                    self.write(VerifyIndex)
        else:
            self.redirect("/sign_in/")
        """
        VerifyIndex = ServePage(self,"/sign_up/verified.html")
        def VerifyEmail(uid,tmpcode):
            VENewToken = random.randint(1000000000,9999999999)
            self.set_cookie("Ft",str(VENewToken))
            VERequestDBUpdate = "UPDATE compacc SET veremail=1,token='{0:d}' WHERE userid='{1:d}' and tmpcode='{2:d}'".format(VENewToken,int(uid),int(tmpcode))
            mycursor.execute(VERequestDBUpdate)
            if mycursor.rowcount >= 1:
                return True
            else:
                return False
            db.commit()
        
        try:
            if self.get_cookie("Fu"):
                VerifyTmpCode = int(self.get_query_argument("e"))
                self.set_cookie("Fv",str(VerifyTmpCode))
                if VerifyEmail(int(self.get_cookie("Fu")),VerifyTmpCode):
                    VerifyIndex = VerifyIndex.replace("<% VerificationMsg %>","(Vr1) Your email has been verified")
                    self.write(VerifyIndex)
                else:
                    VerifyIndex = VerifyIndex.replace("<% VerificationMsg %>","(Ve1) This account could not be found")
                    self.write(VerifyIndex)
            else:
                self.redirect("/sign_in/")
        except tornado.web.MissingArgumentError:
            if self.get_cookie("Fu") and self.get_cookie("Fv"):
                if VerifyEmail(int(self.get_cookie("Fu")),int(self.get_cookie("Fv"))):
                    VerifyIndex = VerifyIndex.replace("<% VerificationMsg %>","(Vr2) Your email has been verified")
                    self.write(VerifyIndex)
                else:
                    VerifyIndex = VerifyIndex.replace("<% VerificationMsg %>","(Ve2) This account could not be found")
                    self.write(VerifyIndex)
            else:
                VerifyIndex = VerifyIndex.replace("<% VerificationMsg %>","(V1) Something went wrong")
                self.write(VerifyIndex)
        """
    
    def post(self):
        SetCookie(self)
