from udf import *

class handler(tornado.web.RequestHandler):
    def get(self):
        # Open
        ForgotPWIndex = ServePage(self,"/sign_in/forgot_pw.html",False)
        self.write(ForgotPWIndex)
    
    def post(self):
        # Open
        ForgotPWIndex = ServePage(self,"/sign_in/forgot_pw.html",False)
        ForgotPWConfIndex = ServePage(self,"/sign_in/forgot_pw_conf.html",False)
        
        # Test
        ForgotPWRequestBody = urllib.parse.unquote(self.request.body.decode('utf-8'))
        if ForgotPWRequestBody.find("fpem=") >= 0:
            ForgotPWRequestEmail = ForgotPWRequestBody[(ForgotPWRequestBody.index("fpem=")+5):len(ForgotPWRequestBody)]
            ForgotPWRequestDBSelectEmail = "SELECT userid FROM compacc WHERE email='{0:s}'".format(ForgotPWRequestEmail)
            mycursor.execute(ForgotPWRequestDBSelectEmail)
            QueryEmailPre = mycursor.fetchone()
            if QueryEmailPre:
                QueryEmailUserID = str(QueryEmailPre[0])
                
                # Send Password Reset Email
                with open("/root/maxima/templates/sign_in/password_reset_email.html") as ForgotPWSMTPTemplate_F:
                    ForgotPWSMTPTemplate = ForgotPWSMTPTemplate_F.read()
                ForgotPWSMTPTemplate = ForgotPWSMTPTemplate.replace("<% UserID %>",QueryEmailUserID)
                ForgotPWTempCode = random.randint(1000000000,9999999999)
                ForgotPWSMTPTemplate = ForgotPWSMTPTemplate.replace("<% TempCode %>",str(ForgotPWTempCode))
                ForgotPWRequestDBUpdate = "UPDATE compacc SET tmpcode='{0:d}' WHERE email='{1:s}'".format(ForgotPWTempCode,ForgotPWRequestEmail)
                mycursor.execute(ForgotPWRequestDBUpdate)
                db.commit()
                ForgotPWSMTPHeaders = "\r\n".join(["from: comicernol@gmail.com","subject: Reset Your Password - FRANZAR","to:"+ForgotPWRequestEmail,"mime-version: 1.0","content-type: text/html"])
                ForgotPWSMTPContent = ForgotPWSMTPHeaders+"\r\n\r\n"+ForgotPWSMTPTemplate
                ForgotPWMail = smtplib.SMTP('smtp.gmail.com',587)
                ForgotPWMail.ehlo()
                ForgotPWMail.starttls()
                ForgotPWMail.login('comicernol@gmail.com',str(os.environ["Comicernol_Gmail_Passwd"]))
                ForgotPWMail.sendmail('comicernol@gmail.com',ForgotPWRequestEmail,ForgotPWSMTPContent)
                ForgotPWMail.close()
                ForgotPWConfIndex = ForgotPWConfIndex.replace("<% ShowError %>","none")
                ForgotPWConfIndex = ForgotPWConfIndex.replace("<% ErrorMsg %>","")
                ForgotPWConfIndex = ForgotPWConfIndex.replace("<% Email %>",ForgotPWRequestEmail)
                self.write(ForgotPWConfIndex)
            else:
                ForgotPWIndex = ForgotPWIndex.replace("<% ShowError %>","block")
                ForgotPWIndex = ForgotPWIndex.replace("<% ErrorMsg %>","Account does not exist")
                self.write(ForgotPWIndex)
        elif ForgotPWRequestBody.find("faem=") >= 0:
            ForgotPWRequestEmail = urllib.parse.unquote(ForgotPWRequestBody[(ForgotPWRequestBody.index("faem=")+5):len(ForgotPWRequestBody)])
            ForgotPWRequestDBSelectEmail = "SELECT userid FROM compacc WHERE email='{0:s}'".format(ForgotPWRequestEmail)
            mycursor.execute(ForgotPWRequestDBSelectEmail)
            QueryEmailPre = mycursor.fetchone()
            if QueryEmailPre:
                QueryEmailUserID = str(QueryEmailPre[0])
                with open("/root/maxima/templates/sign_in/password_reset_email.html") as ForgotPWSMTPTemplate_F:
                    ForgotPWSMTPTemplate = ForgotPWSMTPTemplate_F.read()
                ForgotPWSMTPTemplate = ForgotPWSMTPTemplate.replace("<% UserID %>",QueryEmailUserID)
                ForgotPWTempCode = random.randint(1000000000,9999999999)
                ForgotPWSMTPTemplate = ForgotPWSMTPTemplate.replace("<% TempCode %>",str(ForgotPWTempCode))
                ForgotPWRequestDBUpdate = "UPDATE compacc SET tmpcode='{0:d}' WHERE email='{1:s}'".format(ForgotPWTempCode,ForgotPWRequestEmail)
                mycursor.execute(ForgotPWRequestDBUpdate)
                db.commit()
                ForgotPWSMTPHeaders = "\r\n".join(["from: comicernol@gmail.com","subject: Reset Your Password - FRANZAR","to:"+ForgotPWRequestEmail,"mime-version: 1.0","content-type: text/html"])
                ForgotPWSMTPContent = ForgotPWSMTPHeaders+"\r\n\r\n"+ForgotPWSMTPTemplate
                ForgotPWMail = smtplib.SMTP('smtp.gmail.com',587)
                ForgotPWMail.ehlo()
                ForgotPWMail.starttls()
                ForgotPWMail.login('comicernol@gmail.com',str(os.environ["Comicernol_Gmail_Passwd"]))
                ForgotPWMail.sendmail('comicernol@gmail.com',ForgotPWRequestEmail,ForgotPWSMTPContent)
                ForgotPWMail.close()
                ForgotPWConfIndex = ForgotPWConfIndex.replace("<% ShowError %>","none")
                ForgotPWConfIndex = ForgotPWConfIndex.replace("<% ErrorMsg %>","")
                ForgotPWConfIndex = ForgotPWConfIndex.replace("<% Email %>",ForgotPWRequestEmail)
                self.write(ForgotPWConfIndex)
            else:
                ForgotPWIndex = ForgotPWIndex.replace("<% ShowError %>","block")
                ForgotPWIndex = ForgotPWIndex.replace("<% ErrorMsg %>","Account does not exist")
                self.write(ForgotPWIndex)
        else:
            if SetCookie(self):
                pass
            else:
                ForgotPWIndex = ForgotPWIndex.replace("<% ShowError %>","block")
                ForgotPWIndex = ForgotPWIndex.replace("<% ErrorMsg %>","(F1) Something went wrong")
                self.write(ForgotPWIndex)
