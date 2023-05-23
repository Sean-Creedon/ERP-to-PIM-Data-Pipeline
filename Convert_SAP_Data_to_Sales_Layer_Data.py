#!/usr/bin/env python3
#This is the entry point script/main file for running the SAP_to_Sales_Layer_Data_Converter.
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

#09/09/22
#Products need to get color list from variants obj
#Need to read existing prod & var info and match to new var; will need to update prod info (color list) and var info (retroactively set existing vars to img req).
#Var need img req set.
#Add img info to prod & var objs.

def runSAPDataToSalesLayerDataConversion(inputFile, outputPath):
	""""""
	
	##
	#Read PRODUCT_UPLOAD_TRACKING_SHEET & VARIANT_UPLOAD_TRACKING_SHEET and load into "tracking dicts" here.
	##

	#ensureOutputFolderExists(OUTPUT_FOLDER_PATH)#This path will be a folder at Box\eCommerce Product Uploads\MM-DD-YY named after current date.
	#Read SAP export test:
	dataFromSAP = readCSV(inputFile, readSAPDataCSV)
	dictOfSAPData = assembleProductData(dataFromSAP)
	#print("\ndictOfSAPData:", type(dictOfSAPData), dictOfSAPData, "\n", sep="\t")
	#09/12/22 Consolidated funcs for reading SAPData for dicts of SL product and variant data:
	dictOfSLProduct, dictOfSLVariant = generateDictsOfSLProductsAndVariants(dictOfSAPData)
	#print("\ndictOfSLVariant:", type(dictOfSLVariant), dictOfSLVariant, "\n", sep="\t")
	#Create subfolder for images in output folder:
	imagesOutputSubfolder = ensureImageSubFolderExists(outputPath)
	imageZipToUpload = fr"{imagesOutputSubfolder}\Image-Zip-File-Name-Placeholder.zip"
	dictOfAllMatchingProductImages, dictOfVariantImages, listOfProductSKUsMissingImg, listOfVariantSKUsMissingRequiredImg = findProductAndVariantImages(dictOfSLProduct, dictOfSLVariant, imageZipToUpload)
	#print("\n\ndictOfAllMatchingProductImages:", dictOfAllMatchingProductImages, "dictOfVariantImages:", dictOfVariantImages, "listOfProductSKUsMissingImg:", listOfProductSKUsMissingImg, "listOfVariantSKUsMissingRequiredImg:", listOfVariantSKUsMissingRequiredImg, "imageZipToUpload:", imageZipToUpload, sep = "\n\n")
	dictOfSLProduct = mergeSLProductDataWithMatchingProductImagesDict(dictOfSLProduct, dictOfAllMatchingProductImages)
	dictOfSLVariant = mergeSLVariantDataWithMatchingVariantImagesDict(dictOfSLVariant, dictOfVariantImages)
	#Put Both SL prod and var csv write funcs in one func. . .
	writeSalesLayerProductImportSheet(dictOfSLProduct, f"{outputPath}\Test-Sales-Layer-Product-Import-Sheet.csv")#Replace 2nd param after testing: FULL_SALESLAYER_PRODUCT_IMPORT_PATH
	writeSalesLayerVariantImportSheet(dictOfSLVariant, f"{outputPath}\Test-Sales-Layer-Variant-Import-Sheet.csv")#Replace 2nd param after testing: FULL_SALESLAYER_VARIANT_IMPORT_PATH
	uploadNewDataToSalesLayerAPI(dictOfSLProduct, dictOfSLVariant)
	#Record uploaded products and variants for tracking purposes:
	recordUploadedNewProductDataToTrackingSheet(dictOfSLProduct, dictOfSLVariant)
	#Add modified prod upload here.
	#Test if there are any modified products or variants, upload if needed:
	if ( bool(RECENTLY_MODIFIED_PRODUCTS) ) or ( bool(RECENTLY_MODIFIED_VARIANTS) ):
		uploadModifiedDataToSalesLayerAPI(RECENTLY_MODIFIED_PRODUCTS, RECENTLY_MODIFIED_VARIANTS)
		recordUploadedModifiedProductDataToTrackingSheet(RECENTLY_MODIFIED_PRODUCTS, RECENTLY_MODIFIED_VARIANTS)
		recordModifiedDataUploadToLog()
	return dictOfSLProduct, dictOfSLVariant, imageZipToUpload, listOfProductSKUsMissingImg, listOfVariantSKUsMissingRequiredImg



if __name__ == "__main__":
	testOutputPath = fr"C:\REDACTED\Test_Data"
	runSAPDataToSalesLayerDataConversion(testInputFile, testOutputPath)
	print(f"\n\nRECENTLY_UPLOADED_PRODUCTS: {RECENTLY_UPLOADED_PRODUCTS}\n\nRECENTLY_UPLOADED_VARIANTS: {RECENTLY_UPLOADED_VARIANTS}\n\n")
	print(f"\n\nRECENTLY_MODIFIED_PRODUCTS: {RECENTLY_MODIFIED_PRODUCTS}\n\nRECENTLY_MODIFIED_VARIANTS: {RECENTLY_MODIFIED_VARIANTS}\n\n")