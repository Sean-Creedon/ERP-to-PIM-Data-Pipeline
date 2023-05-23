#!/usr/bin/env python3
import re, os, zipfile
from pathlib import Path
from Variant_Class import *
from Variant_Class_Methods import *
from Product_Class import *
from Product_Class_Methods import *
print("Deactivate Product and Variant class imports; only needed for testing.")
from Constants import *

#Search SL img info export with prod SKU list:
#match img to prods, build indices of matched img & unmatched prod (update SL prod img info)
#filter for POD pk-a-sprt images
#Repeat same search on file system, build index of matched img to zip & update unmatched img index (update SL prod img info)
#Use index of matched img to update SL var img info where img required

####To Do:
#Add func to order img according to keywords in file name: 'LCFH010118-423-OSFM back-1.jpg', 'LCFH010118-423-OSFM front-1.jpg'
####

def ensureImageSubFolderExists(folderToCheck):
	"""Checks for the existence of the folder path given as input and creates it if needed."""
	subFolderToCheck =  fr"{folderToCheck}\Images"
	if not os.path.exists(subFolderToCheck):
		os.makedirs(subFolderToCheck)
	return subFolderToCheck

def searchSLImgInfoExportForProductImages(productSKU):
	"""Search list of image file names in Sales Layer image info export for matches to a product SKU. Returns a list of matching files."""
	#Use list comp to loop through list of images & check each image for prod SKU text.
	matchingSLProductImageList = [image for image in SL_UPLOADED_IMAGE_FILE_LIST if productSKU in image]
	return matchingSLProductImageList

def generateDictOfMatchingSLProductImages(productSKUList):
	"""Performs searchSLImgInfoExportForProductImages() func on list of product SKUs, returns dict of product SKU keys/list of matching images values and list of products without matches."""
	#Sample return value for [LCFH010118, AUB-MT0001-AUB-LAG891, MUON012270] as input param:
	#{'LCFH010118': ['LCFH010118-423_2.jpg', 'LCFH010118-423_3.jpg'...], 'AUB-MT0001-AUB-LAG891': ['AUB-MT0001-AUB-LAG891-100_3.jpg'], 'MUON012270': []}
	dictOfMatchingSLProductImages = {}
	prodSKUsWithoutImages = []
	for prodSKU in productSKUList:
		dictOfMatchingSLProductImages[prodSKU] = searchSLImgInfoExportForProductImages(prodSKU)
		if not bool(dictOfMatchingSLProductImages[prodSKU]):
			prodSKUsWithoutImages.append(prodSKU)
	return dictOfMatchingSLProductImages, prodSKUsWithoutImages

def searchFileSystemForProductImages(productSKU):
	"""Search list of file system images for matches to a product SKU. Returns lists of matching file name & paths for zipping/importing to SL & to add to product data plus list of unmatched SKUs."""
	matchingFileSystemProductImageList = [image for image in FILE_SYSTEM_IMAGES if productSKU in image]
	matchingFileSystemProductImagePathList = [imagePath for imagePath in FILE_SYSTEM_IMG_PATHS if productSKU in imagePath]
	return matchingFileSystemProductImageList, matchingFileSystemProductImagePathList

##Need to loop through a prod SKU list, run func above on each SKU, and return:
#Dict of prod SKU keys, matching images list (for prod data/just file names).
#Appended list of matching product image paths to zip/archive.
def generateDictOfMatchingFileSystemProductImages(prodSKUsWithoutImages):
	"""Loops over list of product SKUs still missing images and searches file system to generates/returns list of images to zip, dict with product SKU keys/matching file system images list values. Also returns updated list of products without images."""
	dictOfMatchingFileProductImages = {}
	listOfImageFilesToZip = []
	for prodSKU in prodSKUsWithoutImages:##Update dict of matching img names from SL img search (just need file names for data)?
		dictOfMatchingFileProductImages[prodSKU], listOfProductImagePaths = searchFileSystemForProductImages(prodSKU)
		listOfImageFilesToZip.extend(listOfProductImagePaths)
		if bool(dictOfMatchingFileProductImages[prodSKU]):
			prodSKUsWithoutImages.remove(prodSKU)
	return prodSKUsWithoutImages, dictOfMatchingFileProductImages, listOfImageFilesToZip

def zipMatchingProductImages(listOfImagePaths, zipFileOutputPath):
	"""Loops through list of matching product images/1st param, zips the files into an archive with the name/location given as 2nd param"""
	#1st param example: ['C:\\Users\\Sean Creedon\\Box\\Web Ready Photography\\LCFH010118-423-OSFM angle 1-1.jpg', 'C:\\Users\\Sean Creedon\\Box\\Web Ready Photography\\LCFH010118-423-OSFM angle 2-1.jpg',...]
	#2nd param example: "C:\Users\Sean Creedon\OneDrive - Dyehard Fan Supply\Downloads\08-03-22\testZipArchive.zip"
	if not bool(listOfImagePaths):
		return None
	try:
		with zipfile.ZipFile(zipFileOutputPath, mode="w") as zipArchive:
			for filePath in listOfImagePaths:
				fileName = Path(filePath).name
				zipArchive.write(filePath, fileName)#Zip from the full filePath, to the zipFileOutputPath, but don't "copy" filePath directory structures (just fileName.name).
	except Exception as zipFileError:
		print(f"Error occurred zipping system image files matched to products:\n\n{zipFileError}")
		writeLog(zipFileError, logType="error")
	return zipFileOutputPath



def combineSalesLayerAndFileSystemMatchingImages(dictOfSalesLayerMatchingImages, dictOfFileSystemMatchingImages):
	"""Takes dict of matching product images in Sales Layer export and dict of matching prod img in file system index, then returns new, combined dict of matching prod images"""
	#This function assumes that list of product SKUs w/o matched images from SL export search is used to search file system to avoid overwriting any results from the SL export search.
	combinedDictOfMatchingProductImages = dictOfSalesLayerMatchingImages
	for key, value in dictOfFileSystemMatchingImages.items():
		if key in combinedDictOfMatchingProductImages and bool(value):
			combinedDictOfMatchingProductImages[key].extend(value)
		elif bool(value):
			combinedDictOfMatchingProductImages[key] = value
	return combinedDictOfMatchingProductImages

def filterPickASportFileList(prodImageList):
	"""Receives list of matching product images, returns list of matching product images with "pick a sport" in the file name."""
	#For use with POD/PL "Pick-a-Sport" products that need a sport-agnostic set of images at the product level but individual images for each sport for variants.
	#print("\nprodImageList:\n", prodImageList, str(prodImageList), type(prodImageList))
	#Check if any image file name in the list of images contains "pickasport" after removing hyphens/underscores. If found, creates new list of just "pickasport" file names:
	if any("pickasport" in imgName.lower().replace("-", "").replace("_", "") for imgName in prodImageList):
		filteredPickASportImageList = list(filter(lambda imgName: "pickasport" in imgName.lower().replace("-", "").replace("_", ""), prodImageList))
		#print("\nfilteredPickASportImageList:\n", filteredPickASportImageList, str(filteredPickASportImageList), type(filteredPickASportImageList))
		return filteredPickASportImageList
	else:
		return prodImageList

def createFilteredPickASportProductImageDict(combinedDictOfMatchingProductImagesInput):
	"""Loops through dict of matching product images input, returns filtered dict using filterPickASportFileList() on each value/image list."""
	#Filter for pick-a-sport.
	combinedDictOfMatchingProductImagesOutput = {}
	for productSKUDictKey, imageList in combinedDictOfMatchingProductImagesInput.items():
		filteredImageList = filterPickASportFileList(imageList)
		combinedDictOfMatchingProductImagesOutput[productSKUDictKey] = filteredImageList
	return combinedDictOfMatchingProductImagesOutput

def removeSizeFromVariantSKU(variantSKU):
	"""Recieves Variant SKU and returns a SKU with product and color components but without size components"""
	variantSKU = variantSKU.VariantSKU #Swap variant SKU obj for just the variant SKU.
	lastHyphenPosition =  variantSKU.rfind("-")#Last hyphen in variant SKU & 1st character of size suffix to remove.
	#Remove size suffix: If SKU has more than 1 hyphen, the SKU is assumed to have a size suffix and the size suffix is trimmed. Gift & Accessories will have 0-1 hyphen (should be 1).
	numberOfHyphens = len(re.findall("-", variantSKU))
	variantSKUWithoutSize = variantSKU[:lastHyphenPosition].rstrip() if numberOfHyphens > 1 else variantSKU
	#print(variantSKUWithoutSize)
	variantSKUWithoutSize = re.sub("-[0-9]{1}-", "-", variantSKUWithoutSize)#Remove the -1-/-2- flags that appear before size suffix in POD/PL var SKUs but not in img file names (flags: 1 is visible in SL, 2 is invisible; for inventory tracking or something).
	youthSizeFragment = re.search("(-[0-9]{3})(-[0-9]{1})$", variantSKUWithoutSize) #Test and capture text fragments from youth sizes like "9-12M".
	#print(youthSizeFragment, youthSizeFragment.group()) if youthSizeFragment else print(youthSizeFragment)
	#LCFY010169-275-9-12M -> LCFY010169-275-9 -> LCFY010169-275:
	variantSKUWithoutSize = re.sub("-[0-9]{3}-[0-9]{1}$", youthSizeFragment.group(1), variantSKUWithoutSize) if youthSizeFragment else variantSKUWithoutSize#Remove any remaining fragments from youth sizes like "9-12M".
	#print(variantSKUWithoutSize)
	return variantSKUWithoutSize

def matchVariantsToFoundImages(dictOfAllMatchingProductImages, listOfVariants):
	"""Loops through list of variants, uses each's ProductSKUReference to search dict of matching product image list for matching images (after removing size from variant SKU). Returns a dict of variant keys/matching image list values."""
	#The input list of variants will contain Variant class objs. The output variant list will contain strings.
	#09/08/22 Also return list of variants w/o images that require them?
	dictOfMatchingVariantImages = {}
	listOfImageRequiredVariantsWithoutImg = []
	for varSKU in listOfVariants:
		if varSKU.ImageRequired:
			productSKU = varSKU.ProductSKUReference
			variantSKU = varSKU.VariantSKU
			dictOfMatchingVariantImages[variantSKU] = []
			if productSKU in dictOfAllMatchingProductImages.keys():
				varSKUWithoutSize = removeSizeFromVariantSKU(varSKU)
				for image in dictOfAllMatchingProductImages[productSKU]:
					if varSKUWithoutSize in image:
						dictOfMatchingVariantImages[variantSKU].append(image)
			#If the variant requires an images but nothing was found, add it to list of those requiring but missing an image:
			if not bool(dictOfMatchingVariantImages[variantSKU]):
				listOfImageRequiredVariantsWithoutImg.append(variantSKU)

	return dictOfMatchingVariantImages, listOfImageRequiredVariantsWithoutImg

#Run the img finding funcs
def findProductAndVariantImages(productInfoDict, variantInfoDict, fullPathToZipFileOutput):
	"""Extracts product and variant SKU lists from input dicts, uses list to search Sales Layer image info export and file system to match SKUs to images. Retuns lists of unmatch product SKUs"""
	listOfProdutSKUs = productInfoDict.keys()
	#listOfVariantSKUs = variantInfoDict.keys()
	#print("\n\nvariantInfoDict for Variant Image Search:", type(variantInfoDict), variantInfoDict, sep="\n")
	listOfVariantObjects = []
	for varObjList in variantInfoDict.values():
		listOfVariantObjects.extend(varObjList)
	#print("\n\nlistOfVariantObjects:", type(listOfVariantObjects), listOfVariantObjects, sep="\n")
	dictOfMatchingSLProductImages, listOfProductsWithoutImages = generateDictOfMatchingSLProductImages(listOfProdutSKUs)
	listOfProductsWithoutImages, dictOfMatchingFileSystemProductImages, listOfImagesToZip = generateDictOfMatchingFileSystemProductImages(listOfProductsWithoutImages)
	dictOfCombinedMatchingProductImages = combineSalesLayerAndFileSystemMatchingImages(dictOfMatchingSLProductImages, dictOfMatchingFileSystemProductImages)
	#print("\ndictOfCombinedMatchingProductImages:\n", dictOfCombinedMatchingProductImages)
	dictOfMatchingVariantImages, listOfVariantsMissingRequiredImages =  matchVariantsToFoundImages(dictOfCombinedMatchingProductImages, listOfVariantObjects)
	#Filter for pick-a-sport.
	filteredDictOfCombinedMatchingProductImages = createFilteredPickASportProductImageDict(dictOfCombinedMatchingProductImages)
	fullPathToZipFileOutput = zipMatchingProductImages(listOfImagesToZip, fullPathToZipFileOutput)
	return filteredDictOfCombinedMatchingProductImages, dictOfMatchingVariantImages, listOfProductsWithoutImages, listOfVariantsMissingRequiredImages

def mergeSLProductDataWithMatchingProductImagesDict(dictOfProductData, dictOfAllMatchingProductImages):
	"""Receives dicts of Sales Layer product data and matching product images, sets Sales Layer product obj ProductImages attribute value to either a matching image list or None. Returns the Sales Layer product data dict."""
	for prodSKUKey, productData in dictOfProductData.items():
		#Check if product SKU key in SL product dict is a key in dict of matching product images:
		if prodSKUKey in dictOfAllMatchingProductImages.keys():
			#Add list of product images from dict of all matching prod images to SL product obj's images attr:
			productData.ProductImages = dictOfAllMatchingProductImages[prodSKUKey] if bool(dictOfAllMatchingProductImages[prodSKUKey]) else None
	return dictOfProductData

##Need version of same func above for variants.
def mergeSLVariantDataWithMatchingVariantImagesDict(dictOfVariantData, dictOfAllMatchingVariantImages):
	"""Receives dicts of Sales Layer variant data and matching variant images, sets Sales Layer variant obj ProductImages attribute value to either a matching image list or None. Returns the Sales Layer variant data dict."""
	#print("Calling mergeSLVariantDataWithMatchingVariantImagesDict() for:", type(dictOfVariantData))
	#Loop through dict of variant data to get to list of variant objects:
	for prodSKUKey, variantData in dictOfVariantData.items():
		#Loop list of variant objects:
		for variant in variantData:
			#print(f"Looking up variant {variant.VariantSKU} in image dict.")
			if variant.VariantSKU in dictOfAllMatchingVariantImages.keys():
				#Add list of variant images from dict of all matching var images to SL variant obj's images attr:
				variant.VariantImage = dictOfAllMatchingVariantImages[variant.VariantSKU]
				#print("Variant SKU found in dict of matching images:", variant.VariantSKU)
			else:
				#print("Variant SKU NOT found in dict of matching images:", variant)
				variant.VariantImage = None
	return dictOfVariantData

if __name__ == "__main__":
	testProdSKU = "LCFH010118"
	testProdSKUList = ["LCFH010118", "AUB-MT0001-AUB-LAG891", "TWGM010049", "MUON012270", "CSUM000032", "ISUM999666"] #Added "CSUM000032" on 08/03/22 for testing file sys search (img will be in SL soon/invalidate test).
	testDictOfMatchingSLProductImages, testListOfProductsWithoutImages = generateDictOfMatchingSLProductImages(testProdSKUList)
	print("testDictOfMatchingSLProductImages", testDictOfMatchingSLProductImages)
	testMatchingFileSystemProductImageList, testMatchingFileSystemProductImagePathList = searchFileSystemForProductImages(testProdSKU)
	testListOfProductsWithoutImages, testDictOfMatchingFileSystemProductImages, testListOfImagesToZip = generateDictOfMatchingFileSystemProductImages(testListOfProductsWithoutImages)
	print(f"testListOfProductsWithoutImages: {testListOfProductsWithoutImages}", f"testDictOfMatchingFileSystemProductImages: {testDictOfMatchingFileSystemProductImages}", f"testListOfImagesToZip: {testListOfImagesToZip}", sep="\n")
	testZipFile = fr"C:\REDACTED\Python-Scripts\SAP_to_Sales_Layer_Data_Converter\Test_Data\Images\testZipArchive.zip"
	testOfZip = zipMatchingProductImages(testListOfImagesToZip, testZipFile)
	print(testOfZip)
	testDictOfCombinedMatchingProductImages = combineSalesLayerAndFileSystemMatchingImages({"Key1": ["Value1"], "Key2": ["Value2-1"]}, {"Key2": ["Value2-2"], "Key3": ["Value3"], "Key4": []})
	print(testDictOfCombinedMatchingProductImages)
	testVarSKUListSmall= ["RUTW019245-421-3X", "ISUN012459-999", "AUB-MT0001-AUB-LAG891-1-100-L", "AUB-MT0001-AUB-LAG891-1-100-M", "AUB-MT0001-AUB-LAG891-1-100-S", "AUB-MT0001-AUB-LAG891-1-100-2X", "AUB-MT0001-AUB-LAG891-1-100-XL", "SYR-MT0001-SYR-LAG881-1-419-2X", "SYR-MT0001-SYR-LAG881-1-419-L", "SYR-MT0001-SYR-LAG881-1-419-M", "SYR-MT0001-SYR-LAG881-1-419-S", "SYR-MT0001-SYR-LAG881-1-419-XL", "MUON012270-010", "ISUM999666-423-S"]
	testVariant = variantClass("AUB-MT0001-AUB-LAG891-1-100-2X", "AUB-MT0001-AUB-LAG891", "AUB", "2X", "", "", "", "100", "", "", "", "AUB-11-99999", "", "1", "", "", "", "", "092275313480", "100", "White", "True", "", "", "99999999", "AUB-MT0001-AUB-LAG891-1-100-2X")
	testDictOfMatchingVariantImages =  matchVariantsToFoundImages(testDictOfMatchingSLProductImages, [testVariant])
	print(testDictOfMatchingVariantImages)