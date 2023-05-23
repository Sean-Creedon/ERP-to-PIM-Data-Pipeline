#!/usr/bin/env python3
import os, pandas
import datetime

#The relative path to the Window OS user's "local" folder/user profile.
USER_FOLDER = os.path.expanduser("~")
#03/27/23 Updated after Box service removed:
SHARED_DRIVE_PATH = fr"{USER_FOLDER}\OneDrive - Dyehard Fan Supply" #Path to company shared drive. May change due to subscription costs.

#Dates, Timestamps, and Date-Based Paths:
NOW = datetime.datetime.now()
TODAY = datetime.date.today()
DAY_OF_THE_WEEK = TODAY.strftime("%A")
FIRST_HALF_OF_THE_WEEK = ["Saturday", "Sunday", "Monday", "Tuesday"]
if DAY_OF_THE_WEEK in FIRST_HALF_OF_THE_WEEK:
    LAST_FRIDAY = (TODAY - datetime.timedelta(days=TODAY.weekday()) + datetime.timedelta(days=4, weeks=-1))
    FILE_DATE = LAST_FRIDAY.strftime("%m-%d-%Y")#Date to use in file name
else:
    LAST_MONDAY = TODAY - datetime.timedelta(days=TODAY.weekday())
    FILE_DATE = LAST_MONDAY.strftime("%m-%d-%Y")#Date to use in file name
FILE_SYSTEM_DATE = TODAY.strftime("%m-%d-%y") #Date for folder and file names
TIME_OF_DAY = datetime.datetime.now().strftime("%I%M%p")
AM_OR_PM = "Morning" if "AM" in TIME_OF_DAY else "Afternoon"
AM_OR_PM = AM_OR_PM.replace("Afternoon","Night") if 12 != int(TIME_OF_DAY[:2]) > 5 else AM_OR_PM
OUTPUT_FOLDER_NAME = f"{DAY_OF_THE_WEEK}-{AM_OR_PM}-SAP-to-Sales-Layer-Upload-{FILE_SYSTEM_DATE}-{TIME_OF_DAY}"
#From DOMO export script. Currently this cannot be used since SAP query is always for the last 48 hours.
SAP_EXPORT_FILE_NAME = f"{DAY_OF_THE_WEEK}-SAP-products-data-created-after-{FILE_DATE}.csv"
#OUTPUT_FOLDER_PATH = fr"C:\Users\Sean Creedon\OneDrive - Dyehard Fan Supply\Downloads\{FILE_SYSTEM_DATE}\{OUTPUT_FOLDER_NAME}"
OUTPUT_FOLDER_PATH = fr"{SHARED_DRIVE_PATH}\eCommerce Product Uploads\{FILE_SYSTEM_DATE}\{OUTPUT_FOLDER_NAME}" #02/22/22
FULL_SAP_EXPORT_PATH = fr"{OUTPUT_FOLDER_PATH}\{SAP_EXPORT_FILE_NAME}"

#Python exec:
PYTHON_PATH = f"{USER_FOLDER}\AppData\Local\Programs\Python\Python310\python.exe"

#External python scripts:
SALESLAYER_IMAGE_INFO_EXPORT_SCRIPT = f"{USER_FOLDER}\Python-Scripts\Sales_Layer\Auto-Export-Sales-Layer-Image-Data\Auto_Export_SL_Product_Image_Data.py"
FILE_SYSTEM_IMAGE_FILE_INDEXING_SCRIPT = f"{USER_FOLDER}\Python-Scripts\List_Uploaded_Product_Images\List_All_Product_Images_in_Box.py"

#Common file paths:
ECOMM_INFO_FOLDER = fr"{USER_FOLDER}\OneDrive - Dyehard Fan Supply\Python-Scripts\eCommerce Product Uploads"

#Sales Layer Image Info Export and column header list:
SALESLAYER_IMAGE_INFO_EXPORT = fr"{ECOMM_INFO_FOLDER}\Sales-Layer-Image-Data-Export.csv"
SL_IMG_INFO_EXPORT_COL_NAMES = ["Reference", "Status", "Tags", "Links", "Tables with links", "URL", "Source URL", "Type", "Size (in bytes)", "Width", "Height", "Bits"]
SALESLAYER_IMAGE_DATA = pandas.read_csv(SALESLAYER_IMAGE_INFO_EXPORT, delimiter="\s+|;|,", header=0, names=SL_IMG_INFO_EXPORT_COL_NAMES, dtype="unicode", engine="python", skipinitialspace=True, usecols=SL_IMG_INFO_EXPORT_COL_NAMES).fillna("")
SL_UPLOADED_IMAGE_FILE_LIST = SALESLAYER_IMAGE_DATA["Reference"].tolist()
#Index product images on file system/company drive (12/20/22: Box, but could change due to subscription costs).
try:
    print("Reactivate file system image indexing & add SL img export.")
except Exception as fileSystemIndesingError:
    print(f"Error indexing file system's images:\n{fileSystemIndesingError}")
#Index of product images in Box, column header list, and file name/path lists:
FILE_SYSTEM_PRODUCT_IMAGE_INDEX = fr"{ECOMM_INFO_FOLDER}\Product-Images-Files-Index.csv"
FILE_SYSTEM_PRODUCT_IMG_INDEX_COL_NAMES = ["Product Image File Names", "Product Image File Paths"]
FILE_SYSTEM_IMAGE_INDEX = pandas.read_csv(FILE_SYSTEM_PRODUCT_IMAGE_INDEX, delimiter=",", header=0, names=FILE_SYSTEM_PRODUCT_IMG_INDEX_COL_NAMES, dtype="unicode", skipinitialspace=True, usecols=FILE_SYSTEM_PRODUCT_IMG_INDEX_COL_NAMES).fillna("")
FILE_SYSTEM_IMAGES = FILE_SYSTEM_IMAGE_INDEX["Product Image File Names"].tolist()
FILE_SYSTEM_IMG_PATHS = FILE_SYSTEM_IMAGE_INDEX["Product Image File Paths"].tolist()

#Path to all logs (errors/reports):
LOG_FOLDER_PATH = fr"{USER_FOLDER}\OneDrive - Dyehard Fan Supply\Python-Scripts\SAP_to_Sales_Layer_Data_Converter\Test_Data\Logs"
FULL_ERROR_REPORT_PATH = f"{LOG_FOLDER_PATH}\Errors.txt"

#Ecomm Upload Tracker
#Used to record and track if products/variants have been recently uploaded. Used to avoid re-uploading products/variants
#and only update products/variants if they are modified within 48 hours of their initial upload.
RECENTLY_UPLOADED_PRODUCTS = {}
RECENTLY_UPLOADED_VARIANTS = {}
RECENTLY_MODIFIED_PRODUCTS = {}
RECENTLY_MODIFIED_VARIANTS = {}
PRODUCT_UPLOAD_TRACKING_SHEET = fr"{ECOMM_INFO_FOLDER}\eCommerce_Product_Upload_Tracker.csv"
VARIANT_UPLOAD_TRACKING_SHEET = fr"{ECOMM_INFO_FOLDER}\eCommerce_Variant_Upload_Tracker.csv"

#Sports specific:
#Use to check if a sport is an official sport. For now, use to filter values that include event/collection and whatever else. Have suggested dedicated field for prod sport in SAP.
SPORTS = ["Air Sports", "Archery", "Band", "Baseball", "Basketball", "Bassmaster", "Beach & Ball", "Beach Handball", "Beach Volleyball", "Billards", "Boules", "Bowling", "Canoe", "Cheer", "Crew", "Cross Country", "Cycling", "Dancesport", "Duathlon", "Equestrian", "Field Hockey", "Figure Skating", "Finswimming", "Fishing", "Fistball", "Flag Football", "Floorball", "Flying Disc", "Football", "Golf", "Gymnastics", "Hockey", "Ice Hockey", "Jujitsu", "Karate", "Kickboxing", "Korfball", "Lacrosse", "Lifesaving", "Muay Thai", "Orienteering", "Powerlifting", "Racquetball", "Rifle", "Roller Sports", "Rowing", "Rugby", "Soccer", "Softball", "Sport", "Climbing", "Squash", "Sumo", "Swimming & Diving", "Synchronized", "Skating", "Tennis", "Track & Field", "Tug of War", "Volleyball", "Wakeboarding", "Wheelchair Rugby", "Wrestling", "Wushu"]

#This dict's keys are used to check for conference team names in product names. Values can be used to correct/normalize names (only used for Sports Team field for product info in SL as of 01/13/23).
TEAM_NAMES = {
"georgetown": "Georgetown",
"marquette": "Marquette",
"providence": "Providence",
"seton": "Seton Hall",
"st john": "St. John's",
"st. john": "St. John's",
"st johns": "Saint John's",
"st. johns": "Saint John's",
"st john's": "Saint John's",
"st. john's": "Saint John's",
"uconn": "UConn",
"villanova": "Villanova",
"xavier": "Xavier",
"butler": "Butler",
"creighton": "Creighton",
"depaul": "DePaul",
"brigham young": "Brigham Young",
"loyola marymount": "Loyola Marymount",
"portland": "Portland",
"aztecs": "Aztecs",
"gonzaga": "Gonzaga",
"st. mary": "Saint Mary's",
"st mary": "Saint Mary's",
"st marys": "Saint Mary's",
"st. marys": "Saint Mary's",
"st mary's": "Saint Mary's",
"st. mary's": "Saint Mary's",
"saint mary": "Saint Mary's",
"saint marys": "Saint Mary's",
"saint mary's": "Saint Mary's",
"san diego": "San Diego",
"san francisco": "San Francisco",
"santa clara": "Santa Clara",
"sf state": "SF State",
"pepperdine": "Pepperdine",
"pacific tigers": "Pacific Tigers",}

TEAM_NAME_LIST = list(TEAM_NAMES.keys())

#Terms in product name that indicate the product is memorabilia: 
MEMORABILIA_TERMS = ["autograph", "signed", "game worn", "game-worn", "gameworn"]

#Item Group Names:
ITEM_GROUP_NAMES = ["Items", "Lottery", "Mens", "Novelty", "Fixed Assets", "Food and Beverage", "Overhead", "Raw Material", "Services", "Womens", "Footwear", "Headwear", "Youth", "Item Setup", "Supplies", "Gift Card", "Square"]
#Novelty Item Group Names:
NOVELTY_ITEM_GROUP_NAMES = ["Items", "Lottery", "Novelty", "Food and Beverage", "Gift Card"]
#Apparel Item Group Names:
APPAREL_ITEM_GROUP_NAMES = ["Mens", "Womens", "Youth"]

#SAP Product Line  Names:
PRODUCT_LINE_NAMES = ["ACCESSORY", "ATHLETIC SHOES", "AUTHENIC JERSEY", "AUTHENTIC JERSEY", "AUTOMOTIVE", "BAG", "BALLS/INFLATIBLES", "BATH", "BED", "Bells", "BELTS", "BLANKET", "BOOTS", "BOTTOMS", "BUCKET", "CASUAL SHOES", "CLOTHING ACCESSORIES", "COLLECTIBLE", "CONSIGNMENT", "DECAL MAGNET TATTOO", "DECOR", "Dress", "DRESSES", "DRINKWARE", "FASHION", "FASHION JERSEY", "Flags Pennants", "FLEECE CREW", "FLEECE FASHION", "FLEECE FULL ZIP", "FLEECE HALF ZIP", "FLEECE HOODIE", "Frames", "GAME WORN", "GLASSWARE", "HAIR", "HELMET", "HOBBIES & GAMES", "HOOD", "JERSEYS", "JEWELRY", "Keychains", "KITCHEN", "KNIT HAT", "KOOZIES", "Lanyards", "Lapel Pins", "LEGGINGS", "LIQUOR", "LONG SLEEVE", "LOTTERY", "MENS HAT", "MUGS", "NON ALCOHOLIC", "NON PLUSH TOY", "ONESIE", "OUT FULL ZIP", "OUT HALF ZIP", "OUT JACKET", "OVER THE COUNTER", "OVERALLS", "PANTS", "PET ACCESSORY", "PLUSH", "Poms", "PONCHO", "PRACTICE JERSEY", "Rally Locker Room Towels", "REGULAR JERSEY", "REPLICA JERSEY", "SCARVES", "School Supplies", "SETS", "SHOES", "SHORT SLEEVE", "SHORTS", "Signed Game Worn", "SKIRTS", "SLIDES", "SLIPPERS", "SNACKS", "SNEAKERS", "SOCKS", "STRAW", "STRUCTURED HAT", "TAILGATE PRODUCT", "TANK", "TOBACCO", "TUMBLERS", "UNSTRUCTURED HAT", "VEST", "VISORS", "WATER BOTTLE", "WEATHER", "WOMENS HAT", "YOUTH HAT"]

#First Level Family Names Product Line Lists if no Group Name in data (i.e. product line "KNIT HAT" add "Headwear" or "Dress" will add the "Womens" in "Womens>Tops"). Note there's some gender assumptions built in here.
AMBIGIOUS_PRODUCT_LINE_NAMES = ["CONSIGNMENT", "COLLECTIBLE", "GAME WORN", "Signed Game Worn"]
FOOTWEAR_PRODUCT_LINE_NAMES = ["ATHLETIC SHOES", "BOOTS", "CASUAL SHOES", "SHOES", "SLIDES", "SLIPPERS", "SNEAKERS", "SOCKS"]
HEADWEAR_PRODUCT_LINE_NAMES = ["BUCKET", "KNIT HAT", "MENS HAT", "UNSTRUCTURED HAT", "VISORS", "WOMENS HAT", "YOUTH HAT", "STRAW" , "STRUCTURED HAT"]
MENS_PRODUCT_LINE_NAMES = ["MENS HAT"]
WOMENS_PRODUCT_LINE_NAMES = ["WOMENS HAT", "FASHION"]#Note there's some gender assumptions built in here.
NOVELTY_PRODUCT_LINE_NAMES = ["ACCESSORY", "AUTOMOTIVE", "BAG", "BALLS/INFLATIBLES", "BATH", "BED", "Bells", "BELTS", "BLANKET", "CLOTHING ACCESSORIES", "DECAL MAGNET TATTOO", "DECOR", "DRINKWARE", "Flags Pennants", "Frames", "GLASSWARE", "HAIR", "HELMET", "HOBBIES & GAMES", "JEWELRY", "Keychains", "KITCHEN", "KOOZIES", "Lanyards", "Lapel Pins", "LIQUOR", "LOTTERY", "MUGS", "NON ALCOHOLIC", "NON PLUSH TOY", "OVER THE COUNTER", "PET ACCESSORY", "PLUSH", "Poms", "Rally Locker Room Towels", "SCARVES", "School Supplies", "SETS", "SNACKS", "TAILGATE PRODUCT", "TOBACCO", "TUMBLERS", "WATER BOTTLE", "WEATHER"]
YOUTH_PRODUCT_LINE_NAMES = ["YOUTH HAT", "ONESIE"]

#Second Level Family Names Product Line Lists (i.e. product line "SHORT SLEEVE" will add the "Tops" in "Mens>Tops"):
BOTTOMS_PRODUCT_LINE_NAMES = ["BOTTOMS", "SHORTS", "PANTS", "SKIRTS", "LEGGINGS", "OVERALLS"]
FLEECE_PRODUCT_LINE_NAMES = ["FLEECE CREW", "FLEECE FASHION", "FLEECE FULL ZIP", "FLEECE HALF ZIP", "FLEECE HOODIE"]
JERSEYS_PRODUCT_LINE_NAMES = ["AUTHENTIC JERSEY", "JERSEYS", "AUTHENIC JERSEY", "REPLICA JERSEY", "REGULAR JERSEY", "FASHION JERSEY", "PRACTICE JERSEY"]
OUTERWEAR_PRODUCT_LINE_NAMES = ["OUT FULL ZIP", "OUT HALF ZIP", "OUT JACKET", "VEST", "PONCHO"]
#No Product Lines for polos currently (01/09/23).
#POLO_PRODUCT_LINE_NAMES = [""]
TOPS_PRODUCT_LINE_NAMES = ["SHORT SLEEVE", "LONG SLEEVE", "TANK", "Dress", "DRESSES", "HOOD", "ONESIE"]#Don't forget: 2nd level family name is "Tops" for Mens and Womens, "Tees" for Youth

#Weights and Measures:
#Used to track if a products's weight (and shipping length, width, and height later, maybe).
LIST_OF_13OZ_ITEM_GROUPS = ["AUTHENIC JERSEY", "AUTHENTIC JERSEY", "Bells", "BELTS", "BLANKET", "DECAL MAGNET TATTOO", "FASHION JERSEY", "Flags Pennants", "GAME WORN", "HAIR", "JERSEYS", "Keychains", "KNIT HAT", "KOOZIES", "Lanyards", "Lapel Pins", "LEGGINGS", "ONESIE", "Poms", "PRACTICE JERSEY", "REGULAR JERSEY", "REPLICA JERSEY", "SCARVES", "SHORT SLEEVE", "SHORTS", "SKIRTS", "SOCKS", "STRAW", "TANK"]
LIST_OF_16OZ_ITEM_GROUPS = ["BAG", "BALLS/INFLATIBLES""BOTTOMS", "BUCKET", "CLOTHING ACCESSORIES", "Dress", "DRESSES", "DRINKWARE", "FASHION", "FLEECE CREW", "FLEECE FASHION", "FLEECE FULL ZIP", "FLEECE HALF ZIP", "FLEECE HOODIE", "GLASSWARE", "HOOD", "JEWELRY", "LONG SLEEVE", "MENS HAT", "MUGS", "OUT FULL ZIP", "OUT HALF ZIP", "OVER THE COUNTER", "OVERALLS", "PANTS", "PLUSH", "PONCHO", "Rally Locker Room Towels", "SLIDES", "SLIPPERS", "SNACKS", "STRUCTURED HAT", "TOBACCO", "TUMBLERS", "UNSTRUCTURED HAT", "VEST", "VISORS", "WATER BOTTLE", "WOMENS HAT", "YOUTH HAT"]
LIST_OF_24OZ_ITEM_GROUPS = ["ATHLETIC SHOES", "CASUAL SHOES", "HELMET", "SHOES", "SNEAKERS"]
LIST_OF_32OZ_ITEM_GROUPS = ["BOOTS", "LIQUOR", "NON ALCOHOLIC", "OUT JACKET"]
#Currently not used:
LIST_OF_40OZ_ITEM_GROUPS = ["MALT LIQUOR"]
#Probably won't be used:
LIST_OF_ITEM_GROUPS_WITH_VARIABLE_SHIPPING_WEIGHTS = ["ACCESSORY", "AUTOMOTIVE", "BATH", "BED", "COLLECTIBLE", "CONSIGNMENT", "DECOR", "Frames", "HOBBIES & GAMES", "KITCHEN", "LOTTERY", "NON PLUSH TOY", "PET ACCESSORY", "School Supplies", "SETS", "Signed Game Worn", "TAILGATE PRODUCT", "WEATHER"]

#Age Group and Gender Values:
OTHER_YOUTH_AGE_GROUPS = ["infant", "toddler", "kids", "newborn"]

#Sales Layer new product import sheet info:
SALESLAYER_PRODUCT_IMPORT_SHEET_HEADER = "Product SKU,Family,Product Name,Category Name,Category,Product Description,Tags,Price,OId Description,Use Old Description,Product Images,Size Chart,Product Image 2,Product Image 3,Product Image 4,Product Image 5,Product Image 6,Product Image 7,Product Image 8,Product Image 9,Lifestyle Image 1,Lifestyle Image 2,Lifestyle Image 3,Lifestyle Image 4,Brand Name,Product Brand ID,Age Group,Gender,Is Unisex?,Is Licensed,Season,Sport,Memorabilia,Activity,Fit,Material Type,Material Content,Temperature Rating,Care Instructions,Features,Player Name,Event/Collection,League,Sports Team,Country of Origin,Default Warehouse,Lead Time,Fixed Shipping Cost,Free Shipping,Product Weight,Tax Liable,AvaTax Code,Product Tax Class,Model Group,Previous eComm Number,Product Line Code,Inventory Item,Production Date,Purchase Item,Sales Item,Preferred Vendor,Foreign Name,Item Group,Item Type,Division,Allow Purchases,Track Inventory,Handle,Keywords,WMT Tags,Filters,Created Date,COGS,Discounts & Promotions Applicable\n"
SALESLAYER_VARIANT_IMPORT_SHEET_HEADER = "Variant SKU,Product SKU Reference,Condition,Tags,Variant Size,Variant Price,Variant Image,Vendor Variant Color,Variant Color,Variant Sport,Variant Sort Order,Product Length,GTIN,MPN,UPC,Low Stock Level,Variant Height (3),Variant Width (3),Variant Depth (3),Variant Weight (3),ERP Barcode,Variant Color (WMT),Color Name,Image Required,VendorUPC,ListingSKU,Cost,COGs\n"
SALESLAYER_PRODUCT_IMPORT_FILENAME = f"{DAY_OF_THE_WEEK}-Sales-Layer-Product-Import-Sheet-{FILE_DATE}.csv"
FULL_SALESLAYER_PRODUCT_IMPORT_PATH = fr"{OUTPUT_FOLDER_PATH}\{SALESLAYER_PRODUCT_IMPORT_FILENAME}"
SALESLAYER_VARIANT_IMPORT_FILENAME = f"{DAY_OF_THE_WEEK}-Sales-Layer-Variant-Import-Sheet-{FILE_DATE}.csv"
FULL_SALESLAYER_VARIANT_IMPORT_PATH = fr"{OUTPUT_FOLDER_PATH}\{SALESLAYER_VARIANT_IMPORT_FILENAME}"


#Sales Layer API info:
SALESLAYER_URL = "https://api.saleslayer.com"
NEW_PRODUCT_CONNECTOR_ID_CODE = "ENTER_NEW_PRODUCT_CONNECTOR_ID_CODE_HERE"
NEW_PRODUCT_CHANNEL_PRIVATE_KEY = "ENTER_NEW_PRODUCT_CHANNEL_PRIVATE_KEY_HERE"
MODIFY_PRODUCT_CONNECTOR_ID_CODE = "ENTER_MODIFY_PRODUCT_CONNECTOR_ID_CODE_HERE"
MODIFY_PRODUCT_CHANNEL_PRIVATE_KEY = "ENTER_MODIFY_PRODUCT_CHANNEL_PRIVATE_KEY_HERE"
SALESLAYER_NEW_PRODUCT_JSON = {"input_data": {"products": [], "variants": []}}
SALESLAYER_MODIFY_PRODUCT_JSON = {"input_data": {"products": [], "variants": []}}

#Artificial Intellegence/OpenAI info:
os.environ.setdefault("OPENAI_API_KEY", "ENTER_OPENAI_API_KEY_HERE")
#Product Descriptions AI
#Path to CSV output:
##ACTIVATE THE NEXT 2 LINES WHEN DONE TESTING:
#PRODUCT_DESCRIPTIONS_OUTPUT_PATH = fr"{OUTPUT_FOLDER_PATH}\SL-AI-Description-Instructions-and-AI-Generated-Product-Descriptions-{FILE_SYSTEM_DATE}-{TIME_OF_DAY}.csv"
#AI_PRODUCT_CATEGORIZATION_OUTPUT_PATH = fr"{OUTPUT_FOLDER_PATH}\SL-AI-Product-Category-Assignments-{FILE_SYSTEM_DATE}-{TIME_OF_DAY}.csv"
#OpenAI model for generating product descriptions:
DYEHARD_ECOMM_PRODUCT_DESCRIPTION_AI = "curie:ft-dyehard-fan-supply-llc:dyehard-ecomm-product-descriptions-model-2022-12-23-08-29-32"
#Previous version of categorizaion AI (copy current version here before continued fine-tuning):
#DYEHARD_ECOMM_PRODUCT_CATEGORIZATION_AI = "babbage:ft-dyehard-fan-supply-llc:dyehard-ecomm-categorization-model-2023-02-10-01-45-21"
DYEHARD_ECOMM_PRODUCT_CATEGORIZATION_AI = "babbage:ft-dyehard-fan-supply-llc:dyehard-ecomm-categorization-model-2023-03-03-01-13-16"

#Property Info:

#Property tags/SKUs to NOT upload to Sales Layer:
#Will check the 1st characters of Item No/SKU rather than model/tag value (expect raw material SKU info to be incomplete).
#Includes raw material, generic items, and goods purchased from Silver Crystal.
PRODUCTS_TO_IGNORE = ["RM", "GEN", "SIL"]
#Sometimes a generic SKU is used for products that go on multiple websites. Change this value to false to include generic items in uploads.
INCLUDE_GENERIC_ITEMS = False #So far there's not a way to toggle this value outside changing this line. 03/13/23


#Property Names
DYEHARD_PROPERTY_TAG_TO_NAME_DICT = {
    "AOD": "Kentucky Derby",
    "ARA": "University of Arkansas",
    "ARK": "University of Arkansas",
    "ASU": "Appalachian State University",
    "AUB": "Auburn University",
    "AZB": "Arizona Bowl",
    "BEC": "Big East Conference",
    "BNY": "Bike New York",
    "BSM": "Bassmaster",
    "BWS": "Bowl Bound",
    "CIB": "Guaranteed Rate Bowl",
    "COL": "Columbia University",
    "CSU": "Colorado State University",
    "DEL": "University of Delaware",
    "FIB": "Fiesta Bowl",
    "FST": "1/ST Racing Tour",
    "GRB": "Guaranteed Rate Bowl",
    "ISU": "Iowa State University",
    "KYD": "Kentucky Derby",
    "LCF": "LouCity Football Club",
    "MCB": "Music City Bowl",
    "MIB": "Military Bowl",
    "MIS": "Mississippi State University",
    "MSU": "Michigan State University",
    "MUO": "Miami University of Ohio",
    "NYR": "NYRA Horse Racing",
    "OMI": "University of Mississippi",
    "PIT": "University of Pittsburgh",
    "PRO": "Professional Rodeo Cowboys Association",
    "PUR": "Purdue University",
    "RLF": "Racing Louisville Football Club",
    "RUT": "Rutgers University",
    "SFA": "Stephen F. Austin State University",
    "SGB": "Sugar Bowl",
    "SUB": "Sugar Bowl",
    "SYR": "Syracuse University",
    "TWG": "The World Games",
    "UCO": "University of Connecticut",
    "UNC": "University of North Carolina at Chapel Hill",
    "UST": "USTA LEAGUES",
    "USV": "USA Volleyball",
    "WCC": "West Coast Conference",
    "WGW": "The World Games",
    "WSO": "Winston-Salem Open",
    "WVU": "West Virginia University"
  }

if __name__ == "__main__":
    #Test the date to pinpoint correct cut off.
    date_time= "03-07-23"
    datetime_str = datetime.datetime.strptime(date_time, "%m-%d-%y")
    print(datetime_str, type(datetime_str))
    now = datetime.datetime.now()
    print(now, type(now))
    diff = now - datetime_str
    print(diff, type(diff))
    print(diff.days)
    if diff.days > 1:
        print("Old")
