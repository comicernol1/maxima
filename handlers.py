from udf import *

# Don't forget to eventually close the MySQL connection

class HomeHand(tornado.web.RequestHandler):
    def get(self):
        # Generate Products List
        HomeProductList = ""
        mycursor.execute("SELECT id,ttl,price_"+UserCurrency.lower()+",discount,size,colour,colour_name from products group by left(id,7)")
        QueryProductsDict = mycursor.fetchall()
        for i in range(0,len(QueryProductsDict)):
            QueryProductsPrice = float(QueryProductsDict[i][2])
            QueryProductsDiscountIntPre = int(QueryProductsDict[i][3])
            QueryProductsDiscountInt = (float(QueryProductsDict[i][2]) * ((100 - int(QueryProductsDiscountIntPre)) / 100))
            if UserCurrencySymbol in SpecifyCurrencyList:
                if QueryProductsDiscountIntPre > 0:
                    QueryProductsPriceSet = "<h1><strike>{1:s}{2:,.2f}</strike></h1><h2>{1}{3:,.2f} ({0:s})</h2>".format(UserCurrency,UserCurrencySymbol,QueryProductsPrice,QueryProductsDiscountInt)
                else:
                    QueryProductsPriceSet = "<h1>{1:s}{2:,.2f} ({0:s})</h1>".format(UserCurrency,UserCurrencySymbol,QueryProductsPrice)
            else:
                if QueryProductsDiscountIntPre > 0:
                    QueryProductsPriceSet = "<h1><strike>{0:s}{1:,.2f}</strike></h1><h2>{0:s}{2:,.2f}</h2>".format(UserCurrencySymbol,QueryProductsPrice,QueryProductsDiscountInt)
                else:
                    QueryProductsPriceSet = "<h1>{0:s}{1:,.2f}</h1>".format(UserCurrencySymbol,QueryProductsPrice)
            QueryProductsID = str(QueryProductsDict[i][0])
            QueryProductsDefaultColour = str(QueryProductsDict[i][5])
            QueryProductsDefaultColourName = str(QueryProductsDict[i][6]).title()
            QueryProductColoursDict = FindProductColours(QueryProductsID)
            ReturnProductTitle = str(QueryProductsDict[i][1])
            ReturnProductColoursDict = ""
            for Ci in range(0,len(QueryProductColoursDict["ID"])):
                if QueryProductColoursDict["Hex"][Ci] != QueryProductsDefaultColour:
                    ReturnProductColoursDict += "<abbr style=\"background:#"+QueryProductColoursDict["Hex"][Ci]+";\" title=\""+QueryProductColoursDict["Name"][Ci]+"\" s=\"n\"></abbr>"
            HomeProductList += "<a style=\"background-image:url(/static/product/"+QueryProductsID+"/0.jpg);\" href=\"/product/"+QueryProductsID+"/\" title=\""+ReturnProductTitle+"\"><div class=\"BPX\"><span><abbr style=\"background:#"+QueryProductsDefaultColour+";\" title=\""+QueryProductsDefaultColourName+"\" s=\"y\"></abbr>"+ReturnProductColoursDict+"</span><h6>"+ReturnProductTitle+"</h6>"+QueryProductsPriceSet+"</div></a>\n"
        
        # Open
        HomeIndex = ServePage(self,"/index.html")
        HomeIndex = HomeIndex.replace("<% Products %>", HomeProductList)
        self.write(HomeIndex)
        
    def post(self):
        SetCookie(self)

class ContactHand(tornado.web.RequestHandler):
    def get(self):
        # Open
        ContactIndex = ServePage(self,"/contact/index.html")
        ContactIndex = ContactIndex.replace("<% ShowError %>","none")
        ContactIndex = ContactIndex.replace("<% ErrorMsg %>","")
        self.write(ContactIndex)
        
    def post(self):
        # Open
        ContactIndex = ServePage(self,"/contact/index.html")
        ContactSentIndex = ServePage(self,"/contact/sent.html")
        
        # Test
        ContactRequestBody = urllib.parse.unquote(self.request.body.decode('utf-8').replace("+"," "))
        if ContactRequestBody.find("CFn=") >= 0 and ContactRequestBody.find("CFe=") >= 0 and ContactRequestBody.find("CFo=") >= 0 and ContactRequestBody.find("CFt=") >= 0:
            ContactRequestCFn = ContactRequestBody[(ContactRequestBody.index("CFn=")+4):ContactRequestBody.index("&CFe=")]
            ContactRequestCFe = ContactRequestBody[(ContactRequestBody.index("CFe=")+4):ContactRequestBody.index("&CFo=")]
            ContactRequestCFo = ContactRequestBody[(ContactRequestBody.index("CFo=")+4):ContactRequestBody.index("&CFt=")]
            ContactRequestCFt = ContactRequestBody[(ContactRequestBody.index("CFt=")+4):len(ContactRequestBody)]
            if ContactRequestCFn!="" and ContactRequestCFe!="" and ContactRequestCFt!="":
                with open("/root/maxima/templates/contact/ticket.html") as ContactSMPTTemplate_T_F:
                    ContactSMTPTemplate_T = ContactSMPTTemplate_T_F.read()
                with open("/root/maxima/templates/contact/confirm.html") as ContactSMPTTemplate_U_F:
                    ContactSMTPTemplate_U = ContactSMPTTemplate_U_F.read()
                
                # Send Ticket Email
                ContactSMTPTemplate_T = ContactSMTPTemplate_T.replace("<% FullName %>",str(ContactRequestCFn))
                ContactSMTPTemplate_T = ContactSMTPTemplate_T.replace("<% Email %>",str(ContactRequestCFe))
                ContactSMTPTemplate_T = ContactSMTPTemplate_T.replace("<% OrderID %>",str(ContactRequestCFo))
                ContactSMTPTemplate_T = ContactSMTPTemplate_T.replace("<% Message %>",str(ContactRequestCFt))
                ContactSMTPTicketID = str(random.randint(10000,99999))
                ContactSMTPHeaders_T = "\r\n".join(["from: comicernol@gmail.com","subject: Ticket #"+ContactSMTPTicketID,"to:reedsienkiewicz@gmail.com","mime-version: 1.0","content-type: text/html"])
                ContactSMTPContent_T = ContactSMTPHeaders_T+"\r\n\r\n"+ContactSMTPTemplate_T
                ContactMail_T = smtplib.SMTP('smtp.gmail.com',587)
                ContactMail_T.ehlo()
                ContactMail_T.starttls()
                ContactMail_T.login('comicernol@gmail.com',str(os.environ["Comicernol_Gmail_Passwd"]))
                ContactMail_T.sendmail('comicernol@gmail.com','reedsienkiewicz@gmail.com',ContactSMTPContent_T)
                ContactMail_T.close()
                
                # Send User Confirmation Email
                ContactSMTPTemplate_U = ContactSMTPTemplate_U.replace("<% FullName %>",str(ContactRequestCFn))
                ContactSMTPTemplate_U = ContactSMTPTemplate_U.replace("<% Email %>",str(ContactRequestCFe))
                ContactSMTPTemplate_U = ContactSMTPTemplate_U.replace("<% OrderID %>",str(ContactRequestCFo))
                ContactSMTPTemplate_U = ContactSMTPTemplate_U.replace("<% Message %>",str(ContactRequestCFt))
                ContactSMTPHeaders_U = "\r\n".join(["from: comicernol@gmail.com","subject: Confirmation of Ticket #"+ContactSMTPTicketID,"to:"+str(ContactRequestCFe),"mime-version: 1.0","content-type: text/html"])
                ContactSMTPContent_U = ContactSMTPHeaders_U+"\r\n\r\n"+ContactSMTPTemplate_U
                ContactMail_U = smtplib.SMTP('smtp.gmail.com',587)
                ContactMail_U.ehlo()
                ContactMail_U.starttls()
                ContactMail_U.login('comicernol@gmail.com',str(os.environ["Comicernol_Gmail_Passwd"]))
                ContactMail_U.sendmail('comicernol@gmail.com',str(ContactRequestCFe),ContactSMTPContent_U)
                ContactMail_U.close()
                self.write(ContactSentIndex)
            else:
                if ContactRequestCFn=="":
                    ContactIndex = ContactIndex.replace("<% ErrorMsg %>","Please enter your name")
                elif ContactRequestCFe=="":
                    ContactIndex = ContactIndex.replace("<% ErrorMsg %>","Please enter a valid Email")
                elif ContactRequestCFt=="":
                    ContactIndex = ContactIndex.replace("<% ErrorMsg %>","Please enter your message")
                else:
                    ContactIndex = ContactIndex.replace("<% ErrorMsg %>","(C1) Something went wrong")
                ContactIndex = ContactIndex.replace("<% ShowError %>","block")
                self.write(ContactIndex)
        else:
            if SetCookie(self):
                pass
            else:
                ContactIndex = ContactIndex.replace("<% ErrorMsg %>","(C2) Something went wrong")
                ContactIndex = ContactIndex.replace("<% ShowError %>","block")
                self.write(ContactIndex)

class SignInHand(tornado.web.RequestHandler):
    def get(self):
        # Open Sign In
        SignInIndex = ServePage(self,"/sign_in/index.html")
        SignInIndex = SignInIndex.replace("<% ShowError %>","none")
        SignInIndex = SignInIndex.replace("<% ErrorMsg %>","")
        self.write(SignInIndex)

    def post(self):
        # Open
        SignInIndex = ServePage(self,"/sign_in/index.html")
        
        # Test
        SignInRequestBody = urllib.parse.unquote(self.request.body.decode('utf-8'))
        if SignInRequestBody.find("siem=") >= 0 and SignInRequestBody.find("sipw=") >= 0:
            SignInRequestEmail = SignInRequestBody[(SignInRequestBody.index("siem=")+5):SignInRequestBody.index("&sipw=")]
            SignInRequestPassword = SignInRequestBody[(SignInRequestBody.index("sipw=")+5):len(SignInRequestBody)]
            SignInRequestDBSelectEmail = "SELECT passwd,userid FROM compacc WHERE email='{0:s}'".format(SignInRequestEmail)
            mycursor.execute(SignInRequestDBSelectEmail)
            QueryEmailPre = mycursor.fetchone()
            if QueryEmailPre:
                QueryEmailPw = QueryEmailPre[0].encode()
                QueryEmailUserID = str(QueryEmailPre[1])
                SignInQueryPassword = Enc32a.decrypt(QueryEmailPw).decode('utf-8')
                if SignInQueryPassword == SignInRequestPassword:
                    SignInRequestToken = random.randint(1000000000,9999999999)
                    SignInRequestDBUpdate = "UPDATE compacc SET token='{0:d}' WHERE email='{1:s}'".format(SignInRequestToken,SignInRequestEmail)
                    mycursor.execute(SignInRequestDBUpdate)
                    db.commit()
                    self.set_secure_cookie("Fu",QueryEmailUserID)
                    self.set_secure_cookie("Ft",str(SignInRequestToken))
                    self.redirect("/")
                else:
                    SignInIndex = SignInIndex.replace("<% ShowError %>","block")
                    SignInIndex = SignInIndex.replace("<% ErrorMsg %>","Incorrect Password")
                    self.write(SignInIndex)
            else:
                SignInIndex = SignInIndex.replace("<% ShowError %>","block")
                SignInIndex = SignInIndex.replace("<% ErrorMsg %>","Account does not exist")
                self.write(SignInIndex)
        else:
            if SetCookie(self):
                pass
            else:
                SignInIndex = SignInIndex.replace("<% ShowError %>","block")
                SignInIndex = SignInIndex.replace("<% ErrorMsg %>","(N1) Something went wrong")
                self.write(SignInIndex)

class ForgotPWHand(tornado.web.RequestHandler):
    def get(self):
        # Open
        ForgotPWIndex = ServePage(self,"/sign_in/forgot_pw.html")
        self.write(ForgotPWIndex)
    
    def post(self):
        # Open
        ForgotPWIndex = ServePage(self,"/sign_in/forgot_pw.html")
        ForgotPWConfIndex = ServePage(self,"/sign_in/forgot_pw_conf.html")
        
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

class ResetPWHand(tornado.web.RequestHandler):
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
                    self.set_secure_cookie("Fu",str(ResetPWRequestE))
                    self.set_secure_cookie("Ft","")
                    self.write(ResetPWIndex)
                else:
                    ResetPWMsgIndex = ResetPWMsgIndex.replace("<% Msg %>","This link has expired.")
                    self.write(ResetPWMsgIndex)
            else:
                ResetPWMsgIndex = ResetPWMsgIndex.replace("<% Msg %>","We can't find an account matching this link.")
                self.write(ResetPWMsgIndex)
        except tornado.web.MissingArgumentError:
            try:
                ResetPWCookieFu = int(self.get_secure_cookie("Fu"))
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
            
    def post(self):
        # Open
        ResetPWIndex = ServePage(self,"/sign_in/reset_pw.html")
        ResetPWMsgIndex = ServePage(self,"/sign_in/reset_pw_msg.html")
        
        # Test
        if self.get_secure_cookie("Fu") != "":
            ResetPWRequestBody = urllib.parse.unquote(self.request.body.decode('utf-8'))
            ResetPWCookieFu = int(self.get_secure_cookie("Fu"))
            if ResetPWRequestBody.find("rppw=") >= 0 and ResetPWRequestBody.find("rppa=") >= 0:
                ResetPWRequestNewPWPre = ResetPWRequestBody[(ResetPWRequestBody.index("rppw=")+5):ResetPWRequestBody.index("&rppa=")]
                ResetPWRequestNewPWAgain = ResetPWRequestBody[(ResetPWRequestBody.index("rppa=")+5):len(ResetPWRequestBody)]
                ResetPWRequestDBSelectCode = "SELECT email FROM compacc WHERE userid='{0:d}'".format(ResetPWCookieFu)
                mycursor.execute(ResetPWRequestDBSelectCode)
                QueryIDPre = mycursor.fetchone()
                if QueryIDPre:
                    if ResetPWRequestNewPWPre == ResetPWRequestNewPWAgain:
                        if len(ResetPWRequestNewPWPre) >= 8:
                            ResetPWRequestNewPW = Enc32a.encrypt(ResetPWRequestNewPWPre.encode()).decode('utf-8')
                            ResetPWRequestDBUpdate = "UPDATE compacc SET passwd='{0:s}' WHERE userid='{1:d}'".format(ResetPWRequestNewPW,ResetPWCookieFu)
                            mycursor.execute(ResetPWRequestDBUpdate)
                            db.commit()
                            ResetPWMsgIndex = ResetPWMsgIndex.replace("<% Msg %>","Your password has been changed")
                            self.write(ResetPWMsgIndex)
                        else:
                            ResetPWIndex = ResetPWIndex.replace("<% Email %>",str(QueryIDPre[0]))
                            ResetPWIndex = ResetPWIndex.replace("<% ShowError %>","block")
                            ResetPWIndex = ResetPWIndex.replace("<% ErrorMsg %>","Password must be 8 characters or more")
                            self.write(ResetPWIndex)
                    else:
                        ResetPWIndex = ResetPWIndex.replace("<% Email %>",str(QueryIDPre[0]))
                        ResetPWIndex = ResetPWIndex.replace("<% ShowError %>","block")
                        ResetPWIndex = ResetPWIndex.replace("<% ErrorMsg %>","Passwords must match")
                        self.write(ResetPWIndex)
                else:
                    ResetPWMsgIndex = ResetPWMsgIndex.replace("<% Msg %>","We can't find an account matching this link.")
                    self.write(ResetPWMsgIndex)
            else:
                ResetPWMsgIndex = ResetPWMsgIndex.replace("<% Msg %>","(R1) Something went wrong")
                self.write(ResetPWMsgIndex)
        else:
            if SetCookie(self):
                pass
            else:
                ResetPWMsgIndex = ResetPWMsgIndex.replace("<% Msg %>","(R2) Something went wrong")
                self.write(ResetPWMsgIndex)

class SignUpHand(tornado.web.RequestHandler):
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
        if SignUpRequestBody.find("suem=") >= 0 and SignUpRequestBody.find("supw=") >= 0 and SignUpRequestBody.find("supa=") >= 0:
            SignUpRequestEmail = SignUpRequestBody[(SignUpRequestBody.index("suem=")+5):SignUpRequestBody.index("&supw=")]
            SignUpRequestDBSelectEmail = "SELECT COUNT(*) FROM compacc WHERE email='{0:s}' and veremail=1".format(SignUpRequestEmail)
            mycursor.execute(SignUpRequestDBSelectEmail)
            QueryCountEmail = mycursor.fetchone()
            SignUpRequestPasswordPre = SignUpRequestBody[(SignUpRequestBody.index("supw=")+5):SignUpRequestBody.index("&supa=")]
            SignUpRequestPassword = Enc32a.encrypt(SignUpRequestPasswordPre.encode()).decode('utf-8')
            SignUpRequestPasswordAgain = SignUpRequestBody[(SignUpRequestBody.index("supa=")+5):len(SignUpRequestBody)]
            if SignUpRequestBody.find("rsve=y") and len(SignUpRequestPasswordPre) >= 8 and SignUpRequestPasswordPre == SignUpRequestPasswordAgain and int(QueryCountEmail[0]) < 1:
                SignUpUserID = random.randint(1000000000,9999999999)
                SignUpVerifyCode = random.randint(1000000000,9999999999)
                SignUpRequestDBInsert = "INSERT INTO compacc (userid,email,veremail,tmpcode,passwd,token) VALUES ('{0:d}','{1:s}',0,'{2:d}','{3:s}','')".format(SignUpUserID,SignUpRequestEmail,SignUpVerifyCode,SignUpRequestPassword)
                mycursor.execute(SignUpRequestDBInsert)
                db.commit()
                
                # Send Verification Email
                with open("/root/maxima/templates/sign_up/conf_email.html") as SignUpSMPTTemplate_F:
                    SignUpSMTPTemplate = SignUpSMPTTemplate_F.read()
                SignUpSMTPTemplate = SignUpSMTPTemplate.replace("<% UserCode %>",str(SignUpVerifyCode))
                SignUpSMTPHeaders = "\r\n".join(["from: comicernol@gmail.com","subject: Verify Your Email - FRANZAR","to:"+SignUpRequestEmail,"mime-version: 1.0","content-type: text/html"])
                SignUpSMTPContent = SignUpSMTPHeaders+"\r\n\r\n"+SignUpSMTPTemplate
                SignUpMail = smtplib.SMTP('smtp.gmail.com',587)
                SignUpMail.ehlo()
                SignUpMail.starttls()
                SignUpMail.login('comicernol@gmail.com',str(os.environ["Comicernol_Gmail_Passwd"]))
                SignUpMail.sendmail('comicernol@gmail.com',SignUpRequestEmail,SignUpSMTPContent)
                SignUpMail.close()
                SignUpConfIndex = SignUpConfIndex.replace("<% Email %>",SignUpRequestEmail)
                self.write(SignUpConfIndex)
            elif SignUpRequestBody.find("rsve=y") == -1 and int(QueryCountEmail[0]) >= 1:
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
            with open("/root/maxima/templates/sign_up/conf_email.html") as SignUpSMPTTemplate_F:
                    SignUpSMTPTemplate = SignUpSMPTTemplate_F.read()
            SignUpSMTPHeaders = "\r\n".join(["from: comicernol@gmail.com","subject: Verify Your Email - FRANZAR","to:"+SignUpRSVEEmail,"mime-version: 1.0","content-type: text/html"])
            SignUpSMTPContent = SignUpSMTPHeaders+"\r\n\r\n"+SignUpSMTPTemplate
            SignUpMail = smtplib.SMTP('smtp.gmail.com',587)
            SignUpMail.ehlo()
            SignUpMail.starttls()
            SignUpMail.login('comicernol@gmail.com',str(os.environ["Comicernol_Gmail_Passwd"]))
            SignUpMail.sendmail('comicernol@gmail.com',SignUpRSVEEmail,SignUpSMTPContent)
            SignUpMail.close()
            SignUpConfIndex = SignUpConfIndex.replace("<% Email %>",SignUpRSVEEmail)
            self.write(SignUpConfIndex)
        else:
            if SetCookie(self):
                pass
            else:
                SignUpIndex = SignUpIndex.replace("<% ShowError %>","block")
                SignUpIndex = SignUpIndex.replace("<% ErrorMsg %>","(P2) Something went wrong")
                self.write(SignUpIndex)

class VerifyHand(tornado.web.RequestHandler):
    def get(self):
        # Open
        VerifyIndex = ServePage(self,"/sign_up/verified.html")
        VerifyIndex = VerifyIndex.replace("<% Email %>",self.get_query_argument("e"))
        self.write(VerifyIndex)

class AccountHand(tornado.web.RequestHandler):
    def get(self):
        if CheckLogin(self):
            UserInfoFu = self.get_secure_cookie("Fu")
            # Pull Account Orders
            AccountOrdersQuery = "SELECT oid,pid,fprice,stat,arrival,dest from orders where uid='{0:d}' order by pdate desc".format(int(UserInfoFu))
            mycursor.execute(AccountOrdersQuery)
            AccountOrdersFetch = mycursor.fetchall()
            
            # Set OrderList
            AccountOrdersList = ""
            for OFi in range(0,len(AccountOrdersFetch)):
                AccountOrdersListStatus = ShippingCodesList[AccountOrdersFetch[OFi][3]]
                AccountOrdersList += "<tr>"
                AccountOrdersList += "<td><a href=\"/order/"+str(AccountOrdersFetch[OFi][0])+"/\">"+str(AccountOrdersFetch[OFi][0])+"</a></td>"
                AccountOrdersList += "<td><a href=\"/product/"+str(AccountOrdersFetch[OFi][1])+"/\">"+str(FindProduct(AccountOrdersFetch[OFi][1])["Name"])+"</a></td>"
                AccountOrdersList += "<td>$"+str(AccountOrdersFetch[OFi][2])+"</td>"
                AccountOrdersList += "<td>"+str(AccountOrdersListStatus)+"</td>"
                AccountOrdersList += "<td>"+str(AccountOrdersFetch[OFi][4])+"</td>"
                AccountOrdersList += "<td>"+str(FindAddress(AccountOrdersFetch[OFi][5])["StAddA"])+"</td>"
                AccountOrdersList += "</tr>\n"
            
            # Pull Account Addresses
            AccountAddressesQuery = "SELECT adid,stadda,staddb,city,zip,prov,ntn from addresses where uid='{0:d}' order by name asc".format(int(UserInfoFu))
            mycursor.execute(AccountAddressesQuery)
            AccountAddressesFetch = mycursor.fetchall()
            
            # Set AddressOptions
            if AccountAddressesFetch:
                AccountAddressOptions = ""
                for AFi in range(0,len(AccountAddressesFetch)):
                    AccountAddressOptions += "<option value=\""+str(AccountAddressesFetch[AFi][0])+"\">"+str(AccountAddressesFetch[AFi][1])+", "+str(AccountAddressesFetch[AFi][3])+" "+str(AccountAddressesFetch[AFi][4])+"</option>\n"
            else:
                AccountAddressOptions = "<option value=\"na\"> - Please Connect an Address - </option>"
            
            # Open
            AccountIndex = ServePage(self,"/account/index.html")
            AccountIndex = AccountIndex.replace("<% AddressOptions %>",AccountAddressOptions)
            AccountIndex = AccountIndex.replace("<% OrderList %>",AccountOrdersList)
            self.write(AccountIndex)
        else:
            self.redirect("/sign_in/")
    
    def post(self):
        SetCookie(self)

class ProductHand(tornado.web.RequestHandler):
    def get(self):
        # Open
        ProductIndex = ServePage(self,"/product/index.html")
        NotFoundIndex = ServePage(self,"/status/404.html")
        
        # Formatting
        ProductIndexURI = self.request.uri
        ProductRequested_ID = ProductIndexURI[(ProductIndexURI.index("/product/")+9):(len(ProductIndexURI)-1)]
        ProductRequested_Name = FindProduct(ProductRequested_ID)["Name"]
        if ProductRequested_Name != "":
            ProductRequested_Desc = FindProduct(ProductRequested_ID)["Description"]
            if FindProduct(ProductRequested_ID)["Wring"]=="n":
                ProductRequested_CareWring = "<li>Do Not Wring</li>"
            else:
                ProductRequested_CareWring = ""
            ProductRequested_Care = "<li>"+WashCareCodesList[FindProduct(ProductRequested_ID)["Wash"]]+"</li><li>"+BleachCareCodesList[FindProduct(ProductRequested_ID)["Bleach"]]+"</li><li>"+DryCareCodesList[FindProduct(ProductRequested_ID)["Dry"]]+"</li>"+ProductRequested_CareWring+"<li>"+DryCleanCareCodesList[FindProduct(ProductRequested_ID)["DryClean"]]+"</li>"
            ProductRequested_ContentsDict = FindProduct(ProductRequested_ID)["ContentsDict"]
            if len(ProductRequested_ContentsDict) > 1:
                ProductRequested_Contents = ""
                for Tk,Ti in ProductRequested_ContentsDict.items():
                    ProductRequested_Contents += "<li>"+Tk+": "+Ti+"</li>"
                ProductRequested_Contents = "<ul>"+ProductRequested_Contents+"</ul>"
            elif len(ProductRequested_ContentsDict) == 1:
                ProductRequested_Contents = ProductRequested_ContentsDict["Main"]
            else:
                ProductRequested_Contents = ""
            ProductRequested_Price = FindProduct(ProductRequested_ID)["Price"]
            ProductRequested_DiscountPre = FindProduct(ProductRequested_ID)["Discount"]
            ProductRequested_Discount = (ProductRequested_Price * ((100 - ProductRequested_DiscountPre) / 100))
            if UserCurrencySymbol in SpecifyCurrencyList:
                if ProductRequested_DiscountPre > 0:
                    ProductRequested_PriceSet = "<h1 id=\"BIp\"><strike>{1:s}{2:,.2f}</strike></h1><h2 id=\"BId\">{1}{3:,.2f} ({0:s})</h2>".format(UserCurrency,UserCurrencySymbol,ProductRequested_Price,ProductRequested_Discount)
                else:
                    ProductRequested_PriceSet = "<h1 id=\"BIp\">{1:s}{2:,.2f} ({0:s})</h1>".format(UserCurrency,UserCurrencySymbol,ProductRequested_Price)
            else:
                if ProductRequested_DiscountPre > 0:
                    ProductRequested_PriceSet = "<h1 id=\"BIp\"><strike>{0:s}{1:,.2f}</strike></h1><h2 id=\"BId\">{0:s}{2:,.2f}</h2>".format(UserCurrencySymbol,ProductRequested_Price,ProductRequested_Discount)
                else:
                    ProductRequested_PriceSet = "<h1 id=\"BIp\">{0:s}{1:,.2f}</h1>".format(UserCurrencySymbol,ProductRequested_Price)
            ProductColoursDict = FindProductColours(ProductRequested_ID)
            ProductRequested_ColourOptions = ""
            for i in range(0,len(ProductColoursDict["ID"])):
                if ProductColoursDict["Hex"][i] == str(FindProduct(ProductRequested_ID)["Colour"]):
                    ProductRequested_ColourOptions += "<a style=\"background:#"+str(FindProduct(ProductRequested_ID)["Colour"])+";\" title=\""+str(FindProduct(ProductRequested_ID)["ColourName"])+"\" s=\"y\"></a>"
                else:
                    ProductRequested_ColourOptions += "<a href=\"/product/"+ProductColoursDict["ID"][i]+"/\" style=\"background:#"+ProductColoursDict["Hex"][i]+";\" title=\""+ProductColoursDict["Name"][i]+"\" s=\"n\"></a>"
            if FindProduct(ProductRequested_ID)["HasImg"]:
                ProductRequested_ImageLink = ProductRequested_ImageLinkTest
                ProductRequested_ImageCnt = len(fnmatch.filter(os.listdir("/root/maxima/static/product/"+ProductRequested_ID+"/"), "*.jpg"))
                ProductRequested_BPs = ""
                for BPSi in range(0,ProductRequested_ImageCnt):
                    ProductRequested_BPs += "<li><img src=\"/static/product/"+ProductRequested_ID+"/"+str(BPSi)+".jpg\" alt=\""+ProductRequested_Name+" ("+str(BPSi + 1)+")\"></li>\n"
            else:
                ProductRequested_ImageLink = "/static/product/missing.jpg"
                ProductRequested_BPs = "<li><img src=\"/static/product/missing.jpg\" alt=\""+ProductRequested_Name+" (1)\"></li>\n"
            ProductRequested_Rating = 0
            ProductRequested_ReviewCount = 0
        
            ProductIndex = ProductIndex.replace("<% ProductID %>",ProductRequested_ID)
            ProductIndex = ProductIndex.replace("<% ProductName %>",ProductRequested_Name)
            ProductIndex = ProductIndex.replace("<% ProductDescription %>",ProductRequested_Desc)
            ProductIndex = ProductIndex.replace("<% ProductContents %>",ProductRequested_Contents)
            ProductIndex = ProductIndex.replace("<% ProductCare %>",ProductRequested_Care)
            ProductIndex = ProductIndex.replace("<% ProductPrice %>",ProductRequested_PriceSet)
            ProductIndex = ProductIndex.replace("<% ProductColourOptions %>",ProductRequested_ColourOptions)
            ProductIndex = ProductIndex.replace("<% ProductImgLink %>",ProductRequested_ImageLink)
            ProductIndex = ProductIndex.replace("<% FullImageList %>",ProductRequested_BPs)
            ProductIndex = ProductIndex.replace("<% Rating %>",str(ProductRequested_Rating))
            ProductIndex = ProductIndex.replace("<% ReviewCount %>",str(ProductRequested_ReviewCount))
            self.write(ProductIndex)
        else:
            self.write(NotFoundIndex)
    
    def post(self):
        SetCookie(self)

class CartHand(tornado.web.RequestHandler):
    def get(self):
        CartIndex = ServePage(self,"/cart/index.html")
        UserCartList = GetCart(self)
        UserCartItems = ""
        for i in range(0,len(UserCartList)):
            UserCartItem_ID = str(UserCartList[i][0])
            if FindProduct(UserCartItem_ID)["HasImg"]:
                UserCartItem_ImgLink = "/static/product/"+UserCartItem_ID+"/0.jpg"
            else:
                UserCartItem_ImgLink = "/static/product/missing.jpg"
            UserCartItem_Price = FindProduct(UserCartItem_ID)["Price"]
            if UserCurrencySymbol in SpecifyCurrencyList:
                UserCartItem_PriceSet = "{0:s}{1:,.2f} ({2:s})".format(UserCurrencySymbol,UserCartItem_Price,UserCurrency)
            else:
                UserCartItem_PriceSet = "{0:s}{1:,.2f}".format(UserCurrencySymbol,UserCartItem_Price)
            UserCartItems += "<div class=\"CIt\" style=\"top:"+str(i*210)+"px;\"><input type=\"number\" value=\""+str(UserCartList[i][1])+"\"><div class=\"CIi\" style=\"background-image:url("+UserCartItem_ImgLink+");\"></div><h3>"+FindProduct(UserCartItem_ID)["Name"]+"</h3><h1>"+UserCartItem_PriceSet+"</h1></div>\n"
        CartIndex = CartIndex.replace("<% Cart %>",UserCartItems)
        UserCartFootTop = ((i*210)+120)
        CartIndex = CartIndex.replace("<% FootTop %>",UserCartFootTop)
        self.write(CartIndex)

class TermsConditionsHand(tornado.web.RequestHandler):
    def get(self):
        # Open
        TermsConditionsIndex = ServePage(self,"/legal/terms.html")
        self.write(TermsConditionsIndex)
    
    def post(self):
        SetCookie(self)

class CounterfeitHand(tornado.web.RequestHandler):
    def get(self):
        # Open
        CounterfeitIndex = ServePage(self,"/legal/counterfeit.html")
        self.write(CounterfeitIndex)
    
    def post(self):
        SetCookie(self)

class NotFoundHand(tornado.web.RequestHandler):
    def get(self):
        # Open
        NotFoundIndex = ServePage(self,"/status/404.html")
        self.write(NotFoundIndex)
    
    def post(self):
        SetCookie(self)
