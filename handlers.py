import os,random,base64,fnmatch,tornado.web,urllib.parse,mysql.connector,smtplib
from cryptography.fernet import Fernet
Enc32a = Fernet(base64.b64encode(os.environ["Enc32a"].encode()))
Enc32b = Fernet(base64.b64encode(os.environ["Enc32b"].encode()))
db = mysql.connector.connect(
    host = "127.0.0.1",
    port = 3306,
    user = "maxima",
    password = str(os.environ["MYSQL_MAXIMA_PASSWD"]),
    database = "franzar"
)
mycursor = db.cursor()
        
def CheckLogin(self):
    if self.get_secure_cookie("Fu") and self.get_secure_cookie("Ft"):
        UserInfoFu = self.get_secure_cookie("Fu")
        UserInfoFt = self.get_secure_cookie("Ft")
        UserInfoLoginQuery = "SELECT * from compacc where userid='{0:d}' and token='{1:d}'".format(int(UserInfoFu),int(UserInfoFt))
        mycursor.execute(UserInfoLoginQuery)
        UserInfoLoginFetch = mycursor.fetchone()
        if UserInfoLoginFetch:
            return True
        else:
            return False
    else:
        return False

def ServePage(self,pageloc):
    # Define Basics
    HeaderLISignIn = "<a id=\"HMs\" href=\"/sign_in/\">Sign In</a>"
    HeaderLIAccountButton = "<a id=\"HMs\" href=\"/account/\">My Account<span></span></a><a id=\"HMc\" href=\"/cart/\" title=\"My Cart\"><span>0</span></a>"
    CookieNotifDiv = "<div id=\"Fackc\">By continuing to use this site, you agree to our <a href=\"/legal/cookie_policy/\">Cookie Policy</a>. <b onclick=\"ackc()\">Accept</b></div>"
    
    # Define Header Pre
    if pageloc=="/index.html":
        HeaderLIPre = "<div id=\"M_H_close\" onclick=\"M_menu_hide()\"></div><li><a href=\"/\"><b>Home</b></a></li><li><a href=\"/contact/\">Contact</a></li>"
    elif pageloc=="/contact/index.html" or pageloc=="/contact/sent.html":
        HeaderLIPre = "<div id=\"M_H_close\" onclick=\"M_menu_hide()\"></div><li><a href=\"/\">Home</a></li><li><a href=\"/contact/\"><b>Contact</b></a></li>"
    else:
        HeaderLIPre = "<div id=\"M_H_close\" onclick=\"M_menu_hide()\"></div><li><a href=\"/\">Home</a></li><li><a href=\"/contact/\">Contact</a></li>"
    
    # Open Templates
    with open("/root/maxima/templates/head.html") as HeadHTML_F:
        HeadHTML = HeadHTML_F.read()
    with open("/root/maxima/templates/footer.html") as FooterHTML_F:
        FooterHTML = FooterHTML_F.read()
    
    # Open Requested Page
    with open("/root/maxima/req"+str(pageloc)) as PageIndex_F:
        PageIndex = PageIndex_F.read()
    if CheckLogin(self):
        PageIndex = PageIndex.replace("<% HeaderLI %>",HeaderLIPre+HeaderLIAccountButton)
    else:
        PageIndex = PageIndex.replace("<% HeaderLI %>",HeaderLIPre+HeaderLISignIn)
    PageIndex = PageIndex.replace("<% Head %>",HeadHTML)
    if self.get_secure_cookie("Fa") == "true":
        FooterHTML = FooterHTML.replace("<% CookieNotif %>","")
    else:
        FooterHTML = FooterHTML.replace("<% CookieNotif %>",CookieNotifDiv)
    PageIndex = PageIndex.replace("<% Footer %>",FooterHTML)
    return PageIndex
    
def FindAddress(adid):
    try:
        FindAddressQuery = "SELECT stadda,staddb,city,zip,prov,ntn from addresses where adid='{0:d}'".format(int(adid))
        mycursor.execute(FindAddressQuery)
        FindAddressFetch = mycursor.fetchone()
        if FindAddressFetch:
            FindAddressStAddA = FindAddressFetch[0]
            FindAddressStAddB = FindAddressFetch[1]
            FindAddressCity = FindAddressFetch[2]
            FindAddressZip = FindAddressFetch[3]
            FindAddressProv = FindAddressFetch[4]
            FindAddressNtn = FindAddressFetch[5]
            FindAddressDict = {"StAddA":FindAddressStAddA,"StAddB":FindAddressStAddB,"City":FindAddressCity,"Zip":FindAddressZip,"Prov":FindAddressProv,"Ntn":FindAddressNtn}
            return FindAddressDict
        else:
            return {"StAddA":"","StAddB":"","City":"","Zip":"","Prov":"","Ntn":""}
    except:
        return {"StAddA":"","StAddB":"","City":"","Zip":"","Prov":"","Ntn":""}

SpecifyCurrencyList = ["$"]

UserCurrency = "USD"
if UserCurrency=="USD" or UserCurrency=="CAD":
    UserCurrencySymbol = "$"
elif UserCurrency=="EUR":
    UserCurrencySymbol = "€"
else:
    UserCurrencySymbol = "(?)"

def FindProduct(pid):
    try:
        FindProductQuery = "SELECT ttl,price_"+UserCurrency.lower()+",discount,size,colour,colour_name from products where id='{0:d}'".format(int(pid))
        mycursor.execute(FindProductQuery)
        FindProductFetch = mycursor.fetchone()
        if FindProductFetch:
            FindProductName = FindProductFetch[0]
            FindProductPrice = FindProductFetch[1]
            FindProductDiscount = FindProductFetch[2]
            FindProductSize = FindProductFetch[3]
            FindProductColour = FindProductFetch[4]
            FindProductColourName = FindProductFetch[5].title()
            FindProductDict = {"Name":FindProductName,"Price":FindProductPrice,"Discount":FindProductDiscount,"Size":FindProductSize,"Colour":FindProductColour,"ColourName":FindProductColourName}
            return FindProductDict
        else:
            return {"Name":"","Price":"","Discount":"","Size":"","Colour":"","ColourName":""}
    except:
        return {"Name":"","Price":"","Discount":"","Size":"","Colour":"","ColourName":""}

ShippingCodesList = [("p","In Production"),("i","In Progress"),("d","Delivered")]

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
            QueryProductsUniversalID = QueryProductsID[0:7]
            QueryProductsDefaultColour = str(QueryProductsDict[i][5])
            RequestDBProductColours = "SELECT colour,colour_name from products where left(id,7)='{0:s}' and colour!='{1:s}'".format(QueryProductsUniversalID,QueryProductsDefaultColour)
            mycursor.execute(RequestDBProductColours)
            QueryProductColoursFetch = mycursor.fetchall()
            QueryProductColoursDict = ""
            for Ci in range(0,len(QueryProductColoursFetch)):
                QueryProductColoursDict += "<abbr style=\"background:#"+str(QueryProductColoursFetch[Ci][0])+";\" title=\""+str(QueryProductColoursFetch[Ci][1]).title()+"\" s=\"n\"></abbr>"
            HomeProductList += "<a style=\"background-image:url(/static/product/"+QueryProductsID+"/0.jpg);\" href=\"/product/"+QueryProductsID+"/\"><div class=\"BPX\"><span><abbr style=\"background:#"+QueryProductsDefaultColour+";\" title=\""+str(QueryProductsDict[i][6]).title()+"\" s=\"y\"></abbr>"+QueryProductColoursDict+"</span><h6>"+str(QueryProductsDict[i][1])+"</h6>"+QueryProductsPriceSet+"</div></a>\n"
        
        # Open
        HomeIndex = ServePage(self,"/index.html")
        HomeIndex = HomeIndex.replace("<% Products %>", HomeProductList)
        
        self.set_status(200)
        self.set_header("Content-Type", "text/html")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "*")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.set_header("Access-Control-Max-Age", 1000)
        self.set_header("Access-Control-Allow-Headers", "*")
        self.write(HomeIndex)

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
        ContactRequestBody = self.request.body.decode('utf-8').replace("+"," ")
        if ContactRequestBody.find("CFn=") >= 0 and ContactRequestBody.find("CFe=") >= 0 and ContactRequestBody.find("CFo=") >= 0 and ContactRequestBody.find("CFt=") >= 0:
            ContactRequestCFn = urllib.parse.unquote(ContactRequestBody[(ContactRequestBody.index("CFn=")+4):ContactRequestBody.index("&CFe=")])
            ContactRequestCFe = urllib.parse.unquote(ContactRequestBody[(ContactRequestBody.index("CFe=")+4):ContactRequestBody.index("&CFo=")])
            ContactRequestCFo = urllib.parse.unquote(ContactRequestBody[(ContactRequestBody.index("CFo=")+4):ContactRequestBody.index("&CFt=")])
            ContactRequestCFt = urllib.parse.unquote(ContactRequestBody[(ContactRequestBody.index("CFt=")+4):len(ContactRequestBody)])
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
        SignInRequestBody = self.request.body.decode('utf-8')
        if SignInRequestBody.find("siem=") >= 0 and SignInRequestBody.find("sipw=") >= 0:
            SignInRequestEmail = urllib.parse.unquote(SignInRequestBody[(SignInRequestBody.index("siem=")+5):SignInRequestBody.index("&sipw=")])
            SignInRequestPassword = urllib.parse.unquote(SignInRequestBody[(SignInRequestBody.index("sipw=")+5):len(SignInRequestBody)])
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
        ForgotPWRequestBody = self.request.body.decode('utf-8')
        if ForgotPWRequestBody.find("fpem=") >= 0:
            ForgotPWRequestEmail = urllib.parse.unquote(ForgotPWRequestBody[(ForgotPWRequestBody.index("fpem=")+5):len(ForgotPWRequestBody)])
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
            ResetPWRequestBody = self.request.body.decode('utf-8')
            ResetPWCookieFu = int(self.get_secure_cookie("Fu"))
            if ResetPWRequestBody.find("rppw=") >= 0 and ResetPWRequestBody.find("rppa=") >= 0:
                ResetPWRequestNewPWPre = urllib.parse.unquote(ResetPWRequestBody[(ResetPWRequestBody.index("rppw=")+5):ResetPWRequestBody.index("&rppa=")])
                ResetPWRequestNewPWAgain = urllib.parse.unquote(ResetPWRequestBody[(ResetPWRequestBody.index("rppa=")+5):len(ResetPWRequestBody)])
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
        SignUpRequestBody = self.request.body.decode('utf-8')
        if SignUpRequestBody.find("suem=") >= 0 and SignUpRequestBody.find("supw=") >= 0 and SignUpRequestBody.find("supa=") >= 0:
            SignUpRequestEmail = urllib.parse.unquote(SignUpRequestBody[(SignUpRequestBody.index("suem=")+5):SignUpRequestBody.index("&supw=")])
            SignUpRequestDBSelectEmail = "SELECT COUNT(*) FROM compacc WHERE email='{0:s}' and veremail=1".format(SignUpRequestEmail)
            mycursor.execute(SignUpRequestDBSelectEmail)
            QueryCountEmail = mycursor.fetchone()
            SignUpRequestPasswordPre = urllib.parse.unquote(SignUpRequestBody[(SignUpRequestBody.index("supw=")+5):SignUpRequestBody.index("&supa=")])
            SignUpRequestPassword = Enc32a.encrypt(SignUpRequestPasswordPre.encode()).decode('utf-8')
            SignUpRequestPasswordAgain = urllib.parse.unquote(SignUpRequestBody[(SignUpRequestBody.index("supa=")+5):len(SignUpRequestBody)])
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
            SignUpRSVEEmail = urllib.parse.unquote(SignUpRequestBody[(SignUpRequestBody.index("rsve=")+5):len(SignUpRequestBody)])
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
                AccountOrdersListStatus = AccountOrdersFetch[OFi][3]
                for OFIk,OFIv in ShippingCodesList:
                    AccountOrdersListStatus = AccountOrdersListStatus.replace(OFIk,OFIv)
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
            ProductRequested_Price = float(FindProduct(ProductRequested_ID)["Price"])
            ProductRequested_DiscountPre = int(FindProduct(ProductRequested_ID)["Discount"])
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
            ProductRequested_ImageCnt = len(fnmatch.filter(os.listdir("/root/maxima/static/product/"+ProductRequested_ID+"/"), "*.jpg"))
            ProductRequested_BPs = ""
            for BPSi in range(0,ProductRequested_ImageCnt):
                ProductRequested_BPs += "<li><img src=\"/static/product/"+ProductRequested_ID+"/"+str(BPSi)+".jpg\" alt=\""+ProductRequested_Name+" ("+str(BPSi + 1)+")\"></li>\n"
            ProductRequested_Rating = 0
            ProductRequested_ReviewCount = 0
        
            ProductIndex = ProductIndex.replace("<% ProductID %>",ProductRequested_ID)
            ProductIndex = ProductIndex.replace("<% ProductName %>",ProductRequested_Name)
            ProductIndex = ProductIndex.replace("<% ProductPrice %>",ProductRequested_PriceSet)
            ProductIndex = ProductIndex.replace("<% FullImageList %>",ProductRequested_BPs)
            ProductIndex = ProductIndex.replace("<% Rating %>",str(ProductRequested_Rating))
            ProductIndex = ProductIndex.replace("<% ReviewCount %>",str(ProductRequested_ReviewCount))
            self.write(ProductIndex)
        else:
            self.write(NotFoundIndex)

class TermsConditionsHand(tornado.web.RequestHandler):
    def get(self):
        # Open
        TermsConditionsIndex = ServePage(self,"/legal/terms.html")
        self.write(TermsConditionsIndex)

class NotFoundHand(tornado.web.RequestHandler):
    def get(self):
        # Open
        NotFoundIndex = ServePage(self,"/status/404.html")
        self.write(NotFoundIndex)
