#!/usr/bin/env python3

import re
from Constants import *
from SAP_Data_Class import *
from Product_Class import *
from Variant_Class import *
from File_Read_and_Write_Functions import *
from Product_Name_Functions import *
from Product_And_Variant_Functions import *
from Artificial_Intelligence_Functions import *
from Natural_Language_Processing_Functions import *

def assembleProductData(SAPData):#SAPData will be dict of SAP data export.
	"""Returns dict of product SKU keys with SAP variant object lists for values from SAPData received."""
	SAPProductData = {}
	for key, value in SAPData.items():
		#print(value.Model)
		if value.Model =="":
			value.Model = getSKU(value.ItemNo)
		if value.Model not in SAPProductData.keys():
			SAPProductData[value.Model] = [value]
		else:
			SAPProductData[value.Model].append(value)
	return SAPProductData

def getSKU(variantSKU):
	"""Returns product SKU from variant SKU parameter variantSKU."""
	#Used when productData.Model is blank. Reused from the original DOMO/SAP data conversion script.
	variantSKU = variantSKU.replace("-OSFM", "").replace("-OSFA", "").replace("-OS", "").replace("-ADJ", "")
	generatedProductSKU = re.sub("-[0-9][A-Z]*$", "", variantSKU) #10/28/21 Added to strip sizes from normal & POD SKUs w/ normal size runs.. Would run into issues w/ some shoe/youth sizes and so on.
	generatedProductSKU = re.sub("-[0-9]{3}$", "", generatedProductSKU)
	generatedProductSKU = re.sub("-[A-Z]*$", "", generatedProductSKU) #12/14/21 Repeated.
	generatedProductSKU = re.sub("-[A-Z]*/[A-Z]*$", "", generatedProductSKU) #Hat size
	generatedProductSKU = re.sub("-[0-9] [0-9]/[0-9]*$", "", generatedProductSKU) #Hat size
	generatedProductSKU = re.sub("-[0-9]-", "-", generatedProductSKU)
	generatedProductSKU = re.sub("_[0-9]*$", "", generatedProductSKU)
	generatedProductSKU = re.sub("-[0-9]*.[0-9]*$", "", generatedProductSKU)
	generatedProductSKU = re.sub("-[A-Z]*$", "", generatedProductSKU) #12/14/21 Repeated.
	#print(variantSKU, generatedProductSKU, sep="\t")
	return generatedProductSKU

def generateSLVariantFromSAPData(inputSAPData):
	"""Receives SAP_Data_Class from dict SAP data created by assembleProductData(), returns Variant Class obj."""
	#Used in a loop that will read dict SAP data created by assembleProductData(). Loop will also generate SL product data
	#This outputSLVariant assignment assigns all attributes here. To be used if default values are to be added dynamically with outputSLVariant.addDefaultSLVariantValues().
	'''outputSLVariant = variantClass(inputSAPData.ItemNo, inputSAPData.Model, "Default Condition (value=Visible)", inputSAPData.ModelGroup, inputSAPData.Size, "Blank_Variant_Price",\
		"Need Variant Images", "Blank_Vendor_Variant_Color", inputSAPData.Color, "Need Variant Sport", "Need Variant Sort Order", "Blank_Product_Length", "Blank_GTIN",\
		inputSAPData.ForeignName, "Blank_UPC", "Default Low Stock Level (value=1)", "Blank_Variant_Height", "Blank_Variant_Width", "Blank_Variant_Depth",\
		"Blank_Variant_Weight", inputSAPData.BarCode, inputSAPData.Color, "Need Color Name", "Blank_Image_Required", inputSAPData.VendorUPC, inputSAPData.eCommListingSKU)'''
	variantColorCode = inputSAPData.Color if bool(inputSAPData.Color) else None
	variantColorName = inputSAPData.ColorDescription if bool(inputSAPData.ColorDescription) else None
	variantSortOrder = "1" #Need Variant Sort Order (WMT only)?
	vendorUPC = inputSAPData.VendorUPC if bool(inputSAPData.VendorUPC) else None
	cost = COGs = inputSAPData.MainBuyingPrice
	outputSLVariant = variantClass(#Params/Attrs for SL import data:\
		inputSAPData.ItemNo, inputSAPData.Model, "Visible" ,inputSAPData.ModelGroup, inputSAPData.Size, inputSAPData.MainSellingPrice,\
		"Variant Images will be found using matchVariantsToFoundImages()->findProductAndVariantImages()->mergeSLVariantDataWithMatchingVariantImagesDict() (WMT only?)", None,\
		variantColorCode, "Variant Sport will be added by compileSLProductSportsList() in Product_And_Variant_Functions.py", variantSortOrder, None, None,\
		inputSAPData.ForeignName, vendorUPC, 1, None, None, None, "*Need Variant Weight from ProductWeight (not currently uploaded to SL).*", inputSAPData.BarCode, variantColorCode, variantColorName,\
		"ImageRequired set by generateDictsOfSLProductsAndVariants() in this file (WMT only?).", vendorUPC, inputSAPData.eCommListingSKU, cost, COGs\
		#End params/attrs for SL import data.\
		)
	outputSLVariant.calcVariantRetailPrice()
	outputSLVariant = assignProductOrVariantSport(inputSAPData, outputSLVariant) #outputSLVariant = assignment shouldn't be required. Sport seems to be missing with or without.
	

	return outputSLVariant

def generateSLProductFromSAPData(inputSAPData):
	"""Receives SAP_Data_Class from dict SAP data created by assembleProductData(), returns Product Class obj."""
	outputSLProduct = productClass(#Params/Attrs for SL import data:\
		inputSAPData.Model, inputSAPData.assignProductFamily(), updateSAPProductName(inputSAPData.ItemDescription),\
		["PRODUCT", "All Product", "New Arrivals"], ["PRODUCT", "ALL", "NEWA01"],\
		None, inputSAPData.ModelGroup, inputSAPData.MainSellingPrice, None, False, "Product images will be added by findProductAndVariantImages() in Image_Matching_Functions.py",\
		inputSAPData.BrandName, inputSAPData.ProductBrand, "Adult", "Unisex", True, True, inputSAPData.Season,\
		"Sport will be added by compileSLProductSportsList() in Product_And_Variant_Functions.py", "*Need Memorabilia*", None, None, None, None, None, None, None, None,\
		inputSAPData.ProductCollection, None, "*Need SportsTeam*", inputSAPData.CountryofOrigin, inputSAPData.DefaultWarehouse, None, None, False,\
		None, "Default Tax Class", "PC040100", "Default Tax Class", inputSAPData.ModelGroup, None, inputSAPData.ProductLineCode, None,\
		inputSAPData.ProductionDate, None, False, inputSAPData.PreferredVendor, inputSAPData.ForeignName, inputSAPData.GroupName, inputSAPData.ProductLineName, inputSAPData.GroupName.upper(),\
		None, "Variant", "*Handle generated by generateHandle() in Product_Class_Methods.py*", "*Need Keywords*", "*Need WMTTags (WMT only)*", "*Need Filters (WMT only)*",\
		inputSAPData.ProductionDate, inputSAPData.MainBuyingPrice, True,\
		#End params/attrs for SL import data. Begin user created attr:\
		"isDropShip generated by checkIfDropShip() in Product_Class_Methods.py", "*Need isPrivateLabel*", [inputSAPData.Color], "isMultiColor generated by checkIfMultiColor() in Product_Class.py",\
		[inputSAPData.Size], [inputSAPData.ColorDescription], inputSAPData.ProductLineName\
		)
	outputSLProduct.calcRetailPrice()
	outputSLProduct.generateHandle()
	outputSLProduct.checkIfDropShip()
	outputSLProduct.setProductWeight()
	outputSLProduct.setAvalaraTaxCode()
	outputSLProduct.setAgeGroupGenderAndIfUnisex()
	#print(f"Before running assignProductOrVariantSport on product: {outputSLProduct}")
	outputSLProduct = assignProductOrVariantSport(inputSAPData, outputSLProduct)
	#print(f"After running assignProductOrVariantSport on product: {outputSLProduct}")
	outputSLProduct = assignSportsTeamAndMemorabilia(outputSLProduct)
	outputSLProduct.assignProductCategoryNamesAndCodes(inputSAPData)
	outputSLProduct.Keywords = parseProductNameForSearchKeywords(outputSLProduct.ProductName)
	if outputSLProduct.ProductSKU not in RECENTLY_UPLOADED_PRODUCTS.keys():#Do not process already uploaded products' data with AI.
		outputSLProduct.ProductDescription = outputSLProduct.OldDescription = generateProductDescriptionWithAI(outputSLProduct)
		print(f"Product descripion for {outputSLProduct.ProductSKU}: {outputSLProduct.ProductDescription}")
		outputSLProduct.CategoryName = assignProductCategoriesWithAI(outputSLProduct)
		outputSLProduct = translateCategoryNamesToCodes(outputSLProduct)
	return outputSLProduct

#General "update SL product attr" func (could be reused for var attr if needed).
def updateAttribute(dataObj, dataAttribute, attributeValue):
	"""Receive object, object attribute, and a value. Returns object with attribute value."""
	#print(f"Updating: {dataObj}")
	dataObjAttribute = getattr(dataObj, dataAttribute)
	if (type(dataObjAttribute) == list) and (attributeValue not in dataObjAttribute):
		dataObjAttribute.append(attributeValue)
	elif not bool(dataObjAttribute):
		setattr(dataObj, dataAttribute, attributeValue)
	#print(f"New: {dataObj}")
	return dataObj

def updateAllAttributes(saleLayerDataObj, SAPObject):
	"""Takes existing SL product obj & SAP var obj; updates SL product obj with SAP var obj data."""
	updateAttribute(saleLayerDataObj, "colorList", SAPObject.Color)
	updateAttribute(saleLayerDataObj, "colorDescriptionList", SAPObject.ColorDescription)
	updateAttribute(saleLayerDataObj, "sizeList", SAPObject.Size)
	compileSLProductSportsList(saleLayerDataObj, SAPObject)
	return None

def generateDictsOfSLProductsAndVariants(inputSAPDataDict):
	"""Loops through list of SAP Data obj from assembleProductData(), returns dict of Product SKU keys/Variant Class obj list and dict of Product SKU keys/Product Class obj values."""
	#A combination of the generateDictOfSLVariants and generateDictOfSLProducts funcs to consolidate loops through source data.
	SLVariantDict = {}
	SLProductDict = {}
	print(f"RECENTLY_UPLOADED_PRODUCTS.keys(): {RECENTLY_UPLOADED_PRODUCTS.keys()}")
	for SLProductSKUKey, SAPVariantDataList in inputSAPDataDict.items():
		if (SLProductSKUKey in RECENTLY_UPLOADED_PRODUCTS.keys()):
			print(f"{SLProductSKUKey} found in RECENTLY_UPLOADED_PRODUCTS.keys().")
			#If product is online, generate SL prod class so any new variants can access prod data, but do not add new prod obj to be uploaded.
			#generateSLProductFromSAPData() should internally check uploaded prod SKUs and skip AI processing.
			currentProduct = generateSLProductFromSAPData(SAPVariantDataList[0])
			##If currentProduct price, brand ID/name, & WH doesn't match the corresponding values on the tracking sheet/dict, add product dict of modified products to upload.
			uploadedVersionOfCurrentProduct = RECENTLY_UPLOADED_PRODUCTS[SLProductSKUKey]
			print(f"currentProduct: {currentProduct}, uploadedVersionOfCurrentProduct: {uploadedVersionOfCurrentProduct}")
			if (currentProduct.Price != uploadedVersionOfCurrentProduct["Price"])\
			or (currentProduct.BrandName != uploadedVersionOfCurrentProduct["Brand Name"])\
			or (currentProduct.ProductBrandID != uploadedVersionOfCurrentProduct["Product Brand ID"])\
			or (currentProduct.DefaultWarehouse != uploadedVersionOfCurrentProduct["Default Warehouse"]):
				RECENTLY_MODIFIED_PRODUCTS[SLProductSKUKey] = {"Product SKU": SLProductSKUKey}
				#Test if values exist. Otherwise set value to none.
				currentPrice = currentProduct.Price
				currentBrandName = currentProduct.BrandName
				currentBrandID = currentProduct.ProductBrandID
				currentWH = currentProduct.DefaultWarehouse
				RECENTLY_MODIFIED_PRODUCTS[SLProductSKUKey]["Price"] = currentPrice if (bool(currentPrice)) else None
				RECENTLY_MODIFIED_PRODUCTS[SLProductSKUKey]["Brand Name"] = currentBrandName if (bool(currentBrandName)) else None
				RECENTLY_MODIFIED_PRODUCTS[SLProductSKUKey]["Product Brand ID"] = currentBrandID if (bool(currentBrandID)) else None
				RECENTLY_MODIFIED_PRODUCTS[SLProductSKUKey]["Default Warehouse"] = currentWH if (bool(currentWH)) else None
				print(f"Added {RECENTLY_MODIFIED_PRODUCTS[SLProductSKUKey]} to RECENTLY_MODIFIED_PRODUCTS.")

		if (SLProductSKUKey not in SLProductDict.keys()) and (SLProductSKUKey not in RECENTLY_UPLOADED_PRODUCTS.keys()):
			#Generate initial product info from 1st variant in SAP data:
			#print(f"Creating new product {SLProductSKUKey}.")
			SLProductDict[SLProductSKUKey] = generateSLProductFromSAPData(SAPVariantDataList[0])
			currentProduct = SLProductDict[SLProductSKUKey]
			for variant in SAPVariantDataList:
				updateAllAttributes(currentProduct, variant)
			currentProduct.checkIfMultiColor()
			listOfPossibleEmptyAttributesToCheck = [currentProduct.colorList, currentProduct.colorDescriptionList, currentProduct.sizeList, currentProduct.Sport]
			[setEmptyListsToNone(eachList) for eachList in listOfPossibleEmptyAttributesToCheck]
		if SLProductSKUKey not in SLVariantDict.keys():
			SLVariantDict[SLProductSKUKey] = []
		for SAPVariantData in SAPVariantDataList:
			if SAPVariantData.ItemNo not in RECENTLY_UPLOADED_VARIANTS.keys():
				newSLVariant = generateSLVariantFromSAPData(SAPVariantData)
				newSLVariant.addBlankValues()
				newSLVariant.VariantWeight = currentProduct.ProductWeight #Sets the variant to the product's weight. Would change if adding variant pricing (SAP doesn't have weight in export, 12/29/22).
				newSLVariant.ImageRequired = True if currentProduct.isMultiColor else False
				SLVariantDict[SLProductSKUKey].append(newSLVariant)
			else:#If variant is on the tracking document, check if variant values need to be updated (VendorUPC as o 03/21/23)
				if (bool(SAPVariantData.VendorUPC)) and (SAPVariantData.VendorUPC != RECENTLY_UPLOADED_VARIANTS[SAPVariantData.ItemNo]["VendorUPC"]):# and (SAPVariantData.VendorUPC != ""):
					currentVendorUPC = SAPVariantData.VendorUPC
					RECENTLY_MODIFIED_VARIANTS[SAPVariantData.ItemNo] = {"Variant SKU": SAPVariantData.ItemNo}
					RECENTLY_MODIFIED_VARIANTS[SAPVariantData.ItemNo]["VendorUPC"] = currentVendorUPC if (bool(currentVendorUPC)) else None
					recentUPC = RECENTLY_UPLOADED_VARIANTS[SAPVariantData.ItemNo]["VendorUPC"]
					print(f"SAPVariantData.VendorUPC: {SAPVariantData.VendorUPC} :RECENTLY_UPLOADED_VARIANTS[SAPVariantData.ItemNo]['VendorUPC'] {recentUPC}")
		
	return SLProductDict, SLVariantDict

if __name__ == "__main__":
	testInputFile = fr"C:\Users\Sean Creedon\OneDrive - Dyehard Fan Supply\Python-Scripts\SAP_to_Sales_Layer_Data_Converter\Test_Data\Small-Post-Col-Update-SAP-Product-Data.csv"
	testFunc = readSAPDataCSV
	testOutput = readCSV(testInputFile, testFunc)
	#Assemble SAP export data for processing test:
	testAssembledSAPData = assembleProductData(testOutput)
	testSLProductDict, testSLVariantDict =  generateDictsOfSLProductsAndVariants(testAssembledSAPData)
	#print(testSLProductDict)
	#List comprehension nested in list comprehension of a dictionary just to F around. Sorry future self:
	[print(product, [str(item) for item in var]) for product, var  in testSLVariantDict.items()]
	[print(f"SL Product {prodKey} info: {prodValue}") for prodKey, prodValue in testSLProductDict.items()]
