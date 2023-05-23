#!/usr/bin/env python3
from Product_Class import *
from Constants import *

def testExtraVarMethod(self):
	print("Variant Class method imported.")

#Disable? Change all "blank" values to None?
def addBlankValues(self):
	"""Replaces Var Class obj attribute strings that start with "Blank_" with a blank string ("")."""
	#This allows other functions/methods to clearly label which values default to blank while outputting actual blanks/"".
	#This func is intended to make it easier to make blank attributes dynamic values in the future.
	#It's easier to assign all attributes in same order as existing import/export sheets at start rather than redefine original defaults in __init__ later.
	for attribute in dir(self):#Loop through list of variant obj attributes
		attributeType = type(getattr(self, str(attribute)))#Get attributes data type with getattr() with attribute var converted to string
		attributeValue = str(getattr(self, str(attribute)))#Get attributes value with geattr()/string value of var.
		if (attributeType == str) and (attributeValue.startswith("Blank_")):#Test if  attribute's value is a string starting with "Blank_"
			#print(f"Match found {attributeValue}")
			setattr(self, attribute, "")#Reset the attribute value from "Blank_" to "".
	return self

def addDefaultSLVariantValues(self):
	"""Adds known default values as needed for SL variants."""
	#Probably not needed. Can be used if different products need different defaults but don't warrant full variant class extention
	#For example: Low stock level in WH products gets changed to 5 while POD products can go as low as 1.
	print(f"Likely unneeded addDefaultSLVariantValues({self}) function called.")
	self.Condition = "Visible"
	self.LowStockLevel = "1"
	return self