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

def SetCookie(self):
    CheckCookieRequestBody = self.request.body.decode('utf-8')
    if CheckCookieRequestBody.find("ackc=") >= 0:
        CheckCookieRequestM = urllib.parse.unquote(CheckCookieRequestBody[(CheckCookieRequestBody.index("ackc=")+5):len(CheckCookieRequestBody)])
        if CheckCookieRequestM == "true":
            self.set_secure_cookie("Fa","true")
            self.redirect(self.request.uri)
            return True
        else:
            return False
    else:
        return False

def ServePage(self,pageloc):
    # Define Basics
    HeaderLISignIn = "<a id=\"HMs\" href=\"/sign_in/\">Sign In</a>"
    HeaderLIAccountButton = "<a id=\"HMs\" href=\"/account/\">My Account<span></span></a><a id=\"HMc\" href=\"/cart/\" title=\"My Cart\"><span>0</span></a>"
    CookieNotifDiv = "<form id=\"Sackc\" action=\"\" method=\"POST\"><input type=\"hidden\" name=\"ackc\" value=\"true\"></form><div id=\"Fackc\">By continuing to use this site, you agree to our <a href=\"/legal/cookie_policy/\">Cookie Policy</a>. <b onclick=\"ackc()\">Accept</b></div>"
    
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
    try:
        UserInfoFa = self.get_secure_cookie("Fa").decode('utf-8')
    except:
        UserInfoFa = "false"
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

def FindProductColours(pid):
    UniversalPID = pid[0:7]
    RequestDBColours = "SELECT colour,colour_name from products where left(id,7)='{0:s}'".format(UniversalPID)
    mycursor.execute(RequestDBColours)
    ColoursFetch = mycursor.fetchall()
    ColoursList = []
    ColourNamesList = []
    if ColoursFetch:
        for i in ColoursFetch:
            ColoursList.append(ColoursFetch[i][0])
            ColourNamesList.append(ColoursFetch[i][1])
    ColoursDict = {"Hex":ColoursList,"Name":ColourNamesList}
    return ColoursDict

ShippingCodesList = [("p","In Production"),("i","In Progress"),("d","Delivered")]
