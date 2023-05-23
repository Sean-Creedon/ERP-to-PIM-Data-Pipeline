import requests
from requests.exceptions import HTTPError
import random, hashlib, time
from Constants import *
from SAP_Data_Class import *
from Product_Class import *
from Variant_Class import *
from File_Read_and_Write_Functions import *
from File_Read_and_Write_Functions import convertListForCSV

############
#Add New Product & Variants:
#Example imput:
#newData = [productData, variantData]

def addDataToNewProdJSON(product):
	"""Receives Sales Layer Product object and adds its various attributes to the Sales Layer product JSON. For new product info."""
	print("product", product, type(product))
	try:
		newProductDict = {"Product SKU": product.ProductSKU}
		print("newProductDict", newProductDict, type(newProductDict))
		if bool(product.Family): newProductDict.update({"Family": product.Family})
		if bool(product.ProductName): newProductDict.update({"Product Name": product.ProductName})
		if bool(product.Category): newProductDict.update({"Category": product.Category})
		if bool(product.ProductDescription): newProductDict.update({"Product Description": product.ProductDescription})
		if bool(product.ProdTags): newProductDict.update({"Tags": product.ProdTags})
		#print("product.Price", product.Price, type(product.Price))
		newProductDict.update({"Price": product.Price}) if bool(product.Price) else writeLog(f"MISSING PRICE: {product.ProductSKU}\n", logType="missing-price")
		#If prod/var has images, convert lst data to comma-separated string of file names:
		if bool(product.ProductImages): newProductDict.update({"Product Images": convertListForCSV(product.ProductImages)})
		if bool(product.BrandName): newProductDict.update({"Brand Name": product.BrandName})
		if bool(product.ProductBrandID): newProductDict.update({"Product Brand ID": product.ProductBrandID})
		if bool(product.AgeGroup): newProductDict.update({"Age Group": product.AgeGroup})
		if bool(product.Gender): newProductDict.update({"Gender": product.Gender})
		if bool(product.IsUnisex): newProductDict.update({"Is Unisex?": product.IsUnisex})
		if bool(product.IsLicensed): newProductDict.update({"Is Licensed": product.IsLicensed})
		if bool(product.Season): newProductDict.update({"Season": product.Season})
		if bool(product.Sport): newProductDict.update({"Sport": product.Sport})
		if bool(product.Memorabilia): newProductDict.update({"Memorabilia": product.Memorabilia})
		if bool(product.PlayerName): newProductDict.update({"Player Name": product.PlayerName})
		if bool(product.EventCollection): newProductDict.update({"Event/Collection": product.EventCollection})
		if bool(product.SportsTeam): newProductDict.update({"Sports Team": product.SportsTeam})
		if bool(product.CountryofOrigin): newProductDict.update({"Country of Origin": product.CountryofOrigin})
		if bool(product.DefaultWarehouse): newProductDict.update({"Default Warehouse": product.DefaultWarehouse})
		if bool(product.FixedShippingCost): newProductDict.update({"Fixed Shipping Cost": product.FixedShippingCost})
		newProductDict.update({"Free Shipping": "0"}) if bool(product.FreeShipping) else newProductDict.update({"Free Shipping": "1"}) #Defaults to False as of 12/12/22 (hence the use of "if not"/"short-circuit" evaluation).
		if bool(product.ProductWeight): newProductDict.update({"Product Weight (oz)": product.ProductWeight})
		if bool(product.TaxLiable): newProductDict.update({"Tax Liable": product.TaxLiable})
		if bool(product.AvaTaxCode): newProductDict.update({"AvaTax Code": product.AvaTaxCode})
		if bool(product.ProductTaxClass): newProductDict.update({"Product Tax Class": product.ProductTaxClass})
		if bool(product.PreviouseCommNumber): newProductDict.update({"Previous eComm Number": product.PreviouseCommNumber})
		if bool(product.ProductLineCode): newProductDict.update({"Product Line Code": product.ProductLineCode})
		if bool(product.PreferredVendor): newProductDict.update({"Preferred Vendor": product.PreferredVendor})
		if bool(product.ForeignName): newProductDict.update({"Foreign Name": product.ForeignName})
		if bool(product.ItemGroup): newProductDict.update({"Item Group": product.ItemGroup})
		if bool(product.ItemType): newProductDict.update({"Item Type": product.ItemType})
		if bool(product.Division): newProductDict.update({"Division": product.Division})
		if bool(product.AllowPurchases): newProductDict.update({"Allow Purchases": product.AllowPurchases})
		if bool(product.TrackInventory): newProductDict.update({"Track Inventory": product.TrackInventory})
		if bool(product.Handle): newProductDict.update({"Handle": product.Handle})
		if bool(product.Keywords): newProductDict.update({"Keywords": product.Keywords})
		if bool(product.WMTTags): newProductDict.update({"WMT Tags": product.WMTTags})
		if bool(product.Filters): newProductDict.update({"Filters": product.Filters})
		if bool(product.CreatedDate): newProductDict.update({"Created Date": product.CreatedDate})
		if bool(product.COGS): newProductDict.update({"COGS": product.COGS})
		newProductDict.update({"Discounts & Promotions Applicable":  "Yes"}) if bool(product.DiscountsAndPromotionsApplicable) else newProductDict.update({"Discounts & Promotions Applicable":  "No"})
		#print("newProductDict:", newProductDict, type(newProductDict))
		SALESLAYER_NEW_PRODUCT_JSON["input_data"]["products"].append(newProductDict)
		#print("SALESLAYER_NEW_PRODUCT_JSON after adding product:", SALESLAYER_NEW_PRODUCT_JSON, type(SALESLAYER_NEW_PRODUCT_JSON))
	except Exception as addProdDataToJSONError:
		#print(f"addDataToNewProdJSON encountered an error:\n{addProdDataToJSONError}")
		writeLog(addProdDataToJSONError, logType="error")
	else:
		#print(f"New product data:\n{newProductDict}")
		return SALESLAYER_NEW_PRODUCT_JSON

def addDataToNewVarJSON(variant):
	"""Receives Sales Layer Variant object and adds its various attributes to the Sales Layer product JSON. For new variant info."""
	#print(variant, type(variant))
	try:
		newVariantDict = {"Variant SKU": variant.VariantSKU}
		if bool(variant.ProductSKUReference): newVariantDict.update({"Product SKU Reference": variant.ProductSKUReference})
		if bool(variant.Condition): newVariantDict.update({"Condition": variant.Condition})
		if bool(variant.VarTags): newVariantDict.update({"Tags": variant.VarTags})
		if bool(variant.VariantSize): newVariantDict.update({"Variant Size": variant.VariantSize})
		#if bool(variant.VariantPrice): newVariantDict.update({"Variant Price": variant.VariantPrice})
		#print("variant.VariantPrice", variant.VariantPrice, type(variant.VariantPrice))
		newVariantDict.update({"Variant Price": variant.VariantPrice}) if bool(variant.VariantPrice)  else ""
		#If prod/var has images, convert lst data to comma-separated string of file names:
		if bool(variant.VariantImage): newVariantDict.update({"Variant Image": convertListForCSV(variant.VariantImage)})
		if bool(variant.VendorVariantColor): newVariantDict.update({"Vendor Variant Color": variant.VendorVariantColor})
		if bool(variant.VariantColor): newVariantDict.update({"Variant Color": variant.VariantColor})
		if bool(variant.VariantSport): newVariantDict.update({"Variant Sport": variant.VariantSport})
		if bool(variant.ProductLength): newVariantDict.update({"Variant Sort Order": variant.ProductLength})
		if bool(variant.GTIN): newVariantDict.update({"GTIN": variant.GTIN})
		if bool(variant.MPN): newVariantDict.update({"MPN": variant.MPN})
		if bool(variant.UPC): newVariantDict.update({"UPC": variant.UPC})
		if bool(variant.LowStockLevel): newVariantDict.update({"Low Stock Level":  variant.LowStockLevel})
		if bool(variant.VariantHeight): newVariantDict.update({"Variant Height (3)": variant.VariantHeight})
		if bool(variant.VariantWidth): newVariantDict.update({"Variant Width (3)": variant.VariantWidth})
		if bool(variant.VariantDepth): newVariantDict.update({"Variant Depth (3)": variant.VariantDepth})
		#Variant weight set in code, just not uploaded at this time. Value is just product weight as of 12/29/22 (not true variant shipping weight).
		#if bool(variant.VariantWeight): newVariantDict.update({"Variant Weight (3)": variant.VariantWeight})
		if bool(variant.ERPBarcode): newVariantDict.update({"ERP Barcode": variant.ERPBarcode})
		if bool(variant.VariantColorWMT): newVariantDict.update({"Variant Color (WMT)": variant.VariantColorWMT})
		if bool(variant.ColorName): newVariantDict.update({"Color Name": variant.ColorName})
		if bool(variant.ImageRequired): newVariantDict.update({"Image Required": variant.ImageRequired})
		if bool(variant.VendorUPC): newVariantDict.update({"VendorUPC": variant.VendorUPC})
		if bool(variant.ListingSKU): newVariantDict.update({"ListingSKU": variant.ListingSKU})
		if bool(variant.Cost): newVariantDict.update({"Cost": variant.Cost})
		if bool(variant.COGs): newVariantDict.update({"COGs": variant.COGs})
		#print("newProductDict:", newVariantDict, type(newProductDict))
		SALESLAYER_NEW_PRODUCT_JSON["input_data"]["variants"].append(newVariantDict)
		#print("SALESLAYER_NEW_PRODUCT_JSON after adding variant:", SALESLAYER_NEW_PRODUCT_JSON, type(SALESLAYER_NEW_PRODUCT_JSON))
	except Exception as addVarDataToJSONError:
		print(f"addDataToNewVarJSON encountered an error:\n{addVarDataToJSONError}")
		writeLog(addVarDataToJSONError, logType="error")
	else:
		#print(f"New variant data:\n{newVariantDict}")
		return SALESLAYER_NEW_PRODUCT_JSON

def addAllNewDataToJSON(newProductDict, newVariantDict):
	"""Loops through values of newProductDict & newVariantDict. Calls addDataToNewProdJSON() & addDataToNewVarJSON () on the respective values."""
	#Loops through the SL prod/var obj dicts and adds to JSON for SL upload. For new product data (not updated).
	for product in newProductDict.values():
		addDataToNewProdJSON(product)
	for variantList in newVariantDict.values():
		#print(variantList, type(variantList))
		for variant in variantList:
			#print(variant, type(variant))
			addDataToNewVarJSON(variant)
	return newProductDict, newVariantDict

def addDataToUpdatedProdJSON(modifiedProductDict):
	"""Receives Sales Layer Product object and adds its various attributes to the Sales Layer product JSON. For updated product info."""
	print("modifiedProductDict: ", modifiedProductDict, type(modifiedProductDict), sep="\t")
	try:
		SALESLAYER_MODIFY_PRODUCT_JSON["input_data"]["products"].append(modifiedProductDict)
		print(f"SALESLAYER_MODIFY_PRODUCT_JSON: {SALESLAYER_MODIFY_PRODUCT_JSON}")
	except Exception as addProdDataToUpdateJSONError:
		print(f"addDataToUpdatedProdJSON() encountered an error:\n{addProdDataToUpdateJSONError}")
		writeLog(addProdDataToUpdateJSONError, logType="error")
	else:
		return SALESLAYER_MODIFY_PRODUCT_JSON
 
def addDataToUpdatedVarJSON(variant):
	"""Receives Sales Layer Variant object and adds its various attributes to the Sales Layer product JSON. For updated variant info."""
	print("addDataToUpdatedVarJSON:", variant, type(variant))
	try:
		SALESLAYER_MODIFY_PRODUCT_JSON["input_data"]["variants"].append(variant)
	except Exception as addDataToUpdateVarJSON:
		print(f"addDataToUpdatedVarJSON() encountered an error:\n{addDataToUpdateVarJSON}")
		writeLog(addDataToUpdateVarJSON, logType="error")
	else:
		print(f"SALESLAYER_MODIFY_PRODUCT_JSON:\n{SALESLAYER_MODIFY_PRODUCT_JSON}")
		return SALESLAYER_MODIFY_PRODUCT_JSON

def addAllUpdatedDataToJSON(updatedProductDict, updatedVariantDict):
	"""Loops through values of updatedProductDict & updatedVariantDict. Calls addDataToUpdatedProdJSON() & addDataToUpdatedVarJSON () on the respective values."""
	#First test if the dict is empty before looping. Remove nested dict from SL's input_json if empty.
	#Loops through the SL prod/var obj dicts and adds to JSON for SL upload. For modified product data.
	if bool(updatedProductDict):
		for product in updatedProductDict.values():
			addDataToUpdatedProdJSON(product)
	else:
		SALESLAYER_MODIFY_PRODUCT_JSON["input_data"].pop("products")
	if bool(updatedVariantDict):
		for variant in updatedVariantDict.values():
			addDataToUpdatedVarJSON(variant)
	else:
		SALESLAYER_MODIFY_PRODUCT_JSON["input_data"].pop("variants")
	return updatedProductDict, updatedVariantDict

def addConnectionInfo(tableName, tableConnectorIDcode, tableChannelPrivateKey):
	"""Takes table name and autherizations, generates SHA256 code and adds info to put request message body."""
	#print(f"tableConnectorIDcode: {tableConnectorIDcode}, {type(tableConnectorIDcode)}")
	#print(f"tableChannelPrivateKey: {tableChannelPrivateKey}, {type(tableChannelPrivateKey)}")
	internationalUnixTime = str(time.time())
	randomNumber = str(random.randrange(1, 100))
	key = f"{tableConnectorIDcode}{tableChannelPrivateKey}{internationalUnixTime}{randomNumber}"
	hashedKey = hashlib.sha256(key.encode())
	#print(hashedKey)
	hexKey = hashedKey.hexdigest()
	#print(hexKey)
	#print(f"tableName: {tableName}, {type(tableName)}")
	tableName["code"] = tableConnectorIDcode
	tableName["time"] = internationalUnixTime
	tableName["unique"] = randomNumber
	tableName["key256"] = hexKey
	tableName["input_data_directly"] = True 
	return tableName


def postNewDataToSalesLayerAPI(newData):
	""""""
	print(f"newData: {newData}", type(newData))
	try:
		print(newData, type(newData))
		#print("Modifying Data")
		#dataset = addConnectionInfo(dataset, MODIFY_PRODUCT_CONNECTOR_ID_CODE, MODIFY_PRODUCT_CHANNEL_PRIVATE_KEY)
		print("Uploading New Data")
		newData = addConnectionInfo(newData, NEW_PRODUCT_CONNECTOR_ID_CODE, NEW_PRODUCT_CHANNEL_PRIVATE_KEY)
		postResponse = requests.post(SALESLAYER_URL, json=newData)
		# If the responses were successful, no Exception will be raised
		postResponse.raise_for_status()
	except HTTPError as http_err:
		print(f'HTTP error occurred: {http_err}')
		writeLog(http_err, logType="error")
	except Exception as otherSLAPINewDataUploadError:
		print(f'Other error occurred: {otherSLAPINewDataUploadError}')
		writeLog(otherSLAPINewDataUploadError, logType="error")
	else:
		print(f"Success: Request to {SALESLAYER_URL} returned status code {postResponse.status_code}.")
		#print(postResponse.headers)
		print(postResponse.json())
	return newData, postResponse

def uploadNewDataToSalesLayerAPI(newProductDict, newVariantDict):
	""""""
	addAllNewDataToJSON(newProductDict, newVariantDict)
	if bool(SALESLAYER_NEW_PRODUCT_JSON):
		postNewDataToSalesLayerAPI(SALESLAYER_NEW_PRODUCT_JSON)
	return newProductDict, newVariantDict


def postModifiedDataToSalesLayerAPI(modifiedData):
	""""""
	print(f"modifiedData: {modifiedData}", type(modifiedData))
	try:
		print(modifiedData, type(modifiedData))
		#print("Modifying Data")
		#dataset = addConnectionInfo(dataset, MODIFY_PRODUCT_CONNECTOR_ID_CODE, MODIFY_PRODUCT_CHANNEL_PRIVATE_KEY)
		print("Uploading Modified Data")
		modifiedData = addConnectionInfo(modifiedData, MODIFY_PRODUCT_CONNECTOR_ID_CODE, MODIFY_PRODUCT_CHANNEL_PRIVATE_KEY)
		postResponse = requests.post(SALESLAYER_URL, json=modifiedData)
		# If the responses were successful, no Exception will be raised
		postResponse.raise_for_status()
	except HTTPError as http_err:
		print(f'HTTP error occurred: {http_err}')
		writeLog(http_err, logType="error")
	except Exception as otherSLAPIModifiedDataUploadError:
		print(f'Other error occurred: {otherSLAPIModifiedDataUploadError}')
		writeLog(otherSLAPIModifiedDataUploadError, logType="error")
	else:
		print(f"Success: Request to {SALESLAYER_URL} returned status code {postResponse.status_code}.")
		#print(postResponse.headers)
		print(postResponse.json())
	return modifiedData, postResponse

def uploadModifiedDataToSalesLayerAPI(modifiedProductDict, modifiedVariantDict):
	""""""
	#Need to completely replace addAllUpdatedDataToJSON func def:
	addAllUpdatedDataToJSON(modifiedProductDict, modifiedVariantDict)
	if bool(SALESLAYER_MODIFY_PRODUCT_JSON):
		postModifiedDataToSalesLayerAPI(SALESLAYER_MODIFY_PRODUCT_JSON)
	return modifiedProductDict, modifiedVariantDict