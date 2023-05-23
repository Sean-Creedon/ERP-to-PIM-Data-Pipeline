#!/usr/bin/env python3

import re, csv, os, logging, shutil
from tempfile import NamedTemporaryFile
from SAP_Data_Class import *
from Product_Class import *
from Variant_Class import *
from Constants import *

def ensureOutputFolderExists(folderToCheck):
	"""Checks for the existence of the folder path given as input and creates it if needed."""
	if not os.path.exists(folderToCheck):
		os.makedirs(folderToCheck)

#Mainly for reading SAP export data. Meant to also be reused for DOMO data, etc.
def readCSV(inputFile, loadDataFunc):
	"""Reads .CSV input file, loads data to memory using designated function, returns input data as output class instance."""
	with open(inputFile, "r", encoding="utf8", errors="surrogateescape") as csv_file:
		csv_reader = csv.DictReader(csv_file)
		#inputFileHeaders = csv_reader.fieldnames #For troubleshooting.
		outputData = loadDataFunc(csv_reader)
	return outputData

def readUploadedProductTrackingSheets(inputProductTrackingSheet):
	""""""
	with open(PRODUCT_UPLOAD_TRACKING_SHEET, "r", encoding="utf8", errors="surrogateescape") as permanentProductUploadTrackingCSV:
		#Add loop to add rows from previous uploaded products if date is less than 2 days old.
		permanentProductTrackingCSVReader = csv.DictReader(permanentProductUploadTrackingCSV)
		for row in permanentProductTrackingCSVReader:
			prodSKU = row["Product SKU"]
			prodPrice = row["Price"]
			prodBrand = row["Brand Name"]
			prodBrandID = row["Product Brand ID"]
			prodWH = row["Default Warehouse"]
			originalProdUploadDate = row["Upload Date"]
			prodUploadDate = datetime.datetime.strptime(originalProdUploadDate, "%m-%d-%y")#Get text of upload date from sheet and convert to datetime obj.
			timeProdHasBeenOnline = NOW - prodUploadDate
			daysProdHasBeenOnline = timeProdHasBeenOnline.days
			#If the product has been online for less than 2 day, add it to list of uploaded product SKUs.
			if (daysProdHasBeenOnline < 2):
				print(f"Adding {prodSKU} to the dict of products already uploaded to SL.")
				RECENTLY_UPLOADED_PRODUCTS[prodSKU] = {}
				RECENTLY_UPLOADED_PRODUCTS[prodSKU]["Product SKU"] = prodSKU
				RECENTLY_UPLOADED_PRODUCTS[prodSKU]["Price"] = prodPrice if (bool(prodPrice) and prodPrice != "" and prodPrice != "None") else None
				RECENTLY_UPLOADED_PRODUCTS[prodSKU]["Brand Name"] = prodBrand if (bool(prodBrand) and prodBrand != "" and prodBrand != "None") else None
				RECENTLY_UPLOADED_PRODUCTS[prodSKU]["Product Brand ID"] = prodBrandID if (bool(prodBrandID) and prodBrandID != "" and prodBrandID != "None") else None
				RECENTLY_UPLOADED_PRODUCTS[prodSKU]["Default Warehouse"] = prodWH if (bool(prodWH) and prodWH != "" and prodWH != "None") else None
			else:
				print(f"Not adding {prodSKU} to the dict of products already uploaded to SL.")
				continue
	print(f"RECENTLY_UPLOADED_PRODUCTS: {RECENTLY_UPLOADED_PRODUCTS}")
	return RECENTLY_UPLOADED_PRODUCTS

def readUploadedVariantTrackingSheets(inputVariantTrackingSheet):
	""""""
	with open(VARIANT_UPLOAD_TRACKING_SHEET, "r", encoding="utf8", errors="surrogateescape") as permanentVariantUploadTrackingCSV:
		#Add loop to add rows from previous uploaded variants if date is less than 2 days old..
		permanentVariantTrackingCSVReader = csv.DictReader(permanentVariantUploadTrackingCSV)
		for row in permanentVariantTrackingCSVReader:
			varSKU = row["Variant SKU"]
			varVendorUPC = row["VendorUPC"]
			originalVarUploadDate = row["Upload Date"]
			varUploadDate = datetime.datetime.strptime(originalVarUploadDate, "%m-%d-%y")#Get text of upload date from sheet and convert to datetime obj.
			timeVarHasBeenOnline = NOW - varUploadDate
			daysVarHasBeenOnline = timeVarHasBeenOnline.days
			#If the variant has been online for 2 or more days or is in the list of variants uploaded, do not add row from permanent tracking sheet to temporary tracking sheet.
			if (daysVarHasBeenOnline < 2):
				print(f"Adding {varSKU} to the list of variant SKUs already uploaded to SL.")
				RECENTLY_UPLOADED_VARIANTS[varSKU] = {}
				RECENTLY_UPLOADED_VARIANTS[varSKU]["Variant SKU"] = varSKU
				RECENTLY_UPLOADED_VARIANTS[varSKU]["VendorUPC"] = varVendorUPC if (bool(varVendorUPC) and varVendorUPC != "" and varVendorUPC != "None") else None
			else:
				print(f"Not adding {varSKU} to the list of variant SKUs already uploaded to SL.")
				continue
	print(f"RECENTLY_UPLOADED_VARIANTS: {RECENTLY_UPLOADED_VARIANTS}")
	return RECENTLY_UPLOADED_VARIANTS

#Create product upload tracker and write initial header if it doesn't exist
if not os.path.exists(PRODUCT_UPLOAD_TRACKING_SHEET):
	with open(PRODUCT_UPLOAD_TRACKING_SHEET, mode='w', newline='') as trackProductUploadsCSV:
		trackProductUploadsCSV.write(f"Product SKU,Price,Brand Name,Product Brand ID,Default Warehouse,Upload Date")
else:#Get list of currently tracked Product SKUs
	RECENTLY_UPLOADED_PRODUCTS = readCSV(PRODUCT_UPLOAD_TRACKING_SHEET, readUploadedProductTrackingSheets)
#Create variant upload tracker and write initial header if it doesn't exist
if not os.path.exists(VARIANT_UPLOAD_TRACKING_SHEET):
	with open(VARIANT_UPLOAD_TRACKING_SHEET, mode='w', newline='') as trackVariantUploadsCSV:
		trackVariantUploadsCSV.write(f"Variant SKU,VendorUPC,Upload Date")
else:#Get list of currently tracked Variant SKUs
	RECENTLY_UPLOADED_VARIANTS = readCSV(VARIANT_UPLOAD_TRACKING_SHEET, readUploadedVariantTrackingSheets)

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
	#01/04/22 Should below come out completely? Color code should stripped from prod SKUs already. Old Prod SKUs w/ color codes getting matched to wrong colors.
	#01/10/22 Disabled line below (removed color codes) since used in var img matching. Is there any time this would affect prod img matching?
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

def convertListForCSV(inputList):
	"""Takes a list (product or variant attribute) and converts it to comma-separated text values: ["a", "b"] becomes a, b. None values are replaced with blanks"""
	outputList = str(inputList) if bool(inputList) else "" #Converts the list to a string or sets SL product attribute to blank string if the input is None.
	outputList = outputList.replace("[", "").replace("]", "").replace("'", "") #Replaces list syntax punctuation: ['',''']
	#print(outputList, type(outputList), sep="\t")
	return outputList

def convertNoneToEmptyString(inputValue):
	"""""Returns empty string if inputValue is None else the original value is returned."""""
	outputValue = inputValue if bool(inputValue) else ""
	return outputValue

def writeSalesLayerProductImportSheet(inputDict, fullOutputPath):
	"""Receives inputDict dict, writes its output to a CSV to import to Sales Layer. Returns its inputDict"""
	with open(fullOutputPath, mode='w', newline='') as outputCSV:
		outputCSV.write(SALESLAYER_PRODUCT_IMPORT_SHEET_HEADER)
		for prodSKU, product in inputDict.items():
			#print(f"Writing to CSV: {prodSKU}, {product}")
			categoryCodes, categoryNames = convertListForCSV(product.Category), convertListForCSV(product.CategoryName)
			productImages, productSports = convertListForCSV(product.ProductImages), convertListForCSV(product.Sport)
			prodDescription = product.ProductDescription if bool(product.ProductDescription) else "" #Sets SL product description to blank string if the description is None.
			productPrice = convertNoneToEmptyString(product.Price)
			useOldDescription = "0" if not product.UseOldDescription else "1" #Sets default value of product.UseOldDescription to 0 unless it is true (never happens).
			prodActivity, prodFit = convertNoneToEmptyString(product.Activity), convertNoneToEmptyString(product.Fit)
			prodMaterialType, materialContent, temperatureRating = convertNoneToEmptyString(product.MaterialType), convertNoneToEmptyString(product.MaterialContent), convertNoneToEmptyString(product.TemperatureRating)
			careInstructions, features, playerName,league = convertNoneToEmptyString(product.CareInstructions), convertNoneToEmptyString(product.Features), convertNoneToEmptyString(product.PlayerName),convertNoneToEmptyString(product.League)
			prodSportTeam = convertNoneToEmptyString(product.SportsTeam)
			leadTime, fixedShippingCost = convertNoneToEmptyString(product.LeadTime), convertNoneToEmptyString(product.FixedShippingCost)
			freeShipping = "0" if not bool(product.FreeShipping) else "1" #Defaults to False as of 12/12/22 (hence the use of "if not"/"short-circuit" evaluation).
			prodWeight = convertNoneToEmptyString(product.ProductWeight)
			modelGroup = productionDate = ""#product.ModelGroup is probably a duplicate of (property) Tag. The "Model Group" column is blank on import sheets (12/12/22). Production Date is currently emtpy (12/12/12).
			previousEcommNumber, inventoryItem, purchaseItem = convertNoneToEmptyString(product.PreviouseCommNumber), convertNoneToEmptyString(product.InventoryItem), convertNoneToEmptyString(product.PurchaseItem)
			salesItem, allowPurchases = convertNoneToEmptyString(product.SalesItem), convertNoneToEmptyString(product.AllowPurchases)
			#prod = convertNoneToEmptyString(product.)
			#CreatedDate format is 01/01/01 in SAP exports, but 0001-01-01 (YYYY-MM-DD) in DOMO exports.
			discountsAndPromosApplicable = "Yes" if bool(product.DiscountsAndPromotionsApplicable) else "No"
			outputCSV.write(f"{product.ProductSKU},{product.Family},{product.ProductName}," + '"'+categoryNames+'"' + "," + '"'+categoryCodes+'"' + "," + '"'+prodDescription+'"' + f",{product.ProdTags},{productPrice}," + '"'+prodDescription+'"' + f",{useOldDescription}," + '"'+productImages+'"' + f",,,,,,,,,,,,,,{product.BrandName},{product.ProductBrandID},{product.AgeGroup},{product.Gender},{product.IsUnisex},{product.IsLicensed},{product.Season}," + '"'+productSports+'"' + f",{product.Memorabilia},{prodActivity},{prodFit},{prodMaterialType},{materialContent},{temperatureRating},{careInstructions},{features},{playerName},{product.EventCollection},{league},{prodSportTeam},{product.CountryofOrigin},{product.DefaultWarehouse},{leadTime},{fixedShippingCost},{freeShipping},{prodWeight},{product.TaxLiable},{product.AvaTaxCode},{product.ProductTaxClass},{modelGroup},{previousEcommNumber},{product.ProductLineCode},{inventoryItem},{productionDate},{purchaseItem},{salesItem},{product.PreferredVendor},{product.ForeignName},{product.ItemGroup},{product.ItemType},{product.Division},{allowPurchases},{product.TrackInventory},{product.Handle}," + '"'+str(product.Keywords)+'"' + "," + '"'+str(product.WMTTags)+'"' + f",{product.Filters},{product.CreatedDate},{product.COGS},{discountsAndPromosApplicable}\n")
	return inputDict


def writeSalesLayerVariantImportSheet(inputDict, fullOutputPath):
	"""Receives inputDict dict, writes its output to a CSV to import to Sales Layer. Returns its inputDict"""
	#print("Variant Dict:" ,inputDict, type(inputDict), sep="\n")
	with open(fullOutputPath, mode='w', newline='') as outputCSV:
		outputCSV.write(f"{SALESLAYER_VARIANT_IMPORT_SHEET_HEADER}")
		for variantList in inputDict.values():
			for variant in variantList:
				#print(variant, type(variant), sep="\n")
				#convertListForCSV()
				variantPrice = convertNoneToEmptyString(variant.VariantPrice)
				variantImage = convertListForCSV(variant.VariantImage)
				#convertNoneToEmptyString()
				vendorVariantColor, variantColor, variantSport = convertNoneToEmptyString(variant.VendorVariantColor), convertNoneToEmptyString(variant.VariantColor), convertNoneToEmptyString(variant.VariantSport)
				productLength, GTIN, MPN, UPC = convertNoneToEmptyString(variant.ProductLength), convertNoneToEmptyString(variant.GTIN), convertNoneToEmptyString(variant.MPN), convertNoneToEmptyString(variant.UPC)
				variantHeight, variantWidth, variantDepth = convertNoneToEmptyString(variant.VariantHeight), convertNoneToEmptyString(variant.VariantWidth), convertNoneToEmptyString(variant.VariantDepth)
				variantWeight = convertNoneToEmptyString(variant.VariantWeight)
				vendorUPC = convertNoneToEmptyString(variant.VendorUPC)
				cost = convertNoneToEmptyString(variant.Cost)
				COGs = convertNoneToEmptyString(variant.COGs)
				outputCSV.write(f"{variant.VariantSKU},{variant.ProductSKUReference},{variant.Condition},{variant.VarTags},{variant.VariantSize},{variantPrice}," + '"'+variantImage+'"' + f",{vendorVariantColor},{variantColor},{variantSport},{variant.VariantSortOrder},{productLength},{GTIN},{MPN},{UPC},{variant.LowStockLevel},{variantHeight},{variantWidth},{variantDepth},{variantWeight},{variant.ERPBarcode},{variant.VariantColorWMT},{variant.ColorName},{variant.ImageRequired},{vendorUPC},{variant.ListingSKU},{cost},{COGs}\n")

	return inputDict

ensureOutputFolderExists(LOG_FOLDER_PATH)
#Create log files and write their initial headers:
validLogTypes = ["error", "missing-price", "modified-data-upload"]
for logType in validLogTypes:
	titleHeader = f"{logType.title()}s"#Create title case file name and its header.
	currentLogToCreate = f"{LOG_FOLDER_PATH}\{titleHeader}.txt"
	with open(currentLogToCreate, mode='w', newline='') as outputTXT:
		outputTXT.write(f"{titleHeader}:\n\n")
logging.basicConfig(filename=FULL_ERROR_REPORT_PATH, filemode='a', format='%(name)s - %(levelname)s - %(message)s')

def writeLog(content, logType="error"):
	"""Function to record all logs using the content param for output and logType param to determine which log to output to. If logType is default 'error', it prints the trackback to the error log."""
	global validLogTypes
	print(f"writeLog() called:\nType:{logType}\nContent:\n{content}")
	if logType == "error":
		logging.error("Exception occurred:\n\n", exc_info=True)
	elif logType in validLogTypes:
		titleHeader = f"{logType.title()}s"
		logToWrite = f"{LOG_FOLDER_PATH}\{titleHeader}.txt"
		with open(logToWrite, mode='a', newline='') as outputTXT:
			outputTXT.write(f"{content}\n")
	else:
		print(f"INVALID LOG TYPE: {logType}\n\n{content}")
		with open(FULL_ERROR_REPORT_PATH, mode='a', newline='') as outputTXT:
			outputTXT.write(f"INVALID LOG TYPE: {logType}\n\n{content}")
	return None

#DELETE when done testing:
PRODUCT_DESCRIPTIONS_OUTPUT_PATH = fr"{SHARED_DRIVE_PATH}\Python-Scripts\SAP_to_Sales_Layer_Data_Converter\Test_Data\SL-AI-Description-Instructions-and-AI-Generated-Product-Descriptions-{FILE_SYSTEM_DATE}-{TIME_OF_DAY}.csv"
AI_PRODUCT_CATEGORIZATION_OUTPUT_PATH = fr"{SHARED_DRIVE_PATH}\Python-Scripts\SAP_to_Sales_Layer_Data_Converter\Test_Data\SL-AI-Product-Category-Assignments-{FILE_SYSTEM_DATE}-{TIME_OF_DAY}.csv"
#Create AI output logs:
try:
	print("Creating AI Description Log Headers:")
	with open(PRODUCT_DESCRIPTIONS_OUTPUT_PATH, mode='w', newline='') as outputCSV:
			outputCSV.write(f"Product SKU,Product Name,Instructions Given to AI,Description Returned from AI\n")
except Exception as loggingError:
	print(f"Error creating AI log:\n{loggingError}")
	writeLog(loggingError, logType="error")

try:
	print("Creating AI Categorization Log Headers:")
	with open(AI_PRODUCT_CATEGORIZATION_OUTPUT_PATH, mode='w', newline='') as outputCSV:
			outputCSV.write(f"Product Name,Instructions Given to AI,Response Returned from AI,Product Name\n")
except Exception as loggingError:
	print(f"Error creating AI log:\n{loggingError}")
	writeLog(loggingError, logType="error")

def recordGeneratedProductDescriptionsToCSV(productSKU, productName, instructionsToAIForProductDescription, productDescription):
	""""""
	with open(PRODUCT_DESCRIPTIONS_OUTPUT_PATH, mode='a', newline='') as outputCSV:
			outputCSV.write(f"{productSKU},{productName}," + '"'+instructionsToAIForProductDescription+'"' + "," + '"'+productDescription+'"' + f",\n")
	return None

def recordGeneratedProductCategoriesToCSV(productSKU, promptForAICategoryChecker, generatedCategoryNames, productName):
	""""""
	csvOutput = f"{productSKU}," + '"'+promptForAICategoryChecker+'"' + "," + '"'+generatedCategoryNames+'"' + f",{productName},\n"
	#print(csvOutput)
	with open(AI_PRODUCT_CATEGORIZATION_OUTPUT_PATH, mode='a', newline='') as outputCSV:
		outputCSV.write(csvOutput)
	return None

def recordUploadedNewProductDataToTrackingSheet(dictOfNewUploadedSLProducts, dictOfNewSLVariants):
	""""""
	try:
		#Create temporary versions of the upload tracking sheets, add new product/variant info, and add info from existing tracking sheets if info has been online for less than 2 days.:
		temp_PRODUCT_UPLOAD_TRACKING_SHEET = NamedTemporaryFile(mode="w", newline="", delete=False)
		with temp_PRODUCT_UPLOAD_TRACKING_SHEET as trackProductUploadsCSV, open(PRODUCT_UPLOAD_TRACKING_SHEET, "r", encoding="utf8", errors="surrogateescape") as permanentProductUploadTrackingCSV:#Need 2nd open() as _ for permanent file?
			trackProductUploadsCSV.write(f"Product SKU,Price,Brand Name,Product Brand ID,Default Warehouse,Upload Date\n")
			listOfNewProductSKUs = dictOfNewUploadedSLProducts.keys()
			for uploadedProduct in dictOfNewUploadedSLProducts.items():
				productObject = uploadedProduct[1]#Each product dict item is a tuple, the SKU and the ojb: <class 'tuple'>: ('ARKN999333', <Product_Class.productClass object at 0x000002061509FF70>)
				trackProductUploadsCSV.write(f"{productObject.ProductSKU},{productObject.Price},{productObject.BrandName},{productObject.ProductBrandID},{productObject.DefaultWarehouse},{FILE_SYSTEM_DATE}\n")
			#Loop to add rows from previous uploaded products if date is less than 2 days old.
			permanentProductTrackingCSVReader = csv.DictReader(permanentProductUploadTrackingCSV)
			for row in permanentProductTrackingCSVReader:
				prodSKU = row["Product SKU"]
				prodPrice = row["Price"]
				prodBrand = row["Brand Name"]
				prodBrandID = row["Product Brand ID"]
				prodWH = row["Default Warehouse"]
				originalProdUploadDate = row["Upload Date"]
				prodUploadDate = datetime.datetime.strptime(originalProdUploadDate, "%m-%d-%y")#Get text of upload date from sheet and convert to datetime obj.
				timeProdHasBeenOnline = NOW - prodUploadDate
				daysProdHasBeenOnline = timeProdHasBeenOnline.days
				#If the product has been online for 2 or more days or is in the list of products uploaded, do not add row from permanent tracking sheet to temporary tracking sheet.
				if (prodSKU in listOfNewProductSKUs) or (daysProdHasBeenOnline > 2):
					print(f"Not adding {prodSKU} to the temporary tracking sheet.")
					continue
				else:
					print(f"Adding {prodSKU} to the temporary tracking sheet.")
					trackProductUploadsCSV.write(f"{prodSKU},{prodPrice},{prodBrand},{prodBrandID},{prodWH},{originalProdUploadDate}\n")
		shutil.move(temp_PRODUCT_UPLOAD_TRACKING_SHEET.name, PRODUCT_UPLOAD_TRACKING_SHEET)
		temp_VARIANT_UPLOAD_TRACKING_SHEET = NamedTemporaryFile(mode="w", newline="", delete=False)
		with temp_VARIANT_UPLOAD_TRACKING_SHEET as trackVariantUploadsCSV, open(VARIANT_UPLOAD_TRACKING_SHEET, "r", encoding="utf8", errors="surrogateescape") as permanentVariantUploadTrackingCSV:#Need 2nd open() as _ for permanent file?
			trackVariantUploadsCSV.write(f"Variant SKU,VendorUPC,Upload Date\n")
			#Need to: loop through dictOfNewSLVariants.items(), loop through each item's var obj list to get dictOfNewSLVariants.items()/[variantObj.VariantSKU] values
			#Nested list comprehension(s?): Create a list of just the Variant SKUs from each list of var objs in each item of the dict of new SL var info:
			listOfNewVariantSKUs = [variant.VariantSKU for varObjList in dictOfNewSLVariants.items() for variant in varObjList[1]]#varObjList is a tuple: (var parent SKU, [var obj,...])
			print(f"listOfNewVariantSKUs: {listOfNewVariantSKUs}")
			for uploadedProductVariantList in dictOfNewSLVariants.items():
				listOfVariantObjects = uploadedProductVariantList[1]#A tuple of the product SKU reference/list of variant obj: ('ARKN999333', [<Variant_Class.variantClass object at 0x000001AEDF46CA90>])
				print(f"{type(listOfVariantObjects)}: {listOfVariantObjects}")
				for variantObj in listOfVariantObjects:
					print(f"{type(variantObj)}: {variantObj}")
					trackVariantUploadsCSV.write(f"{variantObj.VariantSKU},{variantObj.VendorUPC},{FILE_SYSTEM_DATE}\n")
			#Loop to add rows from previous uploaded variants if date is less than 2 days old..
			permanentVariantTrackingCSVReader = csv.DictReader(permanentVariantUploadTrackingCSV)
			for row in permanentVariantTrackingCSVReader:
				varSKU = row["Variant SKU"]
				varVendorUPC = row["VendorUPC"]
				originalVarUploadDate = row["Upload Date"]
				varUploadDate = datetime.datetime.strptime(originalVarUploadDate, "%m-%d-%y")#Get text of upload date from sheet and convert to datetime obj.
				timeVarHasBeenOnline = NOW - varUploadDate
				daysVarHasBeenOnline = timeVarHasBeenOnline.days
				#If the variant has been online for 2 or more days or is in the list of variants uploaded, do not add row from permanent tracking sheet to temporary tracking sheet.
				if (varSKU in listOfNewVariantSKUs) or (daysVarHasBeenOnline > 2):
					print(f"Not adding {varSKU} to the temporary tracking sheet.")
					continue
				else:
					print(f"Adding {varSKU} to the temporary tracking sheet.")
					trackVariantUploadsCSV.write(f"{varSKU},{varVendorUPC},{originalVarUploadDate}\n")
		shutil.move(temp_VARIANT_UPLOAD_TRACKING_SHEET.name, VARIANT_UPLOAD_TRACKING_SHEET)
	except Exception as productUploadTrackingError:
		print(f"Error updating product tracking log:\n{productUploadTrackingError}")
		writeLog(productUploadTrackingError, logType="error")
	return None

def recordUploadedModifiedProductDataToTrackingSheet(dictOfModifiedUploadedToSLProducts, dictOfModifiedSLVariants):
	""""""
	try:
		temp_PRODUCT_UPLOAD_TRACKING_SHEET = NamedTemporaryFile(mode="w", newline="", delete=False)
		with temp_PRODUCT_UPLOAD_TRACKING_SHEET as trackProductUploadsCSV, open(PRODUCT_UPLOAD_TRACKING_SHEET, "r", encoding="utf8", errors="surrogateescape") as permanentProductUploadTrackingCSV:#Need 2nd open() as _ for permanent file?
			trackProductUploadsCSV.write(f"Product SKU,Price,Brand Name,Product Brand ID,Default Warehouse,Upload Date\n")
			listOfModifiedProductSKUs = dictOfModifiedUploadedToSLProducts.keys()
			#Loop to add rows from previous uploaded products (with updated data if needed).
			permanentProductTrackingCSVReader = csv.DictReader(permanentProductUploadTrackingCSV)
			for row in permanentProductTrackingCSVReader:
				prodSKU = row["Product SKU"]
				productHasBeenModified = bool(prodSKU in listOfModifiedProductSKUs) #Checks if product has been modified.
				#Add orginal values if unchanged, else the new, uploaded value.
				prodPrice = row["Price"] if not productHasBeenModified else dictOfModifiedUploadedToSLProducts[prodSKU]["Price"]
				prodBrand = row["Brand Name"] if not productHasBeenModified else dictOfModifiedUploadedToSLProducts[prodSKU]["Brand Name"]
				prodBrandID = row["Product Brand ID"] if not productHasBeenModified else dictOfModifiedUploadedToSLProducts[prodSKU]["Product Brand ID"]
				prodWH = row["Default Warehouse"] if not productHasBeenModified else dictOfModifiedUploadedToSLProducts[prodSKU]["Default Warehouse"]
				originalProdUploadDate = row["Upload Date"]
				trackProductUploadsCSV.write(f"{prodSKU},{prodPrice},{prodBrand},{prodBrandID},{prodWH},{originalProdUploadDate}\n")
		shutil.move(temp_PRODUCT_UPLOAD_TRACKING_SHEET.name, PRODUCT_UPLOAD_TRACKING_SHEET)
		temp_VARIANT_UPLOAD_TRACKING_SHEET = NamedTemporaryFile(mode="w", newline="", delete=False)
		with temp_VARIANT_UPLOAD_TRACKING_SHEET as trackVariantUploadsCSV, open(VARIANT_UPLOAD_TRACKING_SHEET, "r", encoding="utf8", errors="surrogateescape") as permanentVariantUploadTrackingCSV:#Need 2nd open() as _ for permanent file?
			trackVariantUploadsCSV.write(f"Variant SKU,VendorUPC,Upload Date\n")
			listOfModifiedVariantSKUs = dictOfModifiedSLVariants.keys()
			print(f"listOfModifiedVariantSKUs: {listOfModifiedVariantSKUs}")
			permanentVariantTrackingCSVReader = csv.DictReader(permanentVariantUploadTrackingCSV)
			for row in permanentVariantTrackingCSVReader:
				varSKU = row["Variant SKU"]
				variantHasBeenModified = bool(varSKU in listOfModifiedVariantSKUs)
				varVendorUPC = row["VendorUPC"] if not variantHasBeenModified else dictOfModifiedSLVariants[varSKU]["VendorUPC"]
				originalVarUploadDate = row["Upload Date"]
				trackVariantUploadsCSV.write(f"{varSKU},{varVendorUPC},{originalVarUploadDate}\n")
		shutil.move(temp_VARIANT_UPLOAD_TRACKING_SHEET.name, VARIANT_UPLOAD_TRACKING_SHEET)
	except Exception as productUploadTrackingError:
		print(f"Error updating product tracking log:\n{productUploadTrackingError}")
		writeLog(productUploadTrackingError, logType="error")
	return None

def recordModifiedDataUploadToLog():
	"""Turns list of modified product and variant SKUs from constants, converts each to a string that lists each SKU on new line, then writes both strings to the log"""
	
	modifiedProductContent = "\n".join(RECENTLY_MODIFIED_PRODUCTS.keys())
	modifiedVariantContent = "\n".join(RECENTLY_MODIFIED_VARIANTS.keys())
	modifiedDataContent = f"Recently Modified Products Uploaded:\n{modifiedProductContent}\n\nRecently Modified Variants Uploaded:\n{modifiedVariantContent}"
	writeLog(modifiedDataContent, logType="modified-data-upload")
	print(modifiedDataContent)
	return None

if __name__ == "__main__":
	testInputFile = fr"{SHARED_DRIVE_PATH}\Python-Scripts\SAP_to_Sales_Layer_Data_Converter\Test_Data\Small-Post-Col-Update-SAP-Product-Data.csv"
	testFunc = readSAPDataCSV
	#Read SAP export test:
	testOutput = readCSV(testInputFile, testFunc)
	print(type(testOutput), testOutput, "\n", sep="\n")
	#Assemble SAP export data for processing test:
	testAssembledSAPData = assembleProductData(testOutput)
	print(type(testAssembledSAPData), testAssembledSAPData, sep="\t")
	origPrice = "50.01"
	testProduct = productClass("ARKM100282", "Mens>Outerwear", "Arkansas Razorbacks Take Your Time 1/4 Zip Windshirt", "Men|Outerwear|Pullovers|All Outerwear,PRODUCT|All Product|New Arrivals|All Outerwear", "MENS01,MENS03,MEOU01,OUTER,PRODUCT,ALL,NEWA01,OUTER", "", "ARK", origPrice, "", "0", "ARKM100282.jpg", "Colosseum", "26", "Adult", "Men", "No", "True", "SP23", "Wiffle Ball", "False", "", "", "", "", "", "", "", "", "NationalWiffleBallPlayOffs", "", "", "Imported", "WSD", "", "", "0", "16.0", "Default Tax Class", "PC040100", "Default Tax Class", "", "", "2", "", "", "", "", "V500027", "COUZ11523W", "Mens", "LONG SLEEVE", "MENS", "", "Variant", "arkansas-razorbacks-take-your-time-1-4-zip-windshirt-ARKM100282", "Fleece, pullover, sweats, hoodie, windshirt, sweatshirt, wind shirt, sweat shirt, pull over, 1/4 zip, quarter zip, Shep Shirt, Shepshirt, Colosseum", ",New,White,Men,Adult", "Age>Adult;Gender>Men;Color>White;Origin>Imported", "07/15/22", "20.70", "Yes", True, True, ["999"], True, ["XS", "S", "M", "L", "XL", "2XL"], ["Multi"], "TestProductLineName")
	testProductDict = {"ARKM100282": testProduct}
	for prodSKU, Product in testProductDict.items():
		print(f"{prodSKU}: {Product}")
	testSLProdOutputFile = fr"{SHARED_DRIVE_PATH}\HTML_and_Source_Code\Python_Scripts\SAP_to_Sales_Layer_Data_Converter\Test_Data\Test-Sales-Layer-Product-Import-Sheet.csv"
	writeSalesLayerProductImportSheet(testProductDict, testSLProdOutputFile)
	testVariant = variantClass("ARKM010968-698-S", "ARKM010968", "Visible", "ARK", "S", "", "", "", "698", "", "", None, "ARK-T5-10712", None, "", "1", "", "", "", "", "092275313480", "698", "Red", "False", "", "")
	testVariantList = [testVariant]
	testVariantDict = {"ARKM010968-698-S": testVariantList}
	for varSKU, variant in testVariantDict.items():
		print(f"{varSKU}: {variant}")
	testSLVarOutputFile = fr"{SHARED_DRIVE_PATH}\Python-Scripts\SAP_to_Sales_Layer_Data_Converter\Test_Data\Test-Sales-Layer-Variant-Import-Sheet.csv"
	writeSalesLayerVariantImportSheet(testVariantDict, testSLVarOutputFile)
