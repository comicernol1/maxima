from udf import *

class handler(tornado.web.RequestHandler):
    def get(self):
        CartIndex = ServePage(self,"/cart/index.html",False)
        UserCartList = GetCart(self)
        UserCartListTotal = 0
        UserCartItems = ""
        UserCartListLen = len(UserCartList)
        for i in range(0,UserCartListLen):
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
            if str(UserCartItem_ID)[0:7] != "1111111":
                UserCartItem_TemplateSet = "<h6 class=\"CIPt\">Size:</h6><select class=\"CIp\"><option>Master Crafted&trade;</option><option>X-Small</option><option>Small</option><option>Medium</option><option>Large</option><option>X-Large</option></select><span class=\"DDoB_B\"></span>"
            else:
                UserCartItem_TemplateSet = ""
            if str(UserCartItem_ID)[0:7] == "1111111":
                UserCartAdjustNumDisable = " disabled"
                UserCartRemoveButton = ""
            else:
                UserCartAdjustNumDisable = ""
                UserCartRemoveButton = "<button class=\"CIr\" onclick=\"RMp('"+UserCartItem_ID+"')\">Remove</button>"
            UserCartListTotal += (UserCartItem_Price*int(UserCartList[i][1]))
            UserCartItems += "<div class=\"CIt\" id=\"CIt_"+UserCartItem_ID+"\" style=\"top:"+str(i*210)+"px;\"><input class=\"CIq\" type=\"number\" value=\""+str(UserCartList[i][1])+"\" onblur=\"AdjOa()\""+UserCartAdjustNumDisable+"><a href=\"/product/"+UserCartItem_ID+"/\" class=\"CIi\" style=\"background-image:url("+UserCartItem_ImgLink+");\"></a>"+UserCartItem_TemplateSet+"<h3>"+FindProduct(UserCartItem_ID)["Name"]+"</h3><h1>"+UserCartItem_PriceSet+"</h1>"+UserCartRemoveButton+"</div>\n"
        if UserCartItems != "":
            if UserCurrencySymbol in SpecifyCurrencyList:
                UserCartTotalsSet = "<h3 id=\"CICt\">Total: {0:s}{1:,.2f} ({2:s})</h3>".format(UserCurrencySymbol,UserCartListTotal,UserCurrency)
            else:
                UserCartTotalsSet = "<h3 id=\"CICt\">Total: {0:s}{1:,.2f}</h3>".format(UserCurrencySymbol,UserCartListTotal)
            UserShippingAddress = "<p>0001 Street Name Rd Apt #1000</p><br><p>New York, NY 00000-0000</p><br><p>United States</p>"
            UserBillingAddress = "0002 Street Name Rd Apt #1000<br>New York, NY 00000-0000<br>United States"
            UserBillingInfoSet = "Card ending in 0000<br>$100.00 gift card balance"
            UserCartItems += "<div id=\"CIc\" style=\"top:{0:s}px;\"><h1 id=\"CICSt\">Shipping Address</h1><h2 id=\"CICs\">{1:s}</h2><h1 id=\"CICBt\">Billing Address</h1><h2 id=\"CICb\">{2:s}</h2><h1 id=\"CICPt\">Payment Method</h1><h2 id=\"CICp\">{3:s}</h2><h6 id=\"CICRt\">Redeem a gift card:</h6><input type=\"text\" id=\"CICr\" placeholder=\"Enter code here\" maxlength=\"20\">{4:s}<button class=\"rgsb\" id=\"CICy\">PLACE ORDER</button></div>".format(str(UserCartListLen*210),UserShippingAddress,UserBillingAddress,UserBillingInfoSet,UserCartTotalsSet)
            CartIndex = CartIndex.replace("<% Cart %>",UserCartItems)
            CartIndex = CartIndex.replace("<% ShowEmptyCartMsg %>","none")
        else:
            CartIndex = CartIndex.replace("<% Cart %>","")
            CartIndex = CartIndex.replace("<% ShowEmptyCartMsg %>","block")
        if UserCartListLen >= 3:
            CartIndex = CartIndex.replace("<% FootTop %>",str(510+(UserCartListLen*210)))
        else:
            CartIndex = CartIndex.replace("<% FootTop %>","700")
        self.write(CartIndex)
