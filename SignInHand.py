from udf import *

class handler(tornado.web.RequestHandler):
    def get(self):
        # Open Sign In
        SignInIndex = ServePage(self,"/sign_in/index.html",False)
        SignInIndex = SignInIndex.replace("<% ShowError %>","none")
        SignInIndex = SignInIndex.replace("<% ErrorMsg %>","")
        self.write(SignInIndex)

    def post(self):
        # Open
        SignInIndex = ServePage(self,"/sign_in/index.html",False)
        SignUpConfIndex = ServePage(self,"/sign_up/conf_sent.html",False)
        
        # Test
        SignInRequestBody = urllib.parse.unquote(self.request.body.decode('utf-8'))
        if SignInRequestBody.find("rsve=") == -1 and SignInRequestBody.find("siem=") >= 0 and SignInRequestBody.find("sipw=") >= 0:
            SignInRequestEmail = SignInRequestBody[(SignInRequestBody.index("siem=")+5):SignInRequestBody.index("&sipw=")]
            SignInRequestPassword = SignInRequestBody[(SignInRequestBody.index("sipw=")+5):len(SignInRequestBody)]
            SignInRequestDBSelectEmail = "SELECT veremail,passwd,userid FROM compacc WHERE email='{0:s}'".format(SignInRequestEmail)
            mycursor.execute(SignInRequestDBSelectEmail)
            QueryEmailPre = mycursor.fetchone()
            if QueryEmailPre:
                QueryEmailVerified = int(QueryEmailPre[0])
                QueryEmailPw = QueryEmailPre[1].encode()
                QueryEmailUserID = str(QueryEmailPre[2])
                SignInQueryPassword = Enc32a.decrypt(QueryEmailPw).decode('utf-8')
                if QueryEmailVerified == 1 and SignInQueryPassword == SignInRequestPassword:
                    SignInRequestToken = random.randint(1000000000,9999999999)
                    SignInRequestDBUpdate = "UPDATE compacc SET token='{0:d}' WHERE email='{1:s}'".format(SignInRequestToken,SignInRequestEmail)
                    mycursor.execute(SignInRequestDBUpdate)
                    db.commit()
                    self.set_cookie("Fu",QueryEmailUserID)
                    self.set_cookie("Ft",str(SignInRequestToken))
                    self.redirect("/")
                elif QueryEmailVerified != 1:
                    SendVerificationEmail(self,SignInRequestEmail)
                    SignUpConfIndex = SignUpConfIndex.replace("<% Email %>",SignInRequestEmail)
                    self.write(SignUpConfIndex)
                else:
                    SignInIndex = SignInIndex.replace("<% ShowError %>","block")
                    SignInIndex = SignInIndex.replace("<% ErrorMsg %>","Incorrect Password")
                    self.write(SignInIndex)
            else:
                SignInIndex = SignInIndex.replace("<% ShowError %>","block")
                SignInIndex = SignInIndex.replace("<% ErrorMsg %>","Account does not exist")
                self.write(SignInIndex)
        elif SignInRequestBody.find("rsve=") >= 0:
            SignUpRSVEEmail = SignInRequestBody[(SignInRequestBody.index("rsve=")+5):len(SignInRequestBody)]
            SendVerificationEmail(self,SignUpRSVEEmail)
            SignUpConfIndex = SignUpConfIndex.replace("<% Email %>",SignUpRSVEEmail)
            self.write(SignUpConfIndex)
        else:
            if SetCookie(self):
                pass
            else:
                SignInIndex = SignInIndex.replace("<% ShowError %>","block")
                SignInIndex = SignInIndex.replace("<% ErrorMsg %>","(N1) Something went wrong")
                self.write(SignInIndex)
