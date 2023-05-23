#!/usr/bin/env python3

from Constants import *

def testExtraSAPMethod(self):
	print("SAP Data Class method imported.")


#02/06/23 Move this to Product_Class_Methods.py at some point. Probably don't have to change much if anything.
def assignProductFamily(self):
	""""""
	family = None
	prodName = self.ItemDescription.lower()
	groupName = self.GroupName
	productLineName = self.ProductLineName
	if groupName in NOVELTY_ITEM_GROUP_NAMES:
		family = "Novelty"
		return family
	elif (groupName == "Footwear") or (groupName == "Headwear"):
		family = groupName
		return family
	elif groupName in APPAREL_ITEM_GROUP_NAMES:
		family = groupName
	elif not bool(family):
		#If there's still no name, create/check more group name lists (youth hat, socks)
		if productLineName in FOOTWEAR_PRODUCT_LINE_NAMES:
			family = "Footwear"
			return family
		elif productLineName in HEADWEAR_PRODUCT_LINE_NAMES:
			family = "Headwear"
			return family
		elif productLineName in MENS_PRODUCT_LINE_NAMES:
			family = "Mens"
		elif productLineName in WOMENS_PRODUCT_LINE_NAMES:
			family = "Womens"
		elif productLineName in YOUTH_PRODUCT_LINE_NAMES:
			family = "Youth"
		elif productLineName in NOVELTY_PRODUCT_LINE_NAMES:
			family = "Novelty"
			return family
	#Add 2nd level family assignments ("Tops" to "Mens>Tops")
	if productLineName in BOTTOMS_PRODUCT_LINE_NAMES:
		family = f"{family}>Bottoms"
		return family
	elif (productLineName in FLEECE_PRODUCT_LINE_NAMES) or ("fleece" in prodName):
		family = f"{family}>Fleece"
		return family
	elif productLineName in JERSEYS_PRODUCT_LINE_NAMES:
		family = f"{family}>Jerseys"
		return family
	elif productLineName in OUTERWEAR_PRODUCT_LINE_NAMES:
		family = f"{family}>Outerwear"
		return family
	#No Polo product lines nor group names as of 01/09/22.
	#elif (productLineName in POLO_PRODUCT_LINE_NAMES) and ("polo" in self.ItemDescription.lower()):
		#return f"{family}>Polo"
	elif (productLineName == "SHORT SLEEVE") and ("polo" in prodName or "ginham" in prodName or "oxford" in prodName or "button down" in prodName or "buttondown" in prodName or "button up" in prodName or "buttonup" in prodName):
		return f"{family}>Polo"
	elif (productLineName in TOPS_PRODUCT_LINE_NAMES) and ("fleece" not in prodName):
		#2nd level family name is "Tops" for Mens and Womens, "Tees" for Youth
		return f"{family}>Tops" if family != "Youth" else f"{family}>Tees"
	#If both Group Name & Product Line Code fields are blank, assign family during categorization when checking keywords in name?
	return family#Will this line ever get triggered/reached?
