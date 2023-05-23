#!/usr/bin/env python3
from Constants import *
from File_Read_and_Write_Functions import *

class productClass(object):
	"""Attributes and methods for converting product data from SAP for Sales Layer (Dyehard Fan Supply Ecommerce)"""
	def __init__(self, ProductSKU, Family, ProductName, CategoryName, Category, ProductDescription, ProdTags, Price, OldDescription, UseOldDescription, ProductImages, BrandName, ProductBrandID, AgeGroup, Gender, IsUnisex, IsLicensed, Season, Sport, Memorabilia, Activity, Fit, MaterialType, MaterialContent, TemperatureRating, CareInstructions, Features, PlayerName, EventCollection, League, SportsTeam, CountryofOrigin, DefaultWarehouse, LeadTime, FixedShippingCost, FreeShipping, ProductWeight, TaxLiable, AvaTaxCode, ProductTaxClass, ModelGroup, PreviouseCommNumber, ProductLineCode, InventoryItem, ProductionDate, PurchaseItem, SalesItem, PreferredVendor, ForeignName, ItemGroup, ItemType, Division, AllowPurchases, TrackInventory, Handle, Keywords, WMTTags, Filters, CreatedDate, COGS, DiscountsAndPromotionsApplicable, isDropShip, isPrivateLabel, colorList, isMultiColor, sizeList, colorDescriptionList, ProductLineName):
		#Attr from Sales Layer product import sheets:
		self.ProductSKU = ProductSKU
		self.Family = Family
		self.ProductName = ProductName
		#DO NOT IMPORT any product's CategoryName attribute to PIM. Values are used to review category assignments. Import expects the category codes:
		self.CategoryName = CategoryName
		self.Category = Category
		self.ProductDescription = ProductDescription
		self.ProdTags = ProdTags
		self.Price = Price
		self.OldDescription = OldDescription #Can this be retired? Temp for transition from RP to SAP?
		self.UseOldDescription = UseOldDescription #Can this be retired? Temp for transition from RP to SAP?
		self.ProductImages = ProductImages
		self.BrandName = BrandName
		self.ProductBrandID = ProductBrandID
		self.AgeGroup = AgeGroup
		self.Gender = Gender
		self.IsUnisex = IsUnisex
		self.IsLicensed = IsLicensed
		self.Season = Season
		self.Sport = Sport
		self.Memorabilia = Memorabilia
		self.Activity = Activity
		self.Fit = Fit
		self.MaterialType = MaterialType
		self.MaterialContent = MaterialContent
		self.TemperatureRating = TemperatureRating
		self.CareInstructions = CareInstructions
		self.Features = Features
		self.PlayerName = PlayerName
		self.EventCollection = EventCollection
		self.League = League
		self.SportsTeam = SportsTeam
		self.CountryofOrigin = CountryofOrigin
		self.DefaultWarehouse = DefaultWarehouse
		self.LeadTime = LeadTime
		self.FixedShippingCost = FixedShippingCost
		self.FreeShipping = FreeShipping
		self.ProductWeight = ProductWeight #Currently in ounces. Minimum should be 13.0 (12/12/22)
		self.TaxLiable = TaxLiable
		self.AvaTaxCode = AvaTaxCode
		self.ProductTaxClass = ProductTaxClass
		self.ModelGroup = ModelGroup #This is a repeat of property tag (the 3 letter code; not marketing-type tags)
		self.PreviouseCommNumber = PreviouseCommNumber
		self.ProductLineCode = ProductLineCode
		self.InventoryItem = InventoryItem
		self.ProductionDate = ProductionDate #This is a repeat of CreateDate
		self.PurchaseItem = PurchaseItem
		self.SalesItem = SalesItem
		self.PreferredVendor = PreferredVendor
		self.ForeignName = ForeignName
		self.ItemGroup = ItemGroup
		self.ItemType = ItemType
		self.Division = Division
		self.AllowPurchases = AllowPurchases
		self.TrackInventory = TrackInventory
		self.Handle = Handle
		self.Keywords = Keywords
		self.WMTTags = WMTTags #WMT only
		self.Filters = Filters #WMT only?
		self.CreatedDate = CreatedDate
		self.COGS = COGS
		self.DiscountsAndPromotionsApplicable = DiscountsAndPromotionsApplicable
		#Attr not on SL import sheets; created for script's internal workings:
		self.isDropShip = isDropShip
		self.isPrivateLabel = isPrivateLabel
		self.colorList = colorList #List of product color codes.
		self.isMultiColor = isMultiColor #bool(self.colorList) #Determine if product has more than one color from length/bool from color list.
		self.sizeList = sizeList #List of sizes. Add dict of Variant_Class objects attribute?
		self.colorDescriptionList = colorDescriptionList #Added 11/30/22
		self.ProductLineName = ProductLineName #Added 11/30/22
		self.preAIcategoryName = CategoryName #Added 02/03/23: Will be used to store original category assignments to be compared to AI category assignments if needed.

	#Product_Class methods:
	def calcRetailPrice(self): #Could make this a SAP_Data_Class method.
		"""Rounds up price to whole number and subtracts 0.05 (change $10 to $9.95)."""
		retailPrice = self.Price.replace("$","").replace(",","")
		if (retailPrice == 0) or (retailPrice == "0") or (retailPrice == 0.00) or (retailPrice == "0.00") or (retailPrice == "") or (retailPrice.isalpha()) or (retailPrice == None):
			retailPrice = None
			#Add alert/flag of some sort.
			self.ProductName = "(CHECK PRICE)-" + self.ProductName
			#Add func to send email/other kind of alert?
			writeLog(f"{self.ProductSKU}\t{self.ProductName}\n", logType="missing-price")
		else:
			retailPrice = str(round(float(retailPrice)) - 0.05)
		self.Price = retailPrice
		return self

	def checkIfMultiColor(self):
		"""Returns bool based on length of color list"""
		self.isMultiColor = len(self.colorList) > 1
		return self.isMultiColor

	from Product_Class_Methods import testExtraProdMethod, generateHandle, checkIfDropShip, setProductWeight, setAgeGroupGenderAndIfUnisex, setAvalaraTaxCode, assignProductCategoryNamesAndCodes

	def __str__(self):
		"""Prints Product Class obj's attributes"""
		return f"PRODUCT SKU: {self.ProductSKU}, FAMILY: {self.Family}, PRODUCT NAME: {self.ProductName}, CATEGORY CODE(S):{self.Category}, CATEGORY NAME(S): {self.CategoryName}, PRODUCT DESCRIPTION: {self.ProductDescription}, TAG(S): {self.ProdTags}, PRICE: {self.Price}, OLD DESCRIPTION: {self.OldDescription}, USE OLD DESCRIPTION: {self.UseOldDescription}, IMAGE(S): {self.ProductImages}, BRAND CODE/NAME: {self.ProductBrandID}/{self.BrandName}, AGE GROUP: {self.AgeGroup}, GENDER: {self.Gender}, IS UNISEX?: {self.IsUnisex}, IS LICENSED: {self.IsLicensed}, SEASON: {self.Season}, SPORT(S): {self.Sport}, MEMORABILIA: {self.Memorabilia}, ACTIVITY: {self.Activity}, FIT: {self.Fit}, MATERIAL TYPE/CONTENT: {self.MaterialType}/{self.MaterialContent}, TEMPERATURE RATING: {self.TemperatureRating}, CARE INSTRUCTIONS: {self.CareInstructions}, FEATURES: {self.Features}, PLAYER NAME: {self.PlayerName}, EVENT/COLLECTION: {self.EventCollection}, LEAGUE: {self.League}, SPORTS TEAM: {self.SportsTeam}, COUNTRY of ORIGIN: {self.CountryofOrigin}, WAREHOUSE: {self.DefaultWarehouse}, LEAD TIME: {self.LeadTime}, FIXED SHIPPING COST: {self.FixedShippingCost}, FREE SHIPPING: {self.FreeShipping}, PRODUCT WEIGHT: {self.ProductWeight}, TAX LIABLE: {self.TaxLiable}, AVATAX CODE: {self.AvaTaxCode}, PRODUCT TAX CLASS: {self.ProductTaxClass}, MODEL GROUP: {self.ModelGroup}, PREVIOUS ECOMM NUMBER: {self.PreviouseCommNumber}, PRODUCT LINE/NAME: {self.ProductLineCode}/{self.ProductLineName}, INVENTORY ITEM: {self.InventoryItem}, PRODUCTION DATE: {self.ProductionDate}, PURCHASE ITEM: {self.PurchaseItem}, SALES ITEM: {self.SalesItem}, PREFERRED VENDOR: {self.PreferredVendor}, FOREIGN NAME: {self.ForeignName}, ITEM GROUP: {self.ItemGroup}, ITEM TYPE: {self.ItemType}, DIVISION: {self.Division}, ALLOW PURCHASES: {self.AllowPurchases}, TRACK INVENTORY: {self.TrackInventory}, HANDLE: {self.Handle}, KEYWORDS: {self.Keywords}, WMT TAG(S): {self.WMTTags}, FILTER(S): {self.Filters}, CREATED DATE: {self.CreatedDate}, COGS: {self.COGS}, DISCOUNTS & PROMOTIONS APPLICABLE: {self.DiscountsAndPromotionsApplicable}, COLOR CODE(S): {self.colorList}, COLOR NAME(S): {self.colorDescriptionList}, MULTICOLOR?: {self.isMultiColor}, SIZE(S): {self.sizeList}, DROPSHIP?: {self.isDropShip}, PRIVATE LABEL?: {self.isPrivateLabel}, Pre-AI-CategoryName: {self.preAIcategoryName}"

#############
if __name__ == "__main__":
	origPrice = "50.01"
	testProduct = productClass("ARKM100282", "Mens>Outerwear", "Arkansas Razorbacks Take Your Time 1/4 Zip Windshirt", "Men|Outerwear|Pullovers|All Outerwear,PRODUCT|All Product|New Arrivals|All Outerwear", "MENS01,MENS03,MEOU01,OUTER,PRODUCT,ALL,NEWA01,OUTER", "", "ARK", origPrice, "", "0", "ARKM100282.jpg", "Colosseum", "26", "Adult", "Men", "No", "True", "SP23", "Wiffle Ball", "False", "", "", "", "", "", "", "", "", "NationalWiffleBallPlayOffs", "", "", "Imported", "WSD", "", "", "0", "16.0", "Default Tax Class", "PC040100", "Default Tax Class", "", "", "2", "", "", "", "", "V500027", "COUZ11523W", "Mens", "LONG SLEEVE", "MENS", "", "Variant", "arkansas-razorbacks-take-your-time-1-4-zip-windshirt-ARKM100282", "Fleece, pullover, sweats, hoodie, windshirt, sweatshirt, wind shirt, sweat shirt, pull over, 1/4 zip, quarter zip, Shep Shirt, Shepshirt, Colosseum", ",New,White,Men,Adult", "Age>Adult;Gender>Men;Color>White;Origin>Imported", "07/15/22", "20.70", "Yes", True, True, ["999"], True, ["XS", "S", "M", "L", "XL", "2XL"], ["Multi"], "TestProductLineName")
	print(testProduct)
	print(testProduct.calcRetailPrice())
	print(testProduct.isMultiColor)
	testProduct.checkIfMultiColor()
	print(testProduct.isMultiColor)
	testProduct.testExtraProdMethod()
	print(testProduct.isDropShip)
	testProduct.checkIfDropShip()
	print(testProduct.isDropShip)
