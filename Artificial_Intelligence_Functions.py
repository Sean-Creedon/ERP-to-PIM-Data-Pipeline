#!/usr/bin/env python3
#This is the main file for running the SAP_to_Sales_Layer_Data_Converter scripts/module/package/whatever this ends up being . . .
import openai
import os
from Constants import *
from SAP_Data_Class import *
from Product_Class import *
from Variant_Class import *
from File_Read_and_Write_Functions import *
from Product_Name_Functions import *
from Convert_SAP_Input_Functions import *
from Image_Matching_Functions import *
from Product_And_Variant_Functions import *
from Sales_Layer_API_Functions import *
from Category_Names_Codes_and_Parent_References import *

#Set OpenAI API key:
try:
	openai.api_key = os.getenv("OPENAI_API_KEY")
	#print(f"Is key still set?: {openai.api_key}")
except Exception as setAPIError:
	setAPIErrorText = f"Error setting API key:\n{setAPIError}"
	print(setAPIErrorText)
	logging.error("setAPIErrorText\n\n", exc_info=True)

#FUNC TO SEND/RETRIEVE CONTENT FROM OPENAI API HERE:
def sendProductDescriptionInstructionToOpenAI(input_prompt):
	""""""
	# create a completion
	try:
		completion = openai.Completion.create(engine=DYEHARD_ECOMM_PRODUCT_DESCRIPTION_AI, prompt=input_prompt, temperature=0.5, stop="#", max_tokens=200, frequency_penalty=0.9, presence_penalty=0.8)
		generatedProductDescription = completion.choices[0].text
		#Print the completion
		print(completion)
		print(f"Product Description from AI:\n{generatedProductDescription}")
	except Exception as generatedProductDescriptionError:
		generatedProductDescriptionErrorLogText = f"Error generating product description with OpenAI API :\n{generatedProductDescriptionError}"
		print(generatedProductDescriptionErrorLogText)
		writeLog(generatedProductDescriptionErrorLogText, logType="error")
	return generatedProductDescription

def generateProductDescriptionWithAI(saleLayerProductObj):
	""""""
	prodSKU = saleLayerProductObj.ProductSKU
	prodName = saleLayerProductObj.ProductName
	print(f"Generating AI product description for {prodSKU}:\t{prodName}")
	ageGroup = "youth" if (saleLayerProductObj.AgeGroup.lower() == "youth") else ""
	prodFamily = saleLayerProductObj.Family
	prodFamily = prodFamily.lower().replace(">", " ").replace("mens", "men's").replace("womens", "women's")
	prodFamily = prodFamily.replace("jerseys", "replica jersey").replace("tops", "top-wear").replace("tees", "top-wear").replace("bottoms", "bottom-wear")#.replace("", "")
	prodFamily = prodFamily.replace("novelty", "gifts/accessories")#.replace("", "")
	prodSupplier = saleLayerProductObj.BrandName if bool(saleLayerProductObj.BrandName) else ""
	propertyName = DYEHARD_PROPERTY_TAG_TO_NAME_DICT[saleLayerProductObj.ProdTags] if bool(saleLayerProductObj.ProdTags) else ""
	#If there is exactly one sport in the list (list isn't empty or multi-sport/pick-a-sport product), add that sport name to end of instructions to AI, else just market to fans of the prop's sports in general.
	prodSportList = saleLayerProductObj.Sport
	#print(f"Sport for product {prodSKU} before var assignment: {prodSportList}, {type(prodSportList)}")
	prodSport = f" {prodSportList[0].lower()}" if ( (None not in prodSportList) and (len(prodSportList) == 1) ) else " sports"
	#print(f"Sport for product {prodSKU} after var assignment: {prodSport}")
	instructionsForProductDescription = f"Write a 4 to 6 sentence marketing description for a {ageGroup} {prodFamily} product named '{prodName}' made by {prodSupplier} that will be marketed to fans of {propertyName}{prodSport}.#"
	instructionsForProductDescription = instructionsForProductDescription.replace("youth youth", "youth").replace("  ", " ").replace("�", "")#.replace("", "")
	needsDefinatePronoun = ["AOD", "ARA", "ARK", "AZB", "BEC", "BWS", "CIB", "DEL", "FIB", "GRB", "KYD", "LCF", "MCB", "MIB""OMI", "PIT", "RLF", "SGB", "SUB", "UCO", "UNC", "WCC", "WSO"]
	if saleLayerProductObj.ProdTags in needsDefinatePronoun:
		instructionsForProductDescription = instructionsForProductDescription.replace("marketed to fans of ", "marketed to fans of the ")
	instructionsForProductDescription = instructionsForProductDescription.replace("LouCity Football Club sports", "LouCity Football Club").replace("NYRA Horse Racing sports", "NYRA Horse Racing").replace("NYRA Horse Racing equestrian", "NYRA Horse Racing")
	instructionsForProductDescription = instructionsForProductDescription.replace("Professional Rodeo Cowboys Association sports", "Professional Rodeo Cowboys Association")
	instructionsForProductDescription = instructionsForProductDescription.replace("Racing Louisville Football Club sports", "Racing Louisville Football Club").replace("The World Games sports", "The World Games")#.replace("", "")
	#Add SEO instructions:
	if bool(prodSport):
		#Replace AI stop word ".#" with period and a space, then add keywords followed by stop word:
		instructionsForProductDescription = instructionsForProductDescription.replace("#", ". ")
		instructionsForProductDescription += f"Include keywords: {prodSport}.#"
	print(f"Instruction from SL Data for product {prodSKU}:\n{instructionsForProductDescription}")
	prodDescription = sendProductDescriptionInstructionToOpenAI(instructionsForProductDescription).strip()
	print(f"OpenAI description for product {prodSKU}:\n{prodDescription}")
	#Human Readable Record:
	recordGeneratedProductDescriptionsToCSV(prodSKU, prodName, instructionsForProductDescription, prodDescription)
	return prodDescription

def translateCategoryNamesToCodes(saleLayerProductObj):
	"""Receives a Sales Layer Product obj as a param and generates a list of category codes for Sales Layer based on the obj's list of category names (assigned by AI). Returns the list of category codes"""
	assignedCategoryNameList = saleLayerProductObj.CategoryName #Get the list of category names assigned from AI.
	print(f"\n\nassignedCategoryNameList: {assignedCategoryNameList}")
	productParentCategoryNameList = list(set(parentCategoryNameList).intersection(assignedCategoryNameList)) #Get a list of parent category names
	categoryCodeList = [primaryParentCategories[categoryName] for categoryName in productParentCategoryNameList] #Assign a list of product's category codes filled with parent category codes.
	#Match potential duplicate category names to their codes here (i.e. 'Gifts & Accessories', 'Home & Office', 'Flags', 'Auto', 'Flags'). 
	if ( ("Gifts & Accessories" in assignedCategoryNameList) or ("Post Season Gear" in assignedCategoryNameList) or ("Special Collection" in assignedCategoryNameList) ) \
	and any(subCategoryName in assignedCategoryNameList for subCategoryName in duplicateNoveltySubcategoryList):#Check if any of the parents of duplicate categories were assigned by AI, then if any name on list of duplicate categories are on the AI assigned categories list.
		print(f"\n\nFound ambigous subcategory: {assignedCategoryNameList}")
		#Football is under both Special Collection, Shop Sports:
		if "Football" in assignedCategoryNameList:
			print(f"\n\nFound ambigous Football category.")
			if ("Shop Sports" in assignedCategoryNameList):#If the categories include both shop sports and football:
				categoryCodeList.extend(["SPORTSP", "FUTBLL"])#Add those codes to code list, but only remove one instance of "football" from name list.
				assignedCategoryNameList.remove("Football")#If there is another "Football" in list of cat names, it must be the one under "Special Collections":
				print(f"\n\nFound Shop Sports.")
			if ("Special Collection" in assignedCategoryNameList) and ("Football" in assignedCategoryNameList):
				categoryCodeList.extend(["SPEC01", "FB01"]) #A 2nd "SPEC01" may get added below but the code list is deduped at the end.
				assignedCategoryNameList.remove("Football")
				print(f"\n\nFound Special Collection.")
		#if Flags, or Magnets: Special Collection, Auto
		if any(subCategoryName in assignedCategoryNameList for subCategoryName in ["Flags", "Magnets"]):
			if ("Auto" in assignedCategoryNameList) and ("Flags" in assignedCategoryNameList):
				categoryCodeList.extend(["GIAC05", "AUFL01"])#Add auto and auto flag codes if both "auto" and "flags" in name list.
				assignedCategoryNameList.remove("Flags")#Remove one instance of "flag" from name list.
			if ("Auto" in assignedCategoryNameList) and ("Magnets" in assignedCategoryNameList):
				categoryCodeList.extend(["GIAC05", "AUMA01"])#Add auto and auto magnets codes if both "auto" and "magnets" in name list.
				assignedCategoryNameList.remove("Magnets")#Remove one instance of "magnets" from name list.
			if ("Home & Office" in assignedCategoryNameList) and ("Flags" in assignedCategoryNameList):
				categoryCodeList.extend(["GAHO03", "GIAC01"])#"Home & Office" & "Flags" cat codes may get added twice below then deduped.
				assignedCategoryNameList.remove("Flags")#Remove one instance of "flag" from name list.
			if ("Home & Office" in assignedCategoryNameList) and ("Magnets" in assignedCategoryNameList):
				categoryCodeList.extend(["HOMA01", "GIAC01"])
				assignedCategoryNameList.remove("Magnets")#Remove one instance of "magnets" from name list.
		#if "Buttons & Pins": Personal Accessories vs Tailgate Gear
		if "Buttons & Pins" in assignedCategoryNameList:
			if ("Personal Accessories" in assignedCategoryNameList):#Category codes may get added twice then deduped
				categoryCodeList.extend(["GIAC07", "PABP01"])#Add personal accessories and personal accessories buttons & pins codes if both "personal accessories" and "buttons & pins" in name list.
				assignedCategoryNameList.remove("Buttons & Pins")
			if ("Buttons & Pins" in assignedCategoryNameList) and ("Tailgate Gear" in assignedCategoryNameList):
				categoryCodeList.extend(["GIAC02", "BUTT01"])
				assignedCategoryNameList.remove("Buttons & Pins")
		#if 2 "Post Season Gear", add codes for both cats w/ that name (they're parent & child):
		if ("Special Collection" in assignedCategoryNameList) and ("Post Season Gear" in assignedCategoryNameList):
			categoryCodeList.extend(["SPEC01", "PSTSPRTS22"])#Add special categories (may get deduped later) and 1st child post season gear cat code.
			if (assignedCategoryNameList.count("Post Season Gear") > 1):#If there there a 2nd post season gear in the cat name list, add the 2nd code to the cat code list.
				categoryCodeList.extend(["PSTSZN22"])
		print(f"\n\nMatching duplicate G&A subcategory to code. Current category codes: {categoryCodeList}")
	for parentCategoryName in productParentCategoryNameList: #Loop through parent category names, match to subcategoryDicts dict.
		allSubcategoryNames = subcategoryDicts[parentCategoryName].keys() #List of all subcategory names for current parent cat.
		print(f"\n\nallSubcategoryNames for {parentCategoryName}: {allSubcategoryNames}")
		matchedSubcategoryDict = subcategoryDicts[parentCategoryName] #The dict of subcategory that will be searched for matching codes to add to the product.
		print(f"\n\nmatchedSubcategoryDict: {matchedSubcategoryDict}")
		subcategoryNamesToMap = list(set(allSubcategoryNames).intersection(assignedCategoryNameList)) # Get list of subcategory names to map to codes and add to product
		subcategoryCodesToAdd = [matchedSubcategoryDict[subcategoryName] for subcategoryName in subcategoryNamesToMap] #
		categoryCodeList.extend(subcategoryCodesToAdd) #Add subcategory codes to temporary list of codes to ulitimately add to product.
	#Check if any names in assignedCategoryNameList are in miscellaneousCategories before trying to map any of those codes.
	miscellaneousCategoryNames = miscellaneousCategories.keys()
	if any(categoryName in assignedCategoryNameList for categoryName in miscellaneousCategoryNames):
		print(f"MiscellaneousCategories names found.")
		miscCategoryNamesToMap = list(set( miscellaneousCategoryNames ).intersection(assignedCategoryNameList)) #
		miscCategoryCodesToAdd = [miscellaneousCategories[miscellaneousCategoryName] for miscellaneousCategoryName in miscCategoryNamesToMap] #
		categoryCodeList.extend(miscCategoryCodesToAdd) #

	print(f"{saleLayerProductObj.ProductSKU}: assignedCategoryNameList: {assignedCategoryNameList},  productParentCategoryNameList: {productParentCategoryNameList},  categoryCodeList: {categoryCodeList}")
	productCategoryCodeList = saleLayerProductObj.Category #Category codes assigned when product obj created: 'PRODUCT', 'All Product', 'New Arrivals'
	productCategoryCodeList.extend(categoryCodeList) #Combine original list with list of codes returned from AI
	saleLayerProductObj.Category = list(set(productCategoryCodeList)) #Dedup combined list and reassign to product obj
	return saleLayerProductObj

def sendProductCategoryInformationToOpenAI(input_prompt):
	""""""
	# create a completion
	try:
		completion = openai.Completion.create(engine=DYEHARD_ECOMM_PRODUCT_CATEGORIZATION_AI, prompt=input_prompt, temperature=0, stop="##", max_tokens=200, frequency_penalty=0, presence_penalty=0)
		generatedProductCategoryNames = completion.choices[0].text
		#Print the completion
		print(completion)
		print(f"Product Category Assignments from AI:\n{generatedProductCategoryNames}, {type(generatedProductCategoryNames)}")
	except Exception as checkProductCategoriesError:
		generatedProductCategoryNamesErrorLogText = f"Error assigning product categories with OpenAI API :\n{checkProductCategoriesError}\n\n"
		print(generatedProductCategoryNamesErrorLogText)
		writeLog(generatedProductCategoryNamesErrorLogText, logType="error")
		generatedProductCategoryNames = "AI Category Assignment Failed"
	return generatedProductCategoryNames

def assignProductCategoriesWithAI(saleLayerProductObj):
	"""Generates and sends a prompt to Dyehard's OpenAI categorization model via API, receives and returns a list of category names."""
	prodSKU = saleLayerProductObj.ProductSKU
	productName = saleLayerProductObj.ProductName.replace("\"", "\\\"")#Escape quotes in prod names.
	#categoryName = saleLayerProductObj.CategoryName
	groupName = saleLayerProductObj.ItemGroup
	itemType = saleLayerProductObj.ItemType
	ageGroup = saleLayerProductObj.AgeGroup
	gender = saleLayerProductObj.Gender
	#Set sport to blank if no OR multiple sports:
	prodSportList = saleLayerProductObj.Sport
	#print(prodSportList, type(prodSportList), bool(prodSportList))
	Sport = f"{prodSportList[0].lower()}" if ( (None not in prodSportList) and (len(prodSportList) == 1) ) else ""
	#print(f"Before AI: {prodSKU}: :{categoryName}")
	promptForCategoryCheckerAI = f"Product Name: {productName}, Group Name: {groupName}, Item Type: {itemType}, Age Group: {ageGroup}, Gender: {gender}, Sport: {Sport}##"
	updatedCategoryNames = sendProductCategoryInformationToOpenAI(promptForCategoryCheckerAI).strip()
	#Human Readable Record:
	recordGeneratedProductCategoriesToCSV(prodSKU, promptForCategoryCheckerAI, updatedCategoryNames, productName)
	listOfCategoryNames = updatedCategoryNames.split(", ") if "AI Category Assignment Failed" not in updatedCategoryNames else [] #Return empty list if AI category assignment failed.
	return listOfCategoryNames


if __name__ == "__main__":
	origPrice = "50.01"
	testProduct = productClass("ARKN999333", "Novelty", "Arkansas Test Product III Razorbacks Seat Cushion", ["PRODUCT", "All Product", "New Arrivals"], ["PRODUCT", "ALL", "NEWA01"], "", "ARK", origPrice, "", "0", "ARKN999333.jpg", "Colosseum", "26", "Adult", "Unisex", "No", "True", "SP23", "Baseball", "False", "", "", "", "", "", "", "", "", "NationalWiffleBallPlayOffs", "", "", "Imported", "WSD", "", "", "0", "16.0", "Default Tax Class", "PC040100", "Default Tax Class", "", "", "2", "", "", "", "", "V500027", "COUZ11523W", "Mens", "LONG SLEEVE", "MENS", "", "Variant", "arkansas-razorbacks-take-your-time-1-4-zip-windshirt-ARKM100282", "Fleece, pullover, sweats, hoodie, windshirt, sweatshirt, wind shirt, sweat shirt, pull over, 1/4 zip, quarter zip, Shep Shirt, Shepshirt, Colosseum", ",New,White,Men,Adult", "Age>Adult;Gender>Men;Color>White;Origin>Imported", "07/15/22", "20.70", "Yes", True, True, ["999"], True, ["XS", "S", "M", "L", "XL", "2XL"], ["Multi"], "TestProductLineName")
	categoriesFromAI = ["Gifts & Accessories", "PRODUCT", "All Product", "New Arrivals", "Miscellaneous", "Shop Sports", "Football", "Stadium Accessories", "Seat Cushions"]#, "Personal Accessories", "Buttons & Pins", "Tailgate Gear", "Stadium Accessories", "Seat Cushions"
	testProduct.CategoryName = categoriesFromAI
	testProduct.calcRetailPrice()
	testProduct.checkIfMultiColor()
	testProduct.testExtraProdMethod()
	testProduct.checkIfDropShip()
	print(testProduct.CategoryName)
	print(testProduct.Category)
	#testProductAfterCatNameToCodeMapping = translateCategoryNamesToCodes(testProduct)
	#print(f"Parent Categories: {testProductAfterCatNameToCodeMapping.CategoryName}, {testProductAfterCatNameToCodeMapping.Category}")
	testProduct = translateCategoryNamesToCodes(testProduct)
	print(f"Categories Names: {testProduct.CategoryName}, Categories Codes: {testProduct.Category}")
