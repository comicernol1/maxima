import os,re,random,base64,fnmatch,json,tornado.web,urllib.parse,mysql.connector,smtplib
from http.cookies import Morsel
from datetime import datetime
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

def AcceptCookies(self):
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

# User Currency
SpecifyCurrencyList = ["$"]
UserCurrency = "USD"
if UserCurrency=="USD" or UserCurrency=="CAD":
    UserCurrencySymbol = "$"
elif UserCurrency=="EUR":
    UserCurrencySymbol = "€"
else:
    UserCurrencySymbol = "(?)"

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

def ServePage(self,pageloc,ForceLogin):
    RequestedHostName = self.request.host
    RequestedHostBase = RequestedHostName[0:RequestedHostName.index(".com")]
    
    # User Language
    global UserLanguage
    if self.get_cookie("Fn"):
        UserInfoFn = str(self.get_cookie("Fn")).lower()
    else:
        UserInfoFn = ""
    if self.get_cookie("FL"):
        UserInfoFL = str(self.get_cookie("FL")).lower()
    else:
        UserInfoFL = ""
    AcceptedLanguages = {"en":"English","fr":"Français"}
    if UserInfoFL != "" and UserInfoFL in AcceptedLanguages:
        UserLanguage = UserInfoFL
    else:
        UserLanguage = ""
        UserLanguagesUnclean = re.split(" |,|;",str(self.request.headers.get("Accept-Language")))
        UserLanguagesList = []
        for i in UserLanguagesUnclean:
            if len(i) == 2:
                UserLanguagesList.append(i)
                if i in AcceptedLanguages.keys() and UserLanguage == "":
                    UserLanguage = i
        if UserLanguage == "":
            UserLanguage = "en"
    LanguageListDefault = ""
    LanguageOptions = ""
    if UserLanguage in AcceptedLanguages:
        for i in AcceptedLanguages.keys():
            if i == UserLanguage:
                SelectedLanguageLi = " selected"
                LanguageListDefault = "<option value=\""+i+"\" selected>"+AcceptedLanguages[i]+"</option>"
            else:
                SelectedLanguageLi = ""
            LanguageOptions += "<option value=\""+i+"\""+SelectedLanguageLi+">"+AcceptedLanguages[i]+"</option>"
    else:
        SelectedLanguageLi = ""
    
    
    # User Nation
    global NationDict,NationDict_EN,NationDict_FR
    NationDict_EN = {"af":"Afghanistan","al":"Albania","dz":"Algeria","as":"American Samoa","ad":"Andorra","ao":"Angola","ai":"Anguilla","aq":"Antarctica","ag":"Antigua & Barbuda","ar":"Argentina","am":"Armenia","aw":"Aruba","au":"Australia","at":"Austria","az":"Azerbaijan","bs":"Bahamas","bh":"Bahrain","bd":"Bangladesh","bb":"Barbados","by":"Belarus","be":"Belgium","bz":"Belize","bj":"Benin","bm":"Bermuda","bt":"Bhutan","bo":"Bolivia","ba":"Bosnia & Herzegovina","bw":"Botswana","bv":"Bouvet Island","br":"Brazil","io":"BIOT","bn":"Brunei Darussalam","bg":"Bulgaria","bf":"Burkina Faso","bi":"Burundi","kh":"Cambodia","cm":"Cameroon","ca":"Canada","cv":"Cape Verde","ky":"Cayman Islands","cf":"Central African Republic","td":"Chad","cl":"Chile","cn":"China","cx":"Christmas Island","cc":"Cocos Islands","co":"Colombia","km":"Comoros","cg":"Congo","cd":"DR Congo","ck":"Cook Islands","cr":"Costa Rica","ci":"Côte d'Ivoire","hr":"Croatia","cu":"Cuba","cy":"Cyprus","cz":"Czech Republic","dk":"Denmark","dj":"Djibouti","dm":"Dominica","do":"Dominican Republic","ec":"Ecuador","eg":"Egypt","eh":"Western Sahara","sv":"El Salvador","gq":"Equatorial Guinea","er":"Eritrea","ee":"Estonia","et":"Ethiopia","fk":"Falkland Islands","fo":"Faroe Islands","fj":"Fiji","fi":"Finland","fr":"France","gf":"French Guiana","pf":"French Polynesia","tf":"French Southern Territories","ga":"Gabon","gm":"Gambia","ge":"Georgia","de":"Germany","gh":"Ghana","gi":"Gibraltar","gr":"Greece","gl":"Greenland","gd":"Grenada","gp":"Guadeloupe","gu":"Guam","gt":"Guatemala","gn":"Guinea","gw":"Guinea-Bissau","gy":"Guyana","ht":"Haiti","hm":"Heard & Mcdonald Islands","hn":"Honduras","hk":"Hong Kong","hu":"Hungary","is":"Iceland","in":"India","id":"Indonesia","ir":"Iran","iq":"Iraq","ie":"Ireland","il":"Israel","it":"Italy","jm":"Jamaica","jp":"Japan","jo":"Jordan","kz":"Kazakhstan","ke":"Kenya","ki":"Kiribati","kr":"South Korea","kw":"Kuwait","kg":"Kyrgyzstan","la":"Laos","ly":"Latvia","lb":"Lebanon","ls":"Lesotho","lr":"Liberia","ly":"Libya","li":"Liechtenstein","lt":"Lithuania","lu":"Luxembourg","mo":"Macao","mk":"Macedonia","mg":"Madagascar","mw":"Malawi","my":"Malasia","mv":"Maldives","ml":"Mali","mt":"Malta","mh":"Marshall Islands","mq":"Martinique","mr":"Mauritania","mu":"Mauritius","yt":"Mayotte","mx":"Mexico","fm":"Micronesia","md":"Moldova","mc":"Monaco","mn":"Mongolia","ms":"Montserrat","ma":"Morocco","mz":"Mozambique","mm":"Myanmar","na":"Nambia","nr":"Nauru","np":"Nepal","nl":"Netherlands","an":"Netherlands Antilles","nc":"New Caledonia","nz":"New Zealand","ni":"Nicaragua","ne":"Niger","ng":"Nigeria","nu":"Niue","nf":"Norfold Island","mp":"Northern Marina Islands","no":"Norway","om":"Oman","pk":"Pakistan","pw":"Palau","ps":"Palestine","pa":"Panama","pg":"Papua New Guinea","py":"Paraguay","pe":"Peru","ph":"Philippines","pn":"Pitcairn","pl":"Poland","pt":"Portugal","pr":"Puerto Rico","qa":"Qatar","re":"Réunion","ro":"Romania","ru":"Russia","rw":"Rwanda","sh":"Saint Helena","kn":"Saint Kitts & Nevis","lc":"Saint Lucia","pm":"Saint Pierre & Miquelon","vc":"Saint Vincent & Grenadines","ws":"Samoa","sm":"San Marino","st":"Sao Tome & Principe","sa":"Saudi Arabia","sn":"Senegal","cs":"Serbia & Montenegro","sc":"Seychelles","sl":"Sierra Leone","sg":"Singapore","sk":"Slovakia","si":"Slovenia","sb":"Solomon Islands","so":"Somalia","za":"South Africa","gs":"South Georgia","es":"Spain","lk":"Sri Lanka","sd":"Sudan","sr":"Suriname","sj":"Svalbard & Jan Mayen","sz":"Swaziland","se":"Sweden","ch":"Switzerland","sy":"Syria","tw":"Taiwan","tj":"Tajikistan","tz":"Tanzania","th":"Thailand","tl":"Timor-Leste","tg":"Togo","tk":"Tokelau","to":"Tonga","tt":"Trinidad & Tobago","tn":"Tunisia","tr":"Turkey","tm":"Turkmenistan","tc":"Turks & Caicos","tv":"Tuvalu","ug":"Uganda","ua":"Ukraine","ae":"United Arab Emirates","gb":"United Kingdom","us":"United States","um":"US Minor Outlying Islands","uy":"Uruguay","uz":"Uzbekistan","ve":"Venezuela","vu":"Vanuatu","vn":"Vietnam","vg":"British Virgin Islands","vi":"US Virgin Islands","wf":"Wallis & Futuna","ye":"Yemen","zw":"Zimbabwe"}
    NationDict_FR = {"af":"Afghanistan","al":"Albanie","dz":"Algérie","as":"Samoa Américaines","ad":"Andorre","ao":"Angola","ai":"Anguilla","aq":"Antarctique","ag":"Antigua & Barbuda","ar":"Argentine","am":"Arménie","aw":"Aruba","au":"Australie","at":"Autriche","az":"Azerbaïdjan","bs":"Bahamas","bh":"Bahrein","bd":"Bangladesh","bb":"Barbade","by":"Biélorussie","be":"Belgique","bz":"Belize","bj":"Bénin","bm":"Bermudes","bt":"Bhoutan","bo":"Bolivie","ba":"Bosnie-Herzegovine","bw":"Botswana","bv":"Île Bouvet","br":"Brésil","io":"BIOT","bn":"Brunei Darussalam","bg":"Bulgarie","bf":"Burkina Faso","bi":"Burundi","kh":"Cambodge","cm":"Cameroun","ca":"Canada","cv":"Cap-Vert","ky":"Îles Caïmans","cf":"République Centrafricaine","td":"Tchad","cl":"Chili","cn":"Chine","cx":"Île de Noël","cc":"Îles Cocos","co":"Colombie","km":"Comores","cg":"Congo","cd":"RD Congo","ck":"Îles Cook","cr":"Costa Rica","ci":"Côte d'Ivoire","hr":"Croatie","cu":"Cuba","cy":"Chypre","cz":"République Tchèque","dk":"Danemark","dj":"Djibouti","dm":"Dominique","do":"République Dominicaine","ec":"Équateur","eg":"Egypte","eh":"Sahara Occidental","sv":"Le Salvador","gq":"Guinée Équatoriale","er":"Érythrée","ee":"Estonie","et":"Ethiopie","fk":"Îles Falkland","fo":"Îles Féroé","fj":"Fidji","fi":"Finlande","fr":"France","gf":"Guyane Française","pf":"Polynésie Française","tf":"Territoires Français du Sud","ga":"Gabon","gm":"Gambie","ge":"Géorgie","de":"Allemagne","gh":"Ghana","gi":"Gibraltar","gr":"Grèce","gl":"Groenland","gd":"Grenade","gp":"Guadeloupe","gu":"Guam","gt":"Guatemala","gn":"Guinée","gw":"Guinée-Bissau","gy":"Guyane","ht":"Haïti","hm":"Îles Heard et Mcdonald","hn":"Honduras","hk":"Hong Kong","hu":"Hongrie","is":"Islande","in":"Inde","id":"Indonésie","ir":"Iran","iq":"Irak","ie":"Irlande","il":"Israël","it":"Italie","jm":"Jamaïque","jp":"Japon","jo":"Jordan","kz":"Kazakhstan","ke":"Kenya","ki":"Kiribati","kr":"Corée du Sud","kw":"Koweit","kg":"Kirghizistan","la":"Laos","ly":"Lettonie","lb":"Liban","ls":"Lesotho","lr":"Libéria","ly":"Libye","li":"Liechtenstein","lt":"Lituanie","lu":"Luxembourg","mo":"Macao","mk":"Macédoine","mg":"Madagascar","mw":"Malawi","my":"Malasia","mv":"Maldives","ml":"Mali","mt":"Malte","mh":"Îles Marshall","mq":"Martinique","mr":"Mauritanie","mu":"Maurice","yt":"Mayotte","mx":"Mexique","fm":"Micronésie","md":"Moldova","mc":"Monaco","mn":"Mongolie","ms":"Montserrat","ma":"Maroc","mz":"Mozambique","mm":"Myanmar","na":"Nambia","nr":"Nauru","np":"Népal","nl":"Pays-Bas","an":"Antilles Néerlandaises","nc":"Nouvelle Calédonie","nz":"Nouvelle-Zélande","ni":"Nicaragua","ne":"Niger","ng":"Nigeria","nu":"Niue","nf":"Île de Norfolk","mp":"Îles du Nord de la Marina","no":"Norvège","om":"Oman","pk":"Pakistan","pw":"Palau","ps":"Palestine","pa":"Panama","pg":"Papouasie Nouvelle Guinée","py":"Paraguay","pe":"Pérou","ph":"Philippines","pn":"Pitcairn","pl":"Pologne","pt":"Portugal","pr":"Porto Rico","qa":"Qatar","re":"Réunion","ro":"Roumanie","ru":"Russie","rw":"Rwanda","sh":"Sainte-Hélène","kn":"Saint-Kitts-et-Nevis","lc":"Sainte-Lucie","pm":"Saint Pierre et Miquelon","vc":"Saint Vincent et Grenadines","ws":"Samoa","sm":"Saint Marin","st":"Sao Tomé et Principe","sa":"Arabie Saoudite","sn":"Sénégal","cs":"Serbie & Monténégro","sc":"Seychelles","sl":"Sierra Leone","sg":"Singapour","sk":"Slovaquie","si":"Slovénie","sb":"Îles Salomon","so":"Somalie","za":"Afrique du Sud","gs":"Géorgie du Sud","es":"Espagne","lk":"Sri Lanka","sd":"Soudan","sr":"Suriname","sj":"Svalbard & Jan Mayen","sz":"Swaziland","se":"Suède","ch":"Suisse","sy":"Syrie","tw":"Taïwan","tj":"Tajikistan","tz":"Tanzanie","th":"Thaïlande","tl":"Timor-Leste","tg":"Aller","tk":"Tokelau","to":"Tonga","tt":"Trinidad & Tobago","tn":"Tunisie","tr":"Turquie","tm":"Turkménistan","tc":"Turks & Caicos","tv":"Tuvalu","ug":"Ouganda","ua":"Ukraine","ae":"Emirats Arabes Unis","gb":"Royaume-Uni","us":"États Unis","um":"Îles Mineures des ÉU","uy":"Uruguay","uz":"Ouzbékistan","ve":"Venezuela","vu":"Vanuatu","vn":"Vietnam","vg":"Îles Vierges Britanniques","vi":"Îles Vierges Américaines","wf":"Wallis et Futuna","ye":"Yémen","zw":"Zimbabwe"}
    exec("NationDict = NationDict_"+UserLanguage.upper(), globals())
    if UserInfoFn != "" and UserInfoFn in NationDict_EN.keys():
        UserNation = UserInfoFn
    else:
        UserNation = "us"
    NationList = ""
    NationListDefault = ""
    NationDictKeys = NationDict.keys()
    for i in NationDictKeys:
        if i == UserNation:
            SelectedNationLi = " selected"
            NationListDefault = "<option value=\""+i+"\" selected>"+NationDict[i]+"</option>"
        else:
            SelectedNationLi = ""
        NationList += "<option value=\""+i+"\""+SelectedNationLi+">"+NationDict[i]+"</option>\n"
    
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
    with open("/root/maxima/"+RequestedHostBase+"/"+UserLanguage+"/templates/head.html") as HeadHTML_F:
        HeadHTML = HeadHTML_F.read()
    with open("/root/maxima/"+RequestedHostBase+"/"+UserLanguage+"/templates/footer.html") as FooterHTML_F:
        FooterHTML = FooterHTML_F.read()
    
    # Open Requested Page
    try:
        with open("/root/maxima/"+RequestedHostBase+"/"+UserLanguage+"/req"+str(pageloc)) as PageIndex_F:
            PageIndex = PageIndex_F.read()
    except FileNotFoundError:
        with open("/root/maxima/"+RequestedHostBase+"/"+UserLanguage+"/req/status/incomplete.html") as PageIndex_F:
            PageIndex = PageIndex_F.read()
    if CheckLogin(self) or ForceLogin and self.get_cookie("Fu"):
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
    else:
        UserInfoFa = "false"
    if UserInfoFa == "true":
        FooterHTML = FooterHTML.replace("<% CookieNotif %>","")
        FooterHTML = FooterHTML.replace("<% NationOptions %>",NationList)
        FooterHTML = FooterHTML.replace("<% LanguageOptions %>",LanguageOptions)
    else:
        FooterHTML = FooterHTML.replace("<% CookieNotif %>",CookieNotifDiv)
        FooterHTML = FooterHTML.replace("<% NationOptions %>",NationListDefault)
        FooterHTML = FooterHTML.replace("<% LanguageOptions %>",LanguageListDefault)
    PageIndex = PageIndex.replace("<% Footer %>",FooterHTML)
    PageIndex = PageIndex.replace("<% NationOptions %>",NationList)
    
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

def CreateCookie(self,cookie_name: str,cookie_value: str,cookie_expires: int,*args,**kwargs):
    RequestedHostName = self.request.host
    if cookie_expires != None:
        ExpiresDateString = datetime.fromtimestamp(int(datetime.today().timestamp())+cookie_expires)
    else:
        ExpiresDateString = None
        
    # self.set_cookie(str(cookie_name),str(cookie_value),RequestedHostName,ExpiresDateString,"/",SameSite="Strict")
    # self.set_cookie('trakr', 'email', httponly=True, samesite="None")
    C = Morsel()
    C.key = str(cookie_name)
    C.value = str(cookie_value)
    C.coded_value = str(cookie_value)
    print(C.output())

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

def FindProduct(pid):
    FindProductQuery = "SELECT disp,ttl,description,price_"+UserCurrency.lower()+",discount,colour,colour_name,contents_dict,wash,bleach,dry,wring,dryclean from products where id='{0:d}'".format(int(pid))
    mycursor.execute(FindProductQuery)
    FindProductFetch = mycursor.fetchone()
    if FindProductFetch:
        FindProductDisp = int(FindProductFetch[0])
        FindProductName = str(FindProductFetch[1])
        FindProductDesc = str(FindProductFetch[2])
        FindProductPrice = float(FindProductFetch[3])
        FindProductDiscount = int(FindProductFetch[4])
        FindProductColour = str(FindProductFetch[5])
        FindProductColourName = str(FindProductFetch[6]).title()
        FindProductContentsDict = json.loads(FindProductFetch[7])
        FindProductWash = str(FindProductFetch[8])
        FindProductBleach = str(FindProductFetch[9])
        FindProductDry = str(FindProductFetch[10])
        FindProductWring = str(FindProductFetch[11])
        FindProductDryClean = str(FindProductFetch[12])
        if os.path.exists("/static/product/"+str(pid)+"/0.jpg"):
            FindProductHasImg = True
        else:
            FindProductHasImg = False
        FindProductDict = {"Display":FindProductDisp,"Name":FindProductName,"Description":FindProductDesc,"Price":FindProductPrice,"Discount":FindProductDiscount,"Colour":FindProductColour,"ColourName":FindProductColourName,"ContentsDict":FindProductContentsDict,"Wash":FindProductWash,"Bleach":FindProductBleach,"Dry":FindProductDry,"Wring":FindProductWring,"DryClean":FindProductDryClean,"HasImg":FindProductHasImg}
    else:
        FindProductDict = {"Display":0,"Name":"","Description":"","Price":0.00,"Discount":0,"Colour":"000000","ColourName":"","ContentsDict":{'Main':['']},"Wash":"0","Bleach":"0","Dry":"0","Wring":"0","DryClean":"0","HasImg":False}
    return FindProductDict

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
WashCareCodesList = {"0":"","a":"Machine Wash Normal","b":"Machine Wash Cold (30°C)","c":"Machine Wash Warm (40°C)","d":"Machine Was Hot (50°C)","e":"Machine Wash Hot (60°C)","f":"Machine Wash Hot (70°C)","g":"Machine Wash Hot (95°C)","h":"Machine Wash Permanent Press","i":"Machine Wash Cold Permanent Press (30°C)","j":"Machine Wash Warm Permanent Press (40°C)","k":"Machine Wash Hot Permanent Press","m":"Machine Wash Hot Permanent Press (50°C)","o":"Machine Wash Hot Permanent Press (70°C)","p":"Machine Wash Hot Permanent Press (95°C)","q":"Machine Wash Gentle","r":"Machine Wash Cold Gentle (30°C)","s":"Machine Wash Warm Gentle (40°C)","t":"Machine Wash Hot Gentle (50°C)","u":"Machine Wash Hot Gentle (60°C)","v":"Machine Wash Hot Gentle (70°C)","w":"Machine Wash Hot Gentle (95°C)","x":"Hand Wash Normal","y":"Hand Wash Cold (30°C)","z":"Hand Wash Warm (40°C)","n":"Do Not Wash"}
BleachCareCodesList = {"0":"","a":"Bleach When Needed","b":"Non-Chlorine Bleach When Needed","n":"Do Not Bleach"}
DryCareCodesList = {"0":"","a":"Tumble Dry Normal","b":"Tumble Dry Normal Low Heat","c":"Tumble Dry Normal Medium Heat","d":"Tumble Dry Normal High Heat","e":"Tumble Dry Normal No Heat","f":"Tumble Dry Permanent Press","g":"Tumble Dry Permanent Press Low Heat","h":"Tumble Dry Permanent Press Medium Heat","i":"Tumble Dry Permanent Press High Heat","j":"Tumble Dry Gentle","k":"Tumble Dry Gentle Low Heat","m":"Tumble Dry Gentle Medium Heat","o":"Tumble Dry Gentle High Heat","p":"Tumble Dry Gentle No Heat","q":"Do Not Tumble Dry","n":"Do Not Dry","r":"Line Dry","s":"Line Dry In Shade","t":"Drip Dry","u":"Drip Dry In Shade","v":"Dry Flat","w":"Dry Flat In Shade"}
DryCleanCareCodesList = {"0":"","a":"Dry Clean","b":"Dry Clean Any Solvent","c":"Dry Clean Petroleum Solvent Only","d":"Dry Clean Any Colvent Except Trichloroethylene","e":"Dry Clean Low Heat","f":"Dry Clean No Steam","g":"Dry Clean Reduced Moisture","h":"Dry Clean Short Cycle","i":"Dry Clean Any Solvent Low Heat","j":"Dry Clean Any Solvent No Steam","k":"Dry Clean Any Solvent Reduced Moisture","m":"Dry Clean Any Solvent Short Cycle","n":"Do Not Dry Clean"}
