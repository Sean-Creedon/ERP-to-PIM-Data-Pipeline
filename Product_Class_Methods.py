#!/usr/bin/env python3
import re
from Constants import *
from Product_Name_Functions import *

def testExtraProdMethod(self):
	print("Product Class method imported.")

def replaceSpecialCharactersInHandle(productName):
	"""Replaces special characters in product name with appropriate values."""
	productName = productName.lower()
	productName = productName.replace(" " , "-")
	productName = productName.replace("#" , "-")
	productName = productName.replace("@" , "-")
	productName = productName.replace("%" , "-")
	productName = productName.replace("/" , "-")
	productName = productName.replace("\\" , "-")
	productName = productName.replace("'" , "")
	productName = productName.replace("." , "")
	productName = productName.replace("!" , "")
	productName = productName.replace("\u2018" , "")
	productName = productName.replace("\u2019" , "")
	productName = productName.replace("\u201C" , "")
	productName = productName.replace("\u201D" , "")
	productName = productName.replace("\u00BD" , "Half")
	productName = productName.replace("\u00BC" , "Quarter")
	productName = productName.replace("\u00BE" , "Three-Quarter")
	productName = productName.replace("\u2122" , "")
	productName = productName.replace("wproductNameth " , "wproductNameth-") #No idea. Can hopefully remove.
	productName = productName.replace("�" , "")
	productName = productName.replace(" ," , "")
	productName = productName.replace("(" , "")
	productName = productName.replace(")" , "")
	productName = productName.replace("+" , "and")
	productName = productName.replace("&" , "and")
	productName = productName.replace("\"" , "")
	productName = productName.replace(";" , "")

	return productName

def generateHandle(self):
	"""Generate handle string from product name and SKU with pattern name-with-spaces-and-special-charachters-replaced-ABC99999-666"""
	#colorado-state-rams-ouray-20024-vintage-sheet-short-sleeve-t-shirt-CSUM000087
	handleName = replaceSpecialCharactersInHandle(self.ProductName)
	prodSKU = self.ProductSKU
	self.Handle = f"{handleName}-{prodSKU}"
	return self

def checkIfDropShip(self):
	"""Returns bool based on value of default warehouse (DefaultWarehouse): True if 'DS'."""
	self.isDropShip = True if self.DefaultWarehouse == "DS" else False
	return self

def setProductWeight(self):
	"""Checks product's ProductLineName (taken directly from SAP value), assigns a shipping weight if the name is in list/grouping of common weights.\
	Calls _keyword_name_func_TBD if not found, then calls func to determine weight using AI(??) if still not found."""
	if self.ProductLineName in LIST_OF_13OZ_ITEM_GROUPS:
		self.ProductWeight = 13.0
		print(f"{self.ProductName} matched to {LIST_OF_13OZ_ITEM_GROUPS}")
	elif self.ProductLineName in LIST_OF_16OZ_ITEM_GROUPS:
		self.ProductWeight = 16.0
		print(f"{self.ProductName} matched to {LIST_OF_16OZ_ITEM_GROUPS}")
	elif self.ProductLineName in LIST_OF_24OZ_ITEM_GROUPS:
		self.ProductWeight = 24.0
		print(f"{self.ProductName} matched to {LIST_OF_24OZ_ITEM_GROUPS}")
	elif self.ProductLineName in LIST_OF_32OZ_ITEM_GROUPS:
		self.ProductWeight = 32.0
		print(f"{self.ProductName} matched to {LIST_OF_32OZ_ITEM_GROUPS}")
	elif not bool(self.ProductWeight):#If still no shipping weight, call func to check the product name for keywords.
		self.ProductWeight = getWeightFromProductName(self)
	elif not bool(self.ProductWeight):#If still no shipping weight, call AI func to guess prod shipping weight:
		print(f"No shipping weight assigned for {self.ProductSKU}, {self.ProductName}, in product line {self.ProductLineName}. Product needs AI weight check.")#_keyword_name_func_AI
	print(f"{self.ProductName} in product line {self.ProductLineName}: {self.ProductWeight}\nAdd AI check if still None.")
	return self

#Set age, gender, and "is unisex" in one go:
def setAgeGroupGenderAndIfUnisex(self):
	""""""
	if self.ItemGroup not in APPAREL_ITEM_GROUP_NAMES:#i.e. not "Mens" , "Womens" , or "Youth".
		self.AgeGroup = "Adult"
		self.Gender = "Unisex"
		self.IsUnisex = True
	else:
		if self.ItemGroup == "Mens":
			self.AgeGroup = "Adult"
			self.Gender = "Men"
			self.IsUnisex = False
		elif self.ItemGroup == "Womens":
			self.AgeGroup = "Adult"
			self.Gender = "Women"
			self.IsUnisex = False
		else:
			self.Gender = "Unisex"
			self.IsUnisex = True
		if self.ItemGroup == "Youth":
			#Test if "kid" or "infant" and so on in prod name to determine if item is Youth/Infant/Kids/Toddler/Newborn:
			prodName = self.ProductName.lower()
			if any(word in prodName for word in OTHER_YOUTH_AGE_GROUPS):
				#Make a list of words in the name:
				listOfWordsInProductName = re.split("[\W\d]" , prodName)
				#print(listOfWordsInProductName)
				#Get a list of a words in the prod name that match list of "youth" group names. Take first matching item (in case of 2 or more matches) & convert to title case.
				youthAgeGroupInName = list(set(listOfWordsInProductName).intersection(OTHER_YOUTH_AGE_GROUPS))
				#print(youthAgeGroupInName)
				youthAgeGroupInName = youthAgeGroupInName[0].title() #If name is "Kids Infant Bball Tee" , just use "Kids".
				self.AgeGroup = youthAgeGroupInName
			else:
				self.AgeGroup = "Youth"
	return self

def setAvalaraTaxCode(self):
	"""Sets the Avalara Tax Code prod attr depending on whether an prod is apparel (code "PC040100") or not (code "P0000000")."""
	if bool(self.ItemGroup):
		self.AvaTaxCode = "PC040100" if self.ItemGroup in APPAREL_ITEM_GROUP_NAMES else "P0000000"
		print(f"{self.ProductSKU}: 4th char is {self.ProductSKU[3]}. The Item Group is {self.ItemGroup}.")
	else:
		#If Item Group Name is blank, check the 4th character of the prod SKU for "N" (novelties) to determine if apparel or not.
		#Note: As of 01/13/23, Private Label products' 4th prod SKU char would be a hyphen. If we somehow ever sell PL gift & access., there could be a tax code issue.
		self.AvaTaxCode = "PC040100" if self.ProductSKU[3] != "N" else "P0000000"
		print(f"{self.ProductSKU}: 4th char is {self.ProductSKU[3]}. The Item Group is {self.ItemGroup}.")
	return self

def assignProductCategoryNamesAndCodes(self, inputSAPObj):
	""""""
	groupName = inputSAPObj.GroupName
	productLineName = inputSAPObj.ProductLineName
	categoryNames = self.CategoryName
	categoryCodes = self.Category
	ageGroup = self.AgeGroup
	#Assign parent categories mostly (some sub cats too):
	if ( (groupName not in APPAREL_ITEM_GROUP_NAMES) and (groupName != "Footwear") and (groupName != "Headwear") ) and (productLineName not in JERSEYS_PRODUCT_LINE_NAMES):
		categoryNames.append("Gifts & Accessories")
		categoryCodes.append("GIFT01")
	elif (productLineName in JERSEYS_PRODUCT_LINE_NAMES):
		categoryNames.append("Jerseys")
		categoryCodes.append("JERS02")
		categoryNames.append("Adult") if ageGroup == "Adult" else categoryNames.append("Youth")
		categoryCodes.append("ADUL01") if ageGroup == "Adult" else categoryCodes.append("YTJS01")
	elif groupName == "Footwear":
		categoryNames.append("All Footwear")
		categoryCodes.append("ALLFTW")
		if self.Gender == "Men":
			categoryNames.append("Men")
			categoryCodes.append("MENS01")
		elif self.Gender == "Women":
			categoryNames.append("Women")
			categoryCodes.append("WOME01")
		elif self.Gender == "Unisex":
			categoryNames.extend(["Men", "Footwear", "Women", "Footwear"])
			categoryCodes.extend(["MENS01", "MFTW01", "WOME01", "WFTW01"])
		if (self.AgeGroup == "Youth") or (self.AgeGroup not in OTHER_YOUTH_AGE_GROUPS):
			categoryNames.extend(["Youth", "Footwear"])
			categoryCodes.extend(["YOUT01", "YOFT01"])
	elif groupName == "Headwear":
		categoryNames.append("Headwear")
		categoryCodes.append("HEAD01")
	elif groupName == "Mens":
		categoryNames.append("Men")
		categoryCodes.append("MENS01")
	elif groupName == "Womens":
		categoryNames.append("Women")
		categoryCodes.append("WOME01")
	elif (ageGroup == "Youth") or (ageGroup not in OTHER_YOUTH_AGE_GROUPS):
		categoryNames.append("Youth")
		categoryCodes.append("YOUT01")
	warehouse = inputSAPObj.DefaultWarehouse
	if (self.isDropShip == True):
		categoryNames.append("Dropship & Non-Discount")
		categoryCodes.append("DSND21")
	return self