#!/usr/bin/env python3

import math
from Constants import *

class variantClass(object):
	"""Attributes and methods for converting variant data from SAP for Sales Layer (Dyehard Fan Supply Ecommerce)"""
	#Original __init__ parameters below (includes default values). To be used if default values are assigned dynamically (low stock level changes to vary by WH or vendor, for example).
	#(self, VariantSKU, ProductSKUReference, Condition, VarTags, VariantSize, VariantPrice, VariantImage, VendorVariantColor, VariantColor, VariantSport, VariantSortOrder, ProductLength, GTIN, MPN, UPC, LowStockLevel, VariantHeight, VariantWidth, VariantDepth, VariantWeight, ERPBarcode, VariantColorWMT, ColorName, ImageRequired, VendorUPC, ListingSKU)
	Condition = "Visible"
	LowStockLevel = "1"
	def __init__(self, VariantSKU, ProductSKUReference, Condition, VarTags, VariantSize, VariantPrice, VariantImage, VendorVariantColor, VariantColor, VariantSport, VariantSortOrder, ProductLength, GTIN, MPN, UPC, LowStockLevel, VariantHeight, VariantWidth, VariantDepth, VariantWeight, ERPBarcode, VariantColorWMT, ColorName, ImageRequired, VendorUPC, ListingSKU, Cost, COGs):
		#super(variantClass, self).__init__()
		#Attr from Sales Layer product import sheets:
		self.VariantSKU = VariantSKU
		self.ProductSKUReference = ProductSKUReference
		self.Condition = Condition
		self.VarTags = VarTags
		self.VariantSize = VariantSize
		self.VariantPrice = VariantPrice
		self.VariantImage = VariantImage #WMT only?
		self.VendorVariantColor = VendorVariantColor
		self.VariantColor = VariantColor
		self.VariantSport = VariantSport
		self.VariantSortOrder = VariantSortOrder #WMT only?
		self.ProductLength = ProductLength
		self.GTIN = GTIN
		self.MPN = MPN
		self.UPC = UPC #This is a repeat of VendorUPC and value is blank during uploads as of 12/07/22.
		self.LowStockLevel = LowStockLevel
		self.VariantHeight = VariantHeight
		self.VariantWidth = VariantWidth
		self.VariantDepth = VariantDepth
		self.VariantWeight = VariantWeight #Need Variant Weight from ProductWeight (not currently uploaded to SL).
		self.ERPBarcode = ERPBarcode
		self.VariantColorWMT = VariantColorWMT
		self.ColorName = ColorName
		self.ImageRequired = ImageRequired #WMT only?
		self.VendorUPC = VendorUPC #This is a repeat of UPC and is uploaded to SAP.
		self.ListingSKU = ListingSKU #Currently variant SKU. Is this a repeat of the variant SKU or product SKU reference?
		self.Cost = Cost#
		self.COGs = COGs

	from Variant_Class_Methods import testExtraVarMethod, addBlankValues, addDefaultSLVariantValues, isImageRequired

	def calcVariantRetailPrice(self): #Could make this a SAP_Data_Class method.
		"""Rounds up price to whole number and subtracts 0.05 (change $10 to $9.95)."""
		retailPrice = self.VariantPrice.replace("$","").replace(",","")
		if (retailPrice == 0) or (retailPrice == "0") or (retailPrice == 0.00) or (retailPrice == "0.00") or (retailPrice == "") or (retailPrice.isalpha()) or (retailPrice == None):
			retailPrice = None
		else:
			retailPrice = str(round(float(retailPrice)) - 0.05)
		self.VariantPrice = retailPrice
		return self

	def __str__(self):
		"""Prints Variant Class obj's Variant SKU, Product SKU Reference, Property Tag, Size, Color, Sport, Images, and Image Required attributes"""
		return f"VARIANT SKU: {self.VariantSKU}, PRODUCT SKU REFERENCE: {self.ProductSKUReference}, CONDITION: {self.Condition}, VAR TAGS: {self.VarTags}, VARIANT SIZE: {self.VariantSize}, VARIANT PRICE: {self.VariantPrice}, VARIANT IMAGE: {self.VariantImage}, VENDOR VARIANT COLOR: {self.VendorVariantColor}, VARIANT COLOR: {self.VariantColor}, VARIANT SPORT: {self.VariantSport}, VARIANT SORT ORDER: {self.VariantSortOrder}, PRODUCT LENGTH: {self.ProductLength}, GTIN: {self.GTIN}, MPN: {self.MPN}, UPC: {self.UPC}, LOW STOCK LEVEL: {self.LowStockLevel}, VARIANT HEIGHT: {self.VariantHeight}, VARIANT WIDTH: {self.VariantWidth}, VARIANT DEPTH: {self.VariantDepth}, VARIANT WEIGHT: {self.VariantWeight}, ERP BAR CODE: {self.ERPBarcode}, VARIANT COLOR WMT: {self.VariantColorWMT}, COLOR NAME: {self.ColorName}, IMAGE REQUIRED: {self.ImageRequired}, VENDOR UPC: {self.VendorUPC}, LISTING SKU: {self.ListingSKU}"

#############
if __name__ == "__main__":
	testVariant = variantClass("ARKM010968-698-S", "ARKM010968", "Visible", "ARK", "S", "", "", "", "698", "", "", "", "ARK-T5-10712", "", "", "1", "", "", "", "", "092275313480", "698", "Red", "False", "", "", "", "")
	print(testVariant)
	print(testVariant.VariantSKU)
	#print(testVariant)
	testVariant.testExtraVarMethod()
