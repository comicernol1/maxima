from udf import *

class handler(tornado.web.RequestHandler):
    def get(self):
        # Open
        ResetPWIndex = ServePage(self,"/sign_in/reset_pw.html")
        ResetPWMsgIndex = ServePage(self,"/sign_in/reset_pw_msg.html")
        
        # Test
        try:
            ResetPWRequestE = int(self.get_query_argument("e"))
            ResetPWRequestTempID = int(self.get_query_argument("id"))
            ResetPWRequestDBSelectCode = "SELECT tmpcode,email,veremail FROM compacc WHERE userid='{0:d}'".format(ResetPWRequestE)
            mycursor.execute(ResetPWRequestDBSelectCode)
            QueryIDPre = mycursor.fetchone()
            if QueryIDPre:
                if QueryIDPre[0] is not None:
                    ResetPWQueryIDTemp = int(QueryIDPre[0])
                else:
                    ResetPWQueryIDTemp = ""
                if ResetPWQueryIDTemp == ResetPWRequestTempID:
                    if int(QueryIDPre[2]) != 1:
                        ResetPWRequestDBUpdate = "UPDATE compacc SET veremail='1' WHERE userid='{0:d}'".format(ResetPWRequestE)
                        mycursor.execute(ResetPWRequestDBUpdate)
                    ResetPWIndex = ResetPWIndex.replace("<% Email %>",str(QueryIDPre[1]))
                    ResetPWRequestDBTokenUpdate = "UPDATE compacc SET tmpcode=NULL,token=NULL WHERE userid='{0:d}'".format(ResetPWRequestE)
                    mycursor.execute(ResetPWRequestDBTokenUpdate)
                    db.commit()
                    self.set_cookie("Fu",str(ResetPWRequestE))
                    self.set_cookie("Ft","")
                    self.write(ResetPWIndex)
                else:
                    ResetPWMsgIndex = ResetPWMsgIndex.replace("<% Msg %>","This link has expired.")
                    self.write(ResetPWMsgIndex)
            else:
                ResetPWMsgIndex = ResetPWMsgIndex.replace("<% Msg %>","We can't find an account matching this link.")
                self.write(ResetPWMsgIndex)
        except tornado.web.MissingArgumentError:
            try:
                ResetPWCookieFu = int(self.get_cookie("Fu"))
                ResetPWRequestDBSelectCode = "SELECT email FROM compacc WHERE userid='{0:d}'".format(ResetPWCookieFu)
                mycursor.execute(ResetPWRequestDBSelectCode)
                QueryIDPre = mycursor.fetchone()
                if QueryIDPre:
                    ResetPWIndex = ResetPWIndex.replace("<% Email %>",str(QueryIDPre[0]))
                    ResetPWRequestDBTokenUpdate = "UPDATE compacc SET tmpcode=NULL,token=NULL WHERE userid='{0:d}'".format(ResetPWCookieFu)
                    mycursor.execute(ResetPWRequestDBTokenUpdate)
                    db.commit()
                    self.write(ResetPWIndex)
                else:
                    ResetPWMsgIndex = ResetPWMsgIndex.replace("<% Msg %>","(R1) Something went wrong. Please click on the link again.")
                    self.write(ResetPWMsgIndex)
            except:
                self.redirect("/sign_in/forgot_password/")
