import os,re,random,base64,fnmatch,json,tornado.web,urllib.parse,mysql.connector,smtplib
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
mycursor = db.cursor(buffered=True)

def ValidEmail(eml):
    rgx = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if(re.search(rgx,eml)):
        return True
    else:
        return False

def CheckLogin(self):
    if self.get_cookie("Fu") and self.get_cookie("Ft"):
        UserInfoFu = self.get_cookie("Fu")
        UserInfoFt = self.get_cookie("Ft")
        UserInfoLoginQuery = "SELECT * from compacc where userid='{0:d}' and token='{1:d}'".format(int(UserInfoFu),int(UserInfoFt))
        mycursor.execute(UserInfoLoginQuery)
        UserInfoLoginFetch = mycursor.fetchone()
        if UserInfoLoginFetch:
            return True
        else:
            return False
    else:
        return False

def SendVerificationEmail(self,eml):
    SVEVerifyCode = random.randint(1000000000,9999999999)
    SVERequestDBUpdate = "UPDATE compacc SET tmpcode='{0:d}' WHERE email='{1:s}' LIMIT 1".format(SVEVerifyCode,eml)
    mycursor.execute(SVERequestDBUpdate)
    db.commit()
    with open("/root/maxima/templates/sign_up/conf_email.html") as SVESMPTTemplate_F:
        SVESMTPTemplate = SVESMPTTemplate_F.read()
    SVESMTPTemplate = SVESMTPTemplate.replace("<% UserCode %>",str(SVEVerifyCode))
    SVESMTPHeaders = "\r\n".join(["from: comicernol@gmail.com","subject: Verify Your Email - FRANZAR","to:"+eml,"mime-version: 1.0","content-type: text/html"])
    SVESMTPContent = SVESMTPHeaders+"\r\n\r\n"+SVESMTPTemplate
    SVEMail = smtplib.SMTP('smtp.gmail.com',587)
    SVEMail.ehlo()
    SVEMail.starttls()
    SVEMail.login('comicernol@gmail.com',str(os.environ["Comicernol_Gmail_Passwd"]))
    SVEMail.sendmail('comicernol@gmail.com',eml,SVESMTPContent)
    SVEMail.close()

def SetCookie(self):
    CheckCookieRequestBody = self.request.body.decode('utf-8')
    if CheckCookieRequestBody.find("ackc=") >= 0:
        CheckCookieRequestM = urllib.parse.unquote(CheckCookieRequestBody[(CheckCookieRequestBody.index("ackc=")+5):len(CheckCookieRequestBody)])
        if CheckCookieRequestM == "true":
            self.set_cookie("Fa","true")
            self.redirect(self.request.uri)
            return True
        else:
            return False
    else:
        return False

def GetCart(self):
    UserInfoFu = self.get_cookie("Fu")
    UserCartQuery = "SELECT pid,qty from cart where uid='{0:d}'".format(int(UserInfoFu))
    mycursor.execute(UserCartQuery)
    UserCartFetch = mycursor.fetchall()
    UserCartList = []
    for i in range(0,len(UserCartFetch)):
        UserCartItm = []
        UserCartItm.append(UserCartFetch[i][0])
        UserCartItm.append(UserCartFetch[i][1])
        UserCartList.append(UserCartItm)
    return UserCartList

def ServePage(self,pageloc):
    # Define Basics
    HeaderLISignIn = "<a id=\"HMs\" href=\"/sign_in/\">Sign In</a>"
    CookieNotifDiv = "<form id=\"Fackc\" action=\"\" method=\"POST\">By continuing to use this site, you agree to our <a href=\"/legal/cookie_policy/\">Cookie Policy</a>. <input type=\"hidden\" name=\"ackc\" value=\"true\"><input type=\"submit\" value=\"Accept\"></form>"
    
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
        UserCartCnt = 0
        UserCartList = GetCart(self)
        for i in range(0,len(UserCartList)):
            UserCartCnt += int(UserCartList[i][1])
        HeaderLIAccountButton = "<a id=\"HMs\" href=\"/account/\" title=\"My Account\">My Account<span></span></a><a id=\"HMc\" href=\"/cart/\" title=\"My Cart\"><span id=\"HMCi\">"+str(UserCartCnt)+"</span></a>"
        PageIndex = PageIndex.replace("<% HeaderLI %>",HeaderLIPre+HeaderLIAccountButton)
    else:
        PageIndex = PageIndex.replace("<% HeaderLI %>",HeaderLIPre+HeaderLISignIn)
    PageIndex = PageIndex.replace("<% Head %>",HeadHTML)
    if self.get_cookie("Fa"):
        UserInfoFa = str(self.get_cookie("Fa"))
    print(UserInfoFa)
    if UserInfoFa == "true":
        FooterHTML = FooterHTML.replace("<% CookieNotif %>","")
    else:
        FooterHTML = FooterHTML.replace("<% CookieNotif %>",CookieNotifDiv)
    PageIndex = PageIndex.replace("<% Footer %>",FooterHTML)
    
    # Return Page
    self.set_status(200)
    self.set_header("Content-Type", "text/html")
    self.set_header("Access-Control-Allow-Origin", "*")
    self.set_header("Access-Control-Allow-Headers", "*")
    self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
    self.set_header("Access-Control-Max-Age", 1000)
    self.set_header("Access-Control-Allow-Headers", "*")
    self.set_header("Server", "Harrison Sienkiewicz (Tornado Server)")
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
        FindProductQuery = "SELECT ttl,description,price_"+UserCurrency.lower()+",discount,colour,colour_name,contents_dict,wash,bleach,dry,wring,dryclean from products where id='{0:d}'".format(int(pid))
        mycursor.execute(FindProductQuery)
        FindProductFetch = mycursor.fetchone()
        FindProductName = str(FindProductFetch[0])
        FindProductDesc = str(FindProductFetch[1])
        FindProductPrice = float(FindProductFetch[2])
        FindProductDiscount = int(FindProductFetch[3])
        FindProductColour = str(FindProductFetch[4])
        FindProductColourName = str(FindProductFetch[5]).title()
        FindProductContentsDict = json.loads(FindProductFetch[6])
        FindProductWash = str(FindProductFetch[7])
        FindProductBleach = str(FindProductFetch[8])
        FindProductDry = str(FindProductFetch[9])
        FindProductWring = str(FindProductFetch[10])
        FindProductDryClean = str(FindProductFetch[11])
        if os.path.exists("/static/product/"+str(pid)+"/0.jpg"):
            FindProductHasImg = True
        else:
            FindProductHasImg = False
        FindProductDict = {"Name":FindProductName,"Description":FindProductDesc,"Price":FindProductPrice,"Discount":FindProductDiscount,"Colour":FindProductColour,"ColourName":FindProductColourName,"ContentsDict":FindProductContentsDict,"Wash":FindProductWash,"Bleach":FindProductBleach,"Dry":FindProductDry,"Wring":FindProductWring,"DryClean":FindProductDryClean,"HasImg":FindProductHasImg}
        return FindProductDict
    finally:
        pass

def FindProductColours(pid):
    UniversalPID = pid[0:7]
    RequestDBColours = "SELECT id,colour,colour_name from products where left(id,7)='{0:s}'".format(UniversalPID)
    mycursor.execute(RequestDBColours)
    ColoursFetch = mycursor.fetchall()
    IDsList = []
    ColoursList = []
    ColourNamesList = []
    if ColoursFetch:
        for i in range(0,len(ColoursFetch)):
            PIDID = str(ColoursFetch[i][0])
            PIDColour = str(ColoursFetch[i][1])
            PIDColourName = str(ColoursFetch[i][2]).title()
            IDsList.append(PIDID)
            ColoursList.append(PIDColour)
            ColourNamesList.append(PIDColourName)
    ColoursDict = {"ID":IDsList,"Hex":ColoursList,"Name":ColourNamesList}
    return ColoursDict

ShippingCodesList = {"p":"In Production","i":"In Progress","d":"Delivered"}
WashCareCodesList = {"a":"Machine Wash Normal","b":"Machine Wash Cold (30°C)","c":"Machine Wash Warm (40°C)","d":"Machine Was Hot (50°C)","e":"Machine Wash Hot (60°C)","f":"Machine Wash Hot (70°C)","g":"Machine Wash Hot (95°C)","h":"Machine Wash Permanent Press","i":"Machine Wash Cold Permanent Press (30°C)","j":"Machine Wash Warm Permanent Press (40°C)","k":"Machine Wash Hot Permanent Press","m":"Machine Wash Hot Permanent Press (50°C)","o":"Machine Wash Hot Permanent Press (70°C)","p":"Machine Wash Hot Permanent Press (95°C)","q":"Machine Wash Gentle","r":"Machine Wash Cold Gentle (30°C)","s":"Machine Wash Warm Gentle (40°C)","t":"Machine Wash Hot Gentle (50°C)","u":"Machine Wash Hot Gentle (60°C)","v":"Machine Wash Hot Gentle (70°C)","w":"Machine Wash Hot Gentle (95°C)","x":"Hand Wash Normal","y":"Hand Wash Cold (30°C)","z":"Hand Wash Warm (40°C)","n":"Do Not Wash"}
BleachCareCodesList = {"a":"Bleach When Needed","b":"Non-Chlorine Bleach When Needed","n":"Do Not Bleach"}
DryCareCodesList = {"a":"Tumble Dry Normal","b":"Tumble Dry Normal Low Heat","c":"Tumble Dry Normal Medium Heat","d":"Tumble Dry Normal High Heat","e":"Tumble Dry Normal No Heat","f":"Tumble Dry Permanent Press","g":"Tumble Dry Permanent Press Low Heat","h":"Tumble Dry Permanent Press Medium Heat","i":"Tumble Dry Permanent Press High Heat","j":"Tumble Dry Gentle","k":"Tumble Dry Gentle Low Heat","m":"Tumble Dry Gentle Medium Heat","o":"Tumble Dry Gentle High Heat","p":"Tumble Dry Gentle No Heat","q":"Do Not Tumble Dry","n":"Do Not Dry","r":"Line Dry","s":"Line Dry In Shade","t":"Drip Dry","u":"Drip Dry In Shade","v":"Dry Flat","w":"Dry Flat In Shade"}
DryCleanCareCodesList = {"a":"Dry Clean","b":"Dry Clean Any Solvent","c":"Dry Clean Petroleum Solvent Only","d":"Dry Clean Any Colvent Except Trichloroethylene","e":"Dry Clean Low Heat","f":"Dry Clean No Steam","g":"Dry Clean Reduced Moisture","h":"Dry Clean Short Cycle","i":"Dry Clean Any Solvent Low Heat","j":"Dry Clean Any Solvent No Steam","k":"Dry Clean Any Solvent Reduced Moisture","m":"Dry Clean Any Solvent Short Cycle","n":"Do Not Dry Clean"}
