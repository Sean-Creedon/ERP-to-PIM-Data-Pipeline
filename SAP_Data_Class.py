#!/usr/bin/env python3

from math import ceil
from Constants import *

class SAPData(object):
	"""Attributes and methods for variant data exported from SAP (Dyehard Fan Supply Ecommerce)"""
	def __init__(self, ItemNo, ItemDescription, ForeignName, ItemGroup, GroupName, DefaultWarehouse, Color, ColorDescription, Size, Season, ModelGroup, ProductLineCode, ProductLineName, PrevItemNumber, PreveCommNumber, ProductCollection, ProductSubCollection, CountryofOrigin, PreferredVendor, ProductionDate, CreatnTimeInclSecs, BarCode, VendorUPC, eCommListingSKU, Model, MainSellingPrice, MainBuyingPrice, DateofUpdate, ProductBrand, BrandName):
		#super(SAPData, self).__init__()
		self.ItemNo = ItemNo
		self.ItemDescription = ItemDescription
		self.ForeignName = ForeignName
		self.ItemGroup = ItemGroup
		self.GroupName = GroupName
		self.DefaultWarehouse = DefaultWarehouse
		self.Color = Color #Color Code
		self.ColorDescription = ColorDescription #Color Description. Added 11/11/22
		self.Size = Size
		self.Season = Season
		self.ModelGroup = ModelGroup
		self.ProductLineCode = ProductLineCode
		#Note that SAP exports this and another value as "Name." Need headers renamed in export.
		self.ProductLineName = ProductLineName #Name of Product Line Code (product line #1 = SHORT SLEEVE). Added 11/11/22
		self.PrevItemNumber = PrevItemNumber
		self.PreveCommNumber = PreveCommNumber
		self.ProductCollection = ProductCollection
		self.ProductSubCollection = ProductSubCollection
		self.CountryofOrigin = CountryofOrigin
		self.PreferredVendor = PreferredVendor
		self.ProductionDate = ProductionDate
		self.CreatnTimeInclSecs = CreatnTimeInclSecs
		self.BarCode = BarCode
		self.VendorUPC = VendorUPC
		self.eCommListingSKU = eCommListingSKU
		self.Model = Model
		self.MainSellingPrice = MainSellingPrice
		self.MainBuyingPrice = MainBuyingPrice
		self.DateofUpdate = DateofUpdate
		self.ProductBrand = ProductBrand #Code for Product Brand.
		#Note that SAP exports this and another value as "Name." Need headers renamed in export.
		self.BrandName = BrandName #Name of Product Brand Code (product brand code #3 = Under Armour). Added 11/11/22

	from SAP_Data_Class_Methods import testExtraSAPMethod, assignProductFamily

	def __str__(self):
		"""Prints SAP Data Class obj's Variant SKU, Product SKU Reference, Property Tag, Size, Color, Sport, Images, and Image Required attributes"""
		return f"SAP Variant SKU: {self.ItemNo}, NAME: {self.ItemDescription}, PRODUCT SKU: {self.Model}, COLOR: {self.Color}, SIZE: {self.Size}"

#Begin SAP functions:

#Changes whole dollar amounts to ".95" prices
def adjustPrice(price):
	"""Rounds up price to whole number and subtracts 0.05."""
	price = price.replace("$","").replace(",","")
	if (price == 0) or (price == "0") or (price == 0.00) or (price == "0.00") or (price == ""):
		return "0"
	elif price.isalpha():
		return price
	else:
		price = str(ceil(float(price)) - 0.05)
		return price

def readSAPDataCSV(inputData):
	"""Takes inputData CSV DictReader object, loop through data and assign values to dictionary of data as SAPData objects"""
	SAPDataDict = {}
	#print(inputData, type(inputData), sep="\n")
	for num, row in enumerate(inputData):
		productItemNo = row["Item No."]
		productGroupName = row["Group Name"]
		#Test if SAP item's SKU is in the list of raw material/generic goods, and so on.
		if productGroupName == "Items":
			continue
		if any(productItemNo.startswith(prefix) for prefix in  PRODUCTS_TO_IGNORE):
			if INCLUDE_GENERIC_ITEMS and productItemNo.startswith("GEN"):
				pass#Include generic SKUs if needed
			else:#Otherwise exclude this SAP item from processing.
				continue
		#print(row, type(row), sep="\n")
		SAPDataDict[productItemNo] = SAPData(productItemNo, row["Item Description"], row["Foreign Name"], row["Item Group"], productGroupName, row["Default Warehouse"], row["Color"], row["Color Description"], row["Size"], row["Season"], row["Model Group"], row["Product Line Code"], row["Product Line Name"], row["Prev Item Number"], row["Prev eComm Number"], row["Product Collection"], row["Product Sub Collection"], row["Country of Origin"], row["Preferred Vendor"], row["Production Date"], row["Creatn Time - Incl. Secs"], row["Bar Code"], row["Vendor UPC"], row["eComm Listing SKU"], row["Model"], adjustPrice(row["Main Selling Price"]), row["Main Buying Price"], row["Date of Update"], row["Product Brand"], row["Brand Name"])
		#print(SAPDataDict[row["Item No."]].ItemNo,SAPDataDict[row["Item No."]].ItemDescription, sep="\t")

	return SAPDataDict

#############
if __name__ == "__main__":
    #No test currently.
	pass