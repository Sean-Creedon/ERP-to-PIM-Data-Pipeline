# ERP-to-PIM-Data-Pipeline
ETL/Data Pipeline to process ecommerce product data between ERP and PIM systems. 

SAP_to_Sales_Layer_Data_Converter Script Notes and Documentation

NOTE: This document is incomplete and only a high level view of how the components work together. It is missing NLP, AI, and upload/change tracking functions completely.

Overview:

Reads exported SAP product data, converts it for upload to Sales Layer, matches product images in the Sales Layer media library, plus searches a designated file system for matching product images if none found in the media library.

The main function that forms the infrastructure and controls this workflow is:

runSAPDataToSalesLayerDataConversion(inputFile, outputPath)

This assembles the major functional pieces (read SAP CSV export, generate Sales Layer product/variant data, find matching images) into an ordered workflow. It receives an SAP product data export and a network path as input parameters (an input file and a folder for output).

11/14/2022:
    • As of this date input will be a flat file (current CSV). Currently, ecomm doesn’t have API access to SAP. Ecomm does expect to have possible FTP site access in the future.
    • Will upload data and images directly to Sales Layer.

Required Python Libraries and Dependencies:

The following Python libraries are required to execute this script:
datetime, collections, csv, hashlib, logging, math, os, pathlib, random, re, requests, shutil, subprocess, tempfile, time
These libraries are also required and may need to be installed separately after the initial Python installation on a new machine:
openai, pandas, NLTK (note that the “popular” NLTK data was installed during testing but only WordNet is used as of 03/16/23), 

Main Subfunctions in Order of Execution:

readCSV(inputFile, readSAPDataCSV):

readCSV() reads the SAP export input file and is meant to be reusable for reading a CSV and formatting that data. The CSV data is formatting using the function received as the second parameter. Here the readCSV() function uses the readSAPDataCSV() function from the SAP_Data_Class to load each row’s data as a unique SAP_Data_Class object.

This step generates a key/value collection (dictionary) where each key is an SAP SKU and the value is the SAP_Data_Class object. This dictionary is returned to the script for the next step (product data assembly).

assembleProductData(dataFromSAP):

Receives the dictionary of SAP data objects (labeled by SAP/variant SKU) as input.
This step takes the SAP data objects, which are still unmatched/ungrouped product variants, and assembles them into groups labeled by the intended product SKU.

This step generates a key/value collection (dictionary) where each key is an SAP/Sales Layer SKU and the value is a list of related SAP_Data_Class objects. This dictionary is returned to the script for the next step (generate Sales Layer product data).

generateDictsOfSLProductsAndVariants(dictOfSAPData):

This step loops through the collection of product SKUs/list of SAP object pairings to:

    1. Generates key/value collection of Sales Layer product data using the generateSLProductFromSAPData() and the first SAP data object in the list.
    2. Generates key/value collection of Sales Layer variant data using generateSLVariantFromSAPData() and every SAP data object in the list.
findProductAndVariantImages(dictOfSLProduct, dictOfSLVariant, imageZipToUpload):
Receives the dictionaries of Sales Layer product and variant information plus a path to output a zip file containing any product images to upload to Sales Layer.

This step generates a list of product SKUs and a list of variant objects then runs external scripts to export all media library information from Sales Layer and scan the designated file system for all web-ready product images. The media library export and the index of file system images are saved as .CSV files. Note: If concurrency or multiprocessing capabilities are ever added to this script, move these export/file scan operations outside this function and launch at the start of the script.

The function then searches the Sales Layer export using the list of product SKUs, generating a dictionary of matching images (product SKU keys/list of images values) and a list of products without matching images in Sales Layer.

Next, the function searches the index of file system product images using the list of product SKUs without images. The function creates the dictionary of matching file system images (SKU key/image list values) and list of products without images with any images it finds while generating a list of images to zip for upload.

The function combines the dictionaries of matching uploaded Sales Layer images and matching files system images, then uses this combined dictionary to match images to any variants that require them (for the WMT platform only???), creating a dictionary of variant SKU keys/image list values.

The dictionary of matching Sales Layer images is then searched for any “pick-a-sport” images. If any list of product images has image files with “pick-a-sport” in the name, it is presumed to be a multi-sport product which should only have the “sport-agnostic” images and not every image for each sport. When a list of images for a “pick-a-sport” product is found, a list of only images with “pick-a-sport" in the name is created. A new, filtered dictionary of product images is created as the final product image information output.

The function then zips the images it identified for uploading.

When finished, this function passes the following back to the rest of the program:

    1. The dictionary of matching product images (filtered for “pick-a-sport” products).
    2. The dictionary of matching variant images
    3. A list of product SKUs unmatched to images in the media library and files system.
    4. A list of variant SKUs unmatched to images in the media library and files system.

mergeSLProductDataWithMatchingProductImagesDict(dictOfSLProduct, dictOfAllMatchingProductImages):

This function receives the dictionary of Sales Layer product data (SKU key, Sales Layer data object values), and the combined dictionary of matching product images (from the Sales Layer media library and the file system).

This step adds the lists of matching product images to the Sales Layer product data objects.

mergeSLVariantDataWithMatchingVariantImagesDict(dictOfSLVariant, dictOfVariantImages):

This function receives the dictionary of Sales Layer variant data (SKU key, Sales Layer data object values), and the combined dictionary of matching variant images.

This step adds the lists of matching variant images to the Sales Layer variant data objects.
