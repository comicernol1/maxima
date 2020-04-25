from udf import *

class handler(tornado.web.RequestHandler):
    def get(self):
        CartIndex = ServePage(self,"/cart/index.html",False)
        UserCartList = GetCart(self)
        UserCartListShipping = 1
        UserCartListTotal = 0
        UserCartItems = ""
        UserCartListLen = len(UserCartList)
        for i in range(0,UserCartListLen):
            UserCartItem_ID = int(UserCartList[i][0])
            if FindProduct(UserCartItem_ID)["HasImg"]:
                UserCartItem_ImgLink = "/static/product/{0:d}/0.jpg".format(UserCartItem_ID)
            else:
                UserCartItem_ImgLink = "/static/product/missing.jpg"
            UserCartItem_Price = FindProduct(UserCartItem_ID)["Price"]
            if UserCurrencySymbol in SpecifyCurrencyList:
                UserCartItem_PriceSet = "{0:s}{1:,.2f} ({2:s})".format(UserCurrencySymbol,UserCartItem_Price,UserCurrency)
            else:
                UserCartItem_PriceSet = "{0:s}{1:,.2f}".format(UserCurrencySymbol,UserCartItem_Price)
            if str(UserCartItem_ID)[0:7] != "1111111":
                UserCartItem_TemplateSet = "<h6 class=\"CIPt\">Size:</h6><select class=\"CIp\"><option>Master Crafted&trade;</option><option>X-Small</option><option>Small</option><option>Medium</option><option>Large</option><option>X-Large</option></select><span class=\"DDoB_B\"></span>"
            else:
                UserCartItem_TemplateSet = ""
            if str(UserCartItem_ID)[0:7] == "1111111":
                UserCartAdjustNumDisable = " disabled"
                UserCartRemoveButton = ""
            else:
                UserCartAdjustNumDisable = ""
                UserCartRemoveButton = "<button class=\"CIr\" onclick=\"RMp('{0:d}')\">Remove</button>".format(UserCartItem_ID)
            UserCartListTotal += (UserCartItem_Price*int(UserCartList[i][1]))
            UserCartListTotal += UserCartListShipping
            UserCartItems += "<div class=\"CIt\" id=\"CIt_{0:d}\" prc=\"{8:.2f}\" style=\"top:{1:d}px;\"><input class=\"CIq\" type=\"number\" value=\"{2:d}\" onblur=\"AdjOa()\"{3:s}><a href=\"/product/{0:d}/\" class=\"CIi\" style=\"background-image:url({4:s});\"></a>{5:s}<h3>{6:s}</h3><h1>{7:s}</h1>{9:s}</div>\n".format(UserCartItem_ID,(i*210),int(UserCartList[i][1]),UserCartAdjustNumDisable,UserCartItem_ImgLink,UserCartItem_TemplateSet,FindProduct(UserCartItem_ID)["Name"],UserCartItem_PriceSet,UserCartItem_Price,UserCartRemoveButton)
        if UserCartItems != "":
            if UserCurrencySymbol in SpecifyCurrencyList:
                UserCartTotalsSet = "<h3 id=\"CICh\">Shipping: {0:s}<u id=\"CICHt\">{1:,.2f}</u> ({2:s})</h3><hr id=\"CICTh\"><h3 id=\"CICt\">Total: {0:s}<u id=\"CICTt\">{3:,.2f}</u> ({2:s})</h3>".format(UserCurrencySymbol,UserCartListShipping,UserCurrency,UserCartListTotal)
            else:
                UserCartTotalsSet = "<h3 id=\"CICh\">Shipping: {0:s}<u id=\"CICHt\">{1:,.2f}</u></h3><hr id=\"CICTh\"><h3 id=\"CICt\">Total: {0:s}{2:,.2f}</h3>".format(UserCurrencySymbol,UserCartListShipping,UserCartListTotal)
            UserShippingAddress = "<p>0001 Street Name Rd Apt #1000</p><p>New York, NY 00000-0000</p><p>United States</p>"
            UserBillingAddress = "<p>0002 Street Name Rd Apt #1000</p><p>New York, NY 00000-0000</p><p>United States</p>"
            UserBillingInfoSet = "Card ending in 0000<br>$100.00 gift card balance"
            UserCartItems += "<div id=\"CIc\" style=\"top:{0:s}px;\"><h1 id=\"CICSt\">Shipping Address</h1><h2 id=\"CICs\">{1:s}</h2><h1 id=\"CICBt\">Billing Address</h1><h2 id=\"CICb\">{2:s}</h2><h1 id=\"CICPt\">Payment Method</h1><h2 id=\"CICp\">{3:s}</h2><h6 id=\"CICRt\">Redeem a gift card:</h6><input type=\"text\" id=\"CICr\" placeholder=\"Enter code here\" maxlength=\"19\">{4:s}<button class=\"rgsb\" id=\"CICy\">PLACE ORDER</button></div>".format(str(UserCartListLen*210),UserShippingAddress,UserBillingAddress,UserBillingInfoSet,UserCartTotalsSet)
            CartIndex = CartIndex.replace("<% Cart %>",UserCartItems)
            CartIndex = CartIndex.replace("<% ShowEmptyCartMsg %>","none")
        else:
            CartIndex = CartIndex.replace("<% Cart %>","")
            CartIndex = CartIndex.replace("<% ShowEmptyCartMsg %>","block")
        if UserCartListLen > 0:
            CartIndex = CartIndex.replace("<% FootTop %>",str(510+(UserCartListLen*210)))
        else:
            CartIndex = CartIndex.replace("<% FootTop %>","700")
        self.write(CartIndex)
