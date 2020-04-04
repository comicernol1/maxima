from udf import *

class handler(tornado.web.RequestHandler):
    def get(self):
        VerifyIndex = ServePage(self,"/sign_up/verified.html")
        
        def VerifyEmail(uid,tmpcode):
            VE_uid=int(uid)
            VE_tmpcode=int(tmpcode)
            VE_token = random.randint(1000000000,9999999999)
            self.set_cookie("Ft",str(VE_token))
            VERequestDBUpdate = "UPDATE compacc SET veremail=1,token={0:d} WHERE userid={1:d} and tmpcode={2:d}".format(VE_token,VE_uid,VE_tmpcode)
            print(VE_uid)
            print(VE_tmpcode)
            mycursor.execute(VERequestDBUpdate)
            if mycursor.rowcount >= 1:
                return True
            else:
                return False
            db.commit()
        
        if self.get_cookie("Fu"):
            UserInfoFu = int(self.get_cookie("Fu"))
            try:
                VerifyTmpCode = int(self.get_query_argument("e"))
                self.set_cookie("Fv",str(VerifyTmpCode))
                VerifyEmail(UserInfoFu,VerifyTmpCode)
                VerifyIndex = VerifyIndex.replace("<% VerificationMsg %>",str(VerifyTmpCode))
                self.write(VerifyIndex)
            except tornado.web.MissingArgumentError:
                if self.get_cookie("Fv"):
                    VerifyTmpCode = int(self.get_cookie("Fv"))
                    VerifyEmail(UserInfoFu,VerifyTmpCode)
                    VerifyIndex = VerifyIndex.replace("<% VerificationMsg %>",str(VerifyTmpCode))
                    self.write(VerifyIndex)
                else:
                    VerifyIndex = VerifyIndex.replace("<% VerificationMsg %>","E Empty")
                    self.write(VerifyIndex)
        else:
            VerifyIndex = VerifyIndex.replace("<% VerificationMsg %>","PROBLEM")
            self.write(VerifyIndex)
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
