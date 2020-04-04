from udf import *

class handler(tornado.web.RequestHandler):
    def get(self):
        CartIndex = ServePage(self,"/cart/index.html")
        UserCartList = GetCart(self)
        UserCartItems = ""
        UserCartFootTop = 110
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
            UserCartItems += "<div class=\"CIt\" id=\"CIt_"+UserCartItem_ID+"\" style=\"top:"+str(i*210)+"px;\"><input class=\"CIq\" type=\"number\" value=\""+str(UserCartList[i][1])+"\" onblur=\"AdjOa()\"><a href=\"/product/"+UserCartItem_ID+"/\" class=\"CIi\" style=\"background-image:url("+UserCartItem_ImgLink+");\"></a><h3>"+FindProduct(UserCartItem_ID)["Name"]+"</h3><h1>"+UserCartItem_PriceSet+"</h1><button class=\"CIr\" onclick=\"RMp('"+UserCartItem_ID+"')\">Remove</button></div>\n"
            UserCartFootTop += 210
        if UserCartItems != "":
            CartIndex = CartIndex.replace("<% Cart %>",UserCartItems)
            CartIndex = CartIndex.replace("<% ShowEmptyCartMsg %>","none")
        else:
            CartIndex = CartIndex.replace("<% Cart %>","")
            CartIndex = CartIndex.replace("<% ShowEmptyCartMsg %>","block")
        if UserCartFootTop >= 700:
            CartIndex = CartIndex.replace("<% FootTop %>",str(UserCartFootTop))
        else:
            CartIndex = CartIndex.replace("<% FootTop %>","700")
        self.write(CartIndex)
