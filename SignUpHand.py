from udf import *

class handler(tornado.web.RequestHandler):
    def get(self):
        # Open
        SignUpIndex = ServePage(self,"/sign_up/index.html")
        SignUpIndex = SignUpIndex.replace("<% ShowError %>","none")
        SignUpIndex = SignUpIndex.replace("<% ErrorMsg %>","")
        self.write(SignUpIndex)

    def post(self):
        # Open
        SignUpIndex = ServePage(self,"/sign_up/index.html")
        SignUpConfIndex = ServePage(self,"/sign_up/conf_sent.html")
        
        # Test
        SignUpRequestBody = urllib.parse.unquote(self.request.body.decode('utf-8'))
        if SignUpRequestBody.find("rsve=") == -1 and SignUpRequestBody.find("suem=") >= 0 and SignUpRequestBody.find("supw=") >= 0 and SignUpRequestBody.find("supa=") >= 0:
            SignUpRequestEmail = SignUpRequestBody[(SignUpRequestBody.index("suem=")+5):SignUpRequestBody.index("&supw=")]
            SignUpRequestDBSelectEmail = "SELECT veremail FROM compacc WHERE email='{0:s}'".format(SignUpRequestEmail)
            mycursor.execute(SignUpRequestDBSelectEmail)
            QueryCountEmail = mycursor.fetchone()
            SignUpRequestPasswordPre = SignUpRequestBody[(SignUpRequestBody.index("supw=")+5):SignUpRequestBody.index("&supa=")]
            SignUpRequestPassword = Enc32a.encrypt(SignUpRequestPasswordPre.encode()).decode('utf-8')
            SignUpRequestPasswordAgain = SignUpRequestBody[(SignUpRequestBody.index("supa=")+5):len(SignUpRequestBody)]
            if ValidEmail(SignUpRequestEmail) and len(SignUpRequestPasswordPre) >= 8 and SignUpRequestPasswordPre == SignUpRequestPasswordAgain and mycursor.rowcount < 1:
                SignUpUserID = random.randint(1000000000,9999999999)
                SignUpRequestDBInsert = "INSERT INTO compacc (userid,email,veremail,passwd,token) VALUES ('{0:d}','{1:s}',0,'{2:s}','')".format(SignUpUserID,SignUpRequestEmail,SignUpRequestPassword)
                mycursor.execute(SignUpRequestDBInsert)
                db.commit()
                self.set_cookie("Fu",str(SignUpUserID))
                
                # Send Verification Email
                SendVerificationEmail(self,SignUpRequestEmail)
                SignUpConfIndex = SignUpConfIndex.replace("<% Email %>",SignUpRequestEmail)
                self.write(SignUpConfIndex)
            elif not ValidEmail(SignUpRequestEmail):
                SignUpIndex = SignUpIndex.replace("<% ShowError %>","block")
                SignUpIndex = SignUpIndex.replace("<% ErrorMsg %>","Please enter a valid Email")
                self.write(SignUpIndex)
            elif mycursor.rowcount >= 1:
                if int(QueryCountEmail[0]) != 1:
                    SendVerificationEmail(self,SignUpRequestEmail)
                    SignUpConfIndex = SignUpConfIndex.replace("<% Email %>",SignUpRequestEmail)
                    self.write(SignUpConfIndex)
                else:
                    SignUpIndex = SignUpIndex.replace("<% ShowError %>","block")
                    SignUpIndex = SignUpIndex.replace("<% ErrorMsg %>","This account already exists")
                    self.write(SignUpIndex)
            else:
                SignUpIndex = SignUpIndex.replace("<% ShowError %>","block")
                SignUpIndex = SignUpIndex.replace("<% ErrorMsg %>","(P1) Something went wrong")
                self.write(SignUpIndex)
        elif SignUpRequestBody.find("rsve=") >= 0:
            # Resend Verification Email
            SignUpRSVEEmail = SignUpRequestBody[(SignUpRequestBody.index("rsve=")+5):len(SignUpRequestBody)]
            SendVerificationEmail(self,SignUpRSVEEmail)
            SignUpConfIndex = SignUpConfIndex.replace("<% Email %>",SignUpRSVEEmail)
            self.write(SignUpConfIndex)
        else:
            if SetCookie(self):
                pass
            else:
                SignUpIndex = SignUpIndex.replace("<% ShowError %>","block")
                SignUpIndex = SignUpIndex.replace("<% ErrorMsg %>","(P2) Something went wrong")
                self.write(SignUpIndex)
