from udf import *

class handler(tornado.web.RequestHandler):
    def get(self):
        # Open
        ProductIndex = ServePage(self,"/product/index.html",False)
        NotFoundIndex = ServePage(self,"/status/404.html",False)
        
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
            if str(FindProduct(ProductRequested_ID)["Wash"])=="0":
                ProductRequested_Care = "<p>Unknown</p>"
            else:
                ProductRequested_Care = "<ul><li>"+WashCareCodesList[FindProduct(ProductRequested_ID)["Wash"]]+"</li><li>"+BleachCareCodesList[FindProduct(ProductRequested_ID)["Bleach"]]+"</li><li>"+DryCareCodesList[FindProduct(ProductRequested_ID)["Dry"]]+"</li>"+ProductRequested_CareWring+"<li>"+DryCleanCareCodesList[FindProduct(ProductRequested_ID)["DryClean"]]+"</li></ul>"
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
            if str(ProductRequested_ID)[0:7] != "1111111":
                if CheckLogin(self):
                    ProductRequested_CartButton = "<input type=\"number\" id=\"BIOq\" value=\"1\" onblur=\"AdjOq()\"><button id=\"BIOb\" onclick=\"ACt()\">Add To Cart</button>"
                else:
                    ProductRequested_CartButton = "<input type=\"number\" id=\"BIOq\" value=\"1\" onblur=\"AdjOq()\"><a href=\"/sign_in/\"><button id=\"BIOb\">Sign In To Purchase</button></a>"
            else:
                ProductRequested_CartButton = ""
            ProductRequested_Rating = 0
            ProductRequested_ReviewCount = 0
        
            ProductIndex = ProductIndex.replace("<% ProductID %>",ProductRequested_ID)
            ProductIndex = ProductIndex.replace("<% CartButton %>",ProductRequested_CartButton)
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
