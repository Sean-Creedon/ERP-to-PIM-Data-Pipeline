#!/usr/bin/python3
import re
from Property_Information import *
from collections import Counter
from Constants import *

#This func may still be needed despite repeated word check in next func (would get property name followed by tag: "West Coast Conference WCC . . .")
def fixRepeatedPropertyTag(SAPProductName):
	"""Checks beginning of string parameter for repeated 3-letter code, returns string with repeated code removed."""
	#Check if 1st three characters repeats after a space (repeated property tag: "NYR NYR Primary Logo Compass Polo").
	if (SAPProductName[0:3] == SAPProductName[4:7]) and (SAPProductName[3:4] == " "):
		#print(f"Repeated property tag: {SAPProductName}")
		SAPProductName = SAPProductName.replace(SAPProductName[0:4], "", 1)
		#print(SAPProductName)
	return SAPProductName

###SEE EXAMPLE: Repeated team name issue.
def replacePropertyTagPrefixWithName(SAPProductName):
	"""Checks if starting 3 letter code in parameter is in keys of property tag key/property name value dict. Returns dict value"""
	#Replaces property code prefix in product name with team name. "CSU Rams Yard Dice" becomes "Colorado State Rams Rams Yard Dice"
	if (SAPProductName[0:3].isalpha()) and (SAPProductName[3:4] == " "):#Check if name begins with three letter followed by a space (prevents "NYRA" from becoming "NYRAA").
		propertyTag = SAPProductName[0:3]
		if propertyTag in list(propteryTagToNameDict.keys()):
			propertyName = propteryTagToNameDict[propertyTag]
			SAPProductName = SAPProductName.replace(propertyTag, propertyName, 1)
	#Fix repeated words:
	SAPProductNameWordList = SAPProductName.split(" ")
	#print(SAPProductNameWordList)
	wordCounts = Counter(SAPProductNameWordList)
	#print(wordCounts)
	for word in SAPProductNameWordList:
		if wordCounts[word]>1:
			#print(f"Repeated word: {word}")
			SAPProductName = SAPProductName.replace(f"{word} {word}", f"{word}")
	return SAPProductName

def updateSAPProductName(SAPProductName):
	""""""
	SAPProductName = SAPProductName.title().replace("TeeTee","T-Shirt")
	SAPProductName = SAPProductName.title().replace("Tee","T-Shirt")
	SAPProductName = SAPProductName.replace("Tee Shirt","T-Shirt")
	SAPProductName = SAPProductName.replace("Thirt","Shirt")
	SAPProductName = SAPProductName.replace("Shirt Shirt","Shirt")
	SAPProductName = SAPProductName.replace(" T-Shirt T-Shirt"," T-Shirt")
	SAPProductName = SAPProductName.replace("T-Shirtshirt","T-Shirt")
	SAPProductName = SAPProductName.replace("Tshirt","T-Shirt")
#Change the "x" in dimensions to lower case: 2X2" to 2x2"
	if re.search("[0-9]X[0-9]", SAPProductName):
		temp = re.search("[0-9]X[0-9]", SAPProductName).group().replace("X", "x")
		SAPProductName = re.sub("[0-9]X[0-9]", temp, SAPProductName)
	if re.search("[0-9] X [0-9]", SAPProductName):
		temp = re.search("[0-9] X [0-9]", SAPProductName).group().replace("X", "x")
		SAPProductName = re.sub("[0-9] X [0-9]", temp, SAPProductName)
#Change the "T" in "1St" to "1st"
	if re.search("[0-9]St ", SAPProductName):
		temp = re.search("[0-9]St ", SAPProductName).group().replace("S", "s")
		SAPProductName = re.sub("[0-9]St ", temp, SAPProductName)
#Change the "2Nd" in "2nd"
	if re.search("[0-9]Nd ", SAPProductName):
		temp = re.search("[0-9]Nd ", SAPProductName).group().replace("N", "n")
		SAPProductName = re.sub("[0-9]Nd ", temp, SAPProductName)
#Change the "R" in "3Rd" to "3rd"
	if re.search("[0-9]Rd ", SAPProductName):
		temp = re.search("[0-9]Rd ", SAPProductName).group().replace("R", "r")
		SAPProductName = re.sub("[0-9]Rd ", temp, SAPProductName)
#Change the "T" in "4th" and whatnot to lower case: 5Th to 5th
	if re.search("[0-9]Th ", SAPProductName):
		temp = re.search("[0-9]Th ", SAPProductName).group().replace("T", "t")
		SAPProductName = re.sub("[0-9]Th ", temp, SAPProductName)
	SAPProductName = SAPProductName.replace(" (Thru 3X)", "")
	SAPProductName = SAPProductName.replace(" Acc "," ACC ")
	SAPProductName = SAPProductName.replace(" And ", " and ")
	SAPProductName = SAPProductName.replace(" Asu ", " ASU ")
	SAPProductName = SAPProductName.replace(" At ", " at ")
	SAPProductName = SAPProductName.replace(" Au ", " AU ")
	SAPProductName = SAPProductName.replace("Bbq", "BBQ")
	SAPProductName = SAPProductName.replace(" BLK", " Black")
	SAPProductName = SAPProductName.replace(" Blk", " Black")
	SAPProductName = SAPProductName.replace(" Blk/Org", " Black/Orange").replace(" BLK/ORG", " Black/Orange")
	SAPProductName = SAPProductName.replace(" Caa ", " CAA ")
	SAPProductName = SAPProductName.replace(" Cws ", " CWS ")
	SAPProductName = SAPProductName.replace(" Ez ", " EZ ")
	SAPProductName = SAPProductName.replace(" Eza ", " EZA ")
	SAPProductName = SAPProductName.replace(" F/Zip", " Full Zip")
	SAPProductName = SAPProductName.replace(" For ", " for ")
	SAPProductName = SAPProductName.replace("Fst 1Rt", "FST 1RT")
	SAPProductName = SAPProductName.replace(" Fullzip ", " Full Zip ")
	SAPProductName = SAPProductName.replace(" FZ ", " Full Zip ")
	SAPProductName = SAPProductName.replace(" Fz ", " Full Zip ")
	SAPProductName = SAPProductName.replace("Grb ", "GRB ")
	SAPProductName = SAPProductName.replace(" HOOD/PNT ", " Hoodie/Pants ")
	SAPProductName = SAPProductName.replace(" Hood/Pnt ", " Hoodie/Pants ")
	SAPProductName = SAPProductName.replace(" HOODY", " Hoodie")
	SAPProductName = SAPProductName.replace(" Hoody", " Hoodie")
	SAPProductName = SAPProductName.replace(" Hthr ", " Heather ")
	SAPProductName = SAPProductName.replace(" Ii ", " II ")
	SAPProductName = SAPProductName.replace(" Iii ", " III ")
	SAPProductName = SAPProductName.replace(" In ", " in ")
	SAPProductName = SAPProductName.replace(" INF ", " Infant ")
	SAPProductName = SAPProductName.replace(" Inf ", " Infant ")
	SAPProductName = SAPProductName.replace(" It'S ", " It's ")
	SAPProductName = SAPProductName.replace(" Iv ", " IV ")
	SAPProductName = SAPProductName.replace(" L/S", " Long Sleeve ")
	SAPProductName = SAPProductName.replace(" L/SLEEVE", " Long Sleeve")
	SAPProductName = SAPProductName.replace(" L/Sleeve", " Long Sleeve")
	SAPProductName = SAPProductName.replace(" Led ", " LED ")
	SAPProductName = SAPProductName.replace(" LS ", " Long Sleeve ")
	SAPProductName = SAPProductName.replace(" Ls ", " Long Sleeve ")
	SAPProductName = SAPProductName.replace(" Mac ", " MAC ")
	SAPProductName = SAPProductName.replace(" Mvp ", " MVP ")
	SAPProductName = SAPProductName.replace(" Nba "," NBA ")
	SAPProductName = SAPProductName.replace(" Ncaa "," NCAA ")
	SAPProductName = SAPProductName.replace(" Nyc ", " NYC ")
	SAPProductName = SAPProductName.replace(" Of ", " of ")
	SAPProductName = SAPProductName.replace(" Og ", " OG ")
	SAPProductName = SAPProductName.replace(" Oht"," OHT")
	SAPProductName = SAPProductName.replace(" Pjs", " PJs")
	SAPProductName = SAPProductName.replace(" Po Hood", " Pullover Hood")
	SAPProductName = SAPProductName.replace(" Prca ", " PRCA ")
	SAPProductName = SAPProductName.replace(" Pull Over", " Pullover")
	SAPProductName = SAPProductName.replace(" Pvc ", " PVC ")
	SAPProductName = SAPProductName.replace(" S/S", " Short Sleeve ")
	SAPProductName = SAPProductName.replace(" S/SLEEVE", " Short Sleeve")
	SAPProductName = SAPProductName.replace(" S/Sleeve", " Short Sleeve")
	SAPProductName = SAPProductName.replace(" Sec "," SEC ")
	SAPProductName = SAPProductName.replace(" SS ", " Short Sleeve ") if "SS Track" not in SAPProductName else SAPProductName
	SAPProductName = SAPProductName.replace(" Ss ", " Short Sleeve ") if "Ss Track" not in SAPProductName else SAPProductName
	SAPProductName = SAPProductName.replace(" TDLR ", " Toddler ")
	SAPProductName = SAPProductName.replace(" Tdlr ", " Toddler ")
	SAPProductName = SAPProductName.replace(" The ", " the ")
	SAPProductName = SAPProductName.replace(" Tv ", " TV ")
	SAPProductName = SAPProductName.replace(" Twg2022 ", " TWG2022 ")
	SAPProductName = SAPProductName.replace(" Upf ", " UPF ")
	SAPProductName = SAPProductName.replace(" Uv ", " UV ")
	SAPProductName = SAPProductName.replace(" V ", " V ")
	SAPProductName = SAPProductName.replace(" v-neck", " V-neck")
	SAPProductName = SAPProductName.replace(" Vs ", " vs ")
	SAPProductName = SAPProductName.replace(" Wde ", " WDE ")
	SAPProductName = SAPProductName.replace(" With ", " with ")
	SAPProductName = SAPProductName.replace(" Wmns ", " Women's ")
	SAPProductName = SAPProductName.replace(" YTH ", " Youth ")
	SAPProductName = SAPProductName.replace(" Yth ", " Youth ")
	SAPProductName = SAPProductName.replace(" | the ", " | The ")
	SAPProductName = SAPProductName.replace("''", "\"") #If 2 apostrophe's are used for quotes.
	SAPProductName = SAPProductName.replace(",", " ")
	SAPProductName = SAPProductName.replace("--", "&mdash;")
	SAPProductName = SAPProductName.replace("-IN-", "-in-")
	SAPProductName = SAPProductName.replace("-In-", "-in-")
	SAPProductName = SAPProductName.replace("5Bbt", "5BBT")
	SAPProductName = SAPProductName.replace("\u00AE", "&reg;")
	SAPProductName = SAPProductName.replace("\u00BC", "1/4")
	SAPProductName = SAPProductName.replace("\u00BD", "1/2")
	SAPProductName = SAPProductName.replace("\u00BE", "3/4")
	SAPProductName = SAPProductName.replace("\u02BC", "'")
	SAPProductName = SAPProductName.replace("\u2013", "&ndash;")
	SAPProductName = SAPProductName.replace("\u2014", "&mdash;")
	SAPProductName = SAPProductName.replace("\u2018", "'")
	SAPProductName = SAPProductName.replace("\u2019", "'")
	SAPProductName = SAPProductName.replace("\u2019", "'") #Should be code for curly apostrophe (same as line above, but w/ actual unicode value).
	SAPProductName = SAPProductName.replace("\u201C", "\"")
	SAPProductName = SAPProductName.replace("\u201D", "\"")
	SAPProductName = SAPProductName.replace("\u2122", "&trade;")
	SAPProductName = SAPProductName.replace("Appalachain", "Appalachian")
	SAPProductName = SAPProductName.replace("Ara ", "ARA ")
	SAPProductName = SAPProductName.replace("Ark ", "ARK ")
	SAPProductName = SAPProductName.replace("Aub ", "AUB ")
	SAPProductName = SAPProductName.replace("Bass Master", "Bassmaster")
	SAPProductName = SAPProductName.replace("Bec ", "BEC ")
	SAPProductName = SAPProductName.replace("Bny ", "BNY ")
	SAPProductName = SAPProductName.replace("Bsm ", "BSM ")
	SAPProductName = SAPProductName.replace("Bws ", "BWS ")
	SAPProductName = SAPProductName.replace("Children'S", "Children's")
	SAPProductName = SAPProductName.replace("Col ", "COL ")
	SAPProductName = SAPProductName.replace("Csu ", "CSU ")
	SAPProductName = SAPProductName.replace("Dk Gray", "").replace("Lt Gray", "")
	SAPProductName = SAPProductName.replace("Fsu ", "FSU ")
	SAPProductName = SAPProductName.replace("Guarenteed", "Guaranteed")
	SAPProductName = SAPProductName.replace("Hovr ", "HOVR ")
	SAPProductName = SAPProductName.replace("Iphone", "IPhone")
	SAPProductName = SAPProductName.replace("Isu ", "ISU ")
	SAPProductName = SAPProductName.replace("Lcf ", "LCF ")
	SAPProductName = SAPProductName.replace("Loucity", "LouCity")
	SAPProductName = SAPProductName.replace("Louisville City Fc", "Louisville City FC")
	SAPProductName = SAPProductName.replace("Lsu ", "LSU ")
	SAPProductName = SAPProductName.replace("Lv", "LV")
	SAPProductName = SAPProductName.replace("Mbb ", "MBB ")
	SAPProductName = SAPProductName.replace("Men'S", "Men's")
	SAPProductName = SAPProductName.replace("Mens", "Men's")
	SAPProductName = SAPProductName.replace("Mi ", "MI ")
	SAPProductName = SAPProductName.replace("Mis ", "MIS ")
	SAPProductName = SAPProductName.replace("Msu ", "MSU ")
	SAPProductName = SAPProductName.replace("Mto ", "MTO ")
	SAPProductName = SAPProductName.replace("Muo ", "MUO ")
	SAPProductName = SAPProductName.replace("Nfl ", "NFL ")
	SAPProductName = SAPProductName.replace("Nfr ", "NFR ")
	SAPProductName = SAPProductName.replace(" Nil ", " NIL ")
	SAPProductName = SAPProductName.replace("Nyr ","NYRA ")
	SAPProductName = SAPProductName.replace("Nyra ","NYRA ")
	SAPProductName = SAPProductName.replace("Omi ", "OMI ")
	SAPProductName = SAPProductName.replace("Osfa ", "").replace("Osfm ", "")
	SAPProductName = SAPProductName.replace("Pit ", "PIT ")
	SAPProductName = SAPProductName.replace("Pitt Panters", "Pitt Panthers")
	SAPProductName = SAPProductName.replace("Pro Rodeo", "PRORODEO")
	SAPProductName = SAPProductName.replace("Product_Name","PRODUCT_NAME")
	SAPProductName = SAPProductName.replace("Prorodeo", "PRORODEO")
	SAPProductName = SAPProductName.replace("prorodeo", "PRORODEO")
	SAPProductName = SAPProductName.replace("ProRodeo", "PRORODEO")
	SAPProductName = SAPProductName.replace("Pur ", "PUR ")
	SAPProductName = SAPProductName.replace("Racing City Fc", "Racing City FC")
	SAPProductName = SAPProductName.replace("Racing Louisville Fc", "Racing Louisville FC")
	SAPProductName = SAPProductName.replace("Redhawk", "RedHawk")
	SAPProductName = SAPProductName.replace("Rlf ", "RLF ")
	SAPProductName = SAPProductName.replace("Rut ", "RUT ")
	SAPProductName = SAPProductName.replace("Sfa ", "SFA ")
	SAPProductName = SAPProductName.replace("Sleev ", "Sleeve ")
	SAPProductName = SAPProductName.replace("Syr ","SYR ")
	SAPProductName = SAPProductName.replace("T-Shi ", "T-Shirt ")
	SAPProductName = SAPProductName.replace("T-Shir ", "T-Shirt ")
	SAPProductName = SAPProductName.replace("Taa ", "TAA ")
	SAPProductName = SAPProductName.replace("Tar Heels Tar Heels", "Tar Heels")
	SAPProductName = SAPProductName.replace("Td Five", "TD Five")
	SAPProductName = SAPProductName.replace("They'Re", "They're")
	SAPProductName = SAPProductName.replace("Trk and Fld", "Track and Field")
	SAPProductName = SAPProductName.replace("Twg ", "TWG ")
	SAPProductName = SAPProductName.replace("Uco ", "UCO ")
	SAPProductName = SAPProductName.replace("Ucon ","UConn ")
	SAPProductName = SAPProductName.replace("Uconn ","UConn ")
	SAPProductName = SAPProductName.replace("Unc ", "UNC ")
	SAPProductName = SAPProductName.replace("Under Armor", "Under Armour")
	SAPProductName = SAPProductName.replace("Usa ", "USA ")
	SAPProductName = SAPProductName.replace("Usa Volleyball", "USA Volleyball")
	SAPProductName = SAPProductName.replace("Usav", "USAV")
	SAPProductName = SAPProductName.replace("Usavb", "USAVB")
	SAPProductName = SAPProductName.replace("Usv ", "USV ")
	SAPProductName = SAPProductName.replace("V-neck", "V-Neck")
	SAPProductName = SAPProductName.replace("Vip", "VIP")
	SAPProductName = SAPProductName.replace("Vneck", "V-Neck")
	SAPProductName = SAPProductName.replace("W/", "with")
	SAPProductName = SAPProductName.replace("Wcc ", "WCC ")
	SAPProductName = SAPProductName.replace("Wnba","WNBA")
	SAPProductName = SAPProductName.replace("Women'S", "Women's")
	SAPProductName = SAPProductName.replace("Womens", "Women's")
	SAPProductName = SAPProductName.replace("Woo Pig", "Wooo Pig")
	SAPProductName = SAPProductName.replace("Wvu ", "WVU ")
	SAPProductName = SAPProductName.replace(" ", " ")
	SAPProductName = SAPProductName.replace("®", "&reg;")
	SAPProductName = SAPProductName.replace("¼", "1/4")
	SAPProductName = SAPProductName.replace("¾", "3/4")
	SAPProductName = SAPProductName.replace("×", "x")
	SAPProductName = SAPProductName.replace("é", "e")
	SAPProductName = SAPProductName.replace("–", "&ndash;")
	SAPProductName = SAPProductName.replace("’", "'")
	SAPProductName = SAPProductName.replace("™", "&trade;")
	SAPProductName = SAPProductName.replace("�", " ")
	SAPProductName = SAPProductName.replace("�&trade;S", "'s")
	SAPProductName = SAPProductName.replace("�™S", "'s")
	SAPProductName = SAPProductName.replace("n'T", "n't")

	SAPProductName = SAPProductName.replace("\n", "")

	SAPProductName = SAPProductName.replace("'S ", "'s ")
	SAPProductName = SAPProductName.replace("   ", " ")
	SAPProductName = SAPProductName.replace("  ", " ")

	SAPProductName = SAPProductName.replace(" ALABAMA ", " Alabama ")
	SAPProductName = SAPProductName.replace(" ALASKA ", " Alaska ")
	SAPProductName = SAPProductName.replace(" ARIZONA ", " Arizona ")
	SAPProductName = SAPProductName.replace(" ARKANSAS ", " Arkansas ")
	SAPProductName = SAPProductName.replace(" CALIFORNIA ", " California ")
	SAPProductName = SAPProductName.replace(" COLORADO ", " Colorado ")
	SAPProductName = SAPProductName.replace(" CONNECTICUT ", " Connecticut ")
	SAPProductName = SAPProductName.replace(" DELAWARE ", " Delaware ")
	SAPProductName = SAPProductName.replace(" FLORIDA ", " Florida ")
	SAPProductName = SAPProductName.replace(" GEORGIA ", " Georgia ")
	SAPProductName = SAPProductName.replace(" HAWAII ", " Hawaii ")
	SAPProductName = SAPProductName.replace(" IDAHO ", " Idaho ")
	SAPProductName = SAPProductName.replace(" ILLINOIS ", " Illinois ")
	SAPProductName = SAPProductName.replace(" INDIANA ", " Indiana ")
	SAPProductName = SAPProductName.replace(" IOWA ", " Iowa ")
	SAPProductName = SAPProductName.replace(" KANSAS ", " Kansas ")
	SAPProductName = SAPProductName.replace(" KENTUCKY ", " Kentucky ")
	SAPProductName = SAPProductName.replace(" LOUISIANA ", " Louisiana ")
	SAPProductName = SAPProductName.replace(" MAINE ", " Maine ")
	SAPProductName = SAPProductName.replace(" MARYLAND ", " Maryland ")
	SAPProductName = SAPProductName.replace(" MASSACHUSETTS ", " Massachusetts ")
	SAPProductName = SAPProductName.replace(" MICHIGAN ", " Michigan ")
	SAPProductName = SAPProductName.replace(" MINNESOTA ", " Minnesota ")
	SAPProductName = SAPProductName.replace(" MISSISSIPPI ", " Mississippi ")
	SAPProductName = SAPProductName.replace(" MISSOURI ", " Missouri ")
	SAPProductName = SAPProductName.replace(" MONTANA ", " Montana ")
	SAPProductName = SAPProductName.replace(" NEBRASKA ", " Nebraska ")
	SAPProductName = SAPProductName.replace(" NEVADA ", " Nevada ")
	SAPProductName = SAPProductName.replace(" NEW HAMPSHIRE ", " New Hampshire ")
	SAPProductName = SAPProductName.replace(" NEW JERSEY ", " New Jersey ")
	SAPProductName = SAPProductName.replace(" NEW MEXICO ", " New Mexico ")
	SAPProductName = SAPProductName.replace(" NEW YORK ", " New York ")
	SAPProductName = SAPProductName.replace(" NORTH CAROLINA ", " North Carolina ")
	SAPProductName = SAPProductName.replace(" NORTH DAKOTA ", " North Dakota ")
	SAPProductName = SAPProductName.replace(" OHIO ", " Ohio ")
	SAPProductName = SAPProductName.replace(" OKLAHOMA ", " Oklahoma ")
	SAPProductName = SAPProductName.replace(" OREGON ", " Oregon ")
	SAPProductName = SAPProductName.replace(" PENNSYLVANIA ", " Pennsylvania ")
	SAPProductName = SAPProductName.replace(" RHODE ISLAND ", " Rhode Island ")
	SAPProductName = SAPProductName.replace(" SOUTH CAROLINA ", " South Carolina ")
	SAPProductName = SAPProductName.replace(" SOUTH DAKOTA ", " South Dakota ")
	SAPProductName = SAPProductName.replace(" TENNESSEE ", " Tennessee ")
	SAPProductName = SAPProductName.replace(" TEXAS ", " Texas ")
	SAPProductName = SAPProductName.replace(" UTAH ", " Utah ")
	SAPProductName = SAPProductName.replace(" VERMONT ", " Vermont ")
	SAPProductName = SAPProductName.replace(" VIRGINIA ", " Virginia ")
	SAPProductName = SAPProductName.replace(" WASHINGTON ", " Washington ")
	SAPProductName = SAPProductName.replace(" WEST VIRGINIA ", " West Virginia ")
	SAPProductName = SAPProductName.replace(" WISCONSIN ", " Wisconsin ")
	SAPProductName = SAPProductName.replace(" WYOMING ", " Wyoming ")
	SAPProductName = SAPProductName.replace(" alabama ", " Alabama ")
	SAPProductName = SAPProductName.replace(" alaska ", " Alaska ")
	SAPProductName = SAPProductName.replace(" arizona ", " Arizona ")
	SAPProductName = SAPProductName.replace(" arkansas ", " Arkansas ")
	SAPProductName = SAPProductName.replace(" california ", " California ")
	SAPProductName = SAPProductName.replace(" colorado ", " Colorado ")
	SAPProductName = SAPProductName.replace(" connecticut ", " Connecticut ")
	SAPProductName = SAPProductName.replace(" delaware ", " Delaware ")
	SAPProductName = SAPProductName.replace(" florida ", " Florida ")
	SAPProductName = SAPProductName.replace(" georgia ", " Georgia ")
	SAPProductName = SAPProductName.replace(" hawaii ", " Hawaii ")
	SAPProductName = SAPProductName.replace(" idaho ", " Idaho ")
	SAPProductName = SAPProductName.replace(" illinois ", " Illinois ")
	SAPProductName = SAPProductName.replace(" indiana ", " Indiana ")
	SAPProductName = SAPProductName.replace(" iowa ", " Iowa ")
	SAPProductName = SAPProductName.replace(" kansas ", " Kansas ")
	SAPProductName = SAPProductName.replace(" kentucky ", " Kentucky ")
	SAPProductName = SAPProductName.replace(" louisiana ", " Louisiana ")
	SAPProductName = SAPProductName.replace(" maine ", " Maine ")
	SAPProductName = SAPProductName.replace(" maryland ", " Maryland ")
	SAPProductName = SAPProductName.replace(" massachusetts ", " Massachusetts ")
	SAPProductName = SAPProductName.replace(" michigan ", " Michigan ")
	SAPProductName = SAPProductName.replace(" minnesota ", " Minnesota ")
	SAPProductName = SAPProductName.replace(" mississippi ", " Mississippi ")
	SAPProductName = SAPProductName.replace(" missouri ", " Missouri ")
	SAPProductName = SAPProductName.replace(" montana ", " Montana ")
	SAPProductName = SAPProductName.replace(" nebraska ", " Nebraska ")
	SAPProductName = SAPProductName.replace(" nevada ", " Nevada ")
	SAPProductName = SAPProductName.replace(" new hampshire ", " New Hampshire ")
	SAPProductName = SAPProductName.replace(" new jersey ", " New Jersey ")
	SAPProductName = SAPProductName.replace(" new mexico ", " New Mexico ")
	SAPProductName = SAPProductName.replace(" new york ", " New York ")
	SAPProductName = SAPProductName.replace(" north carolina ", " North Carolina ")
	SAPProductName = SAPProductName.replace(" north dakota ", " North Dakota ")
	SAPProductName = SAPProductName.replace(" ohio ", " Ohio ")
	SAPProductName = SAPProductName.replace(" oklahoma ", " Oklahoma ")
	SAPProductName = SAPProductName.replace(" oregon ", " Oregon ")
	SAPProductName = SAPProductName.replace(" pennsylvania ", " Pennsylvania ")
	SAPProductName = SAPProductName.replace(" rhode island ", " Rhode Island ")
	SAPProductName = SAPProductName.replace(" south carolina ", " South Carolina ")
	SAPProductName = SAPProductName.replace(" south dakota ", " South Dakota ")
	SAPProductName = SAPProductName.replace(" tennessee ", " Tennessee ")
	SAPProductName = SAPProductName.replace(" texas ", " Texas ")
	SAPProductName = SAPProductName.replace(" utah ", " Utah ")
	SAPProductName = SAPProductName.replace(" vermont ", " Vermont ")
	SAPProductName = SAPProductName.replace(" virginia ", " Virginia ")
	SAPProductName = SAPProductName.replace(" washington ", " Washington ")
	SAPProductName = SAPProductName.replace(" west virginia ", " West Virginia ")
	SAPProductName = SAPProductName.replace(" wisconsin ", " Wisconsin ")
	SAPProductName = SAPProductName.replace(" wyoming ", " Wyoming ")

	return SAPProductName

#List of words that presumably appear in the names of our lightest products that get the 13Oz minimum shipping weight:
listOf13OzKeywords = ["anti germ", " bow", " pen", " pom", "anti-germ", "applique", "badge", "ball marker", "bandana", "bandana", "bandanna", "bar blade", "barrette", "bib", "bloomer", "bobby pin", "bottle opener", "burp cloth", "buttons", "can cooler", "coaster", "collar", "collector pin", "collector's pin", "collectors pin", "collectors' pin", "coosie", "coozie", "corkscrew", "corkscrew", "coverall", "creeper", "crop top", "decal", "disposable paper", "dizzler", "doll", "emblem", "face cover", "face mask", "fan mask", "footies", "gaiter", "glove", "hair clip", "hair tie", "hairclip", "hairtie", "handkerchief", "hankie", "headband", "headcover", "hopper", "kerchief", "key chain", "key ring", "keychain", "keystrap", "koozie", "lanyard", "lapel pin", "lapel", "leash", "legging", "logo pin", "magnet", "marker", "mini helmet", "mitten", "neck tie", "neck warmer", "onesie", "oven mitt", "patch", "pencil", "pin set", "plush", "pot holder", "potholder", "raglan", "romper", "rooter", "sanitizer", "scarf", "scrunchie", "scrunchy", "serviette", "shaker", "shersey", "shirsey", "shirtsey", "shorts", "silk tie", "sleeper", "sock", "sticker", "stocking", "stylus", "switchblade", "sunglasses", "sun glasses", "t shirt", "t-shirt", "tackle twill", "tag", "tail tie", "tank", "tassel", "teddy fleece suit", "tee", "tights", "top", "towelette", "tubular bandana", "tubular bandanna", "wrist band", "wristband"]
listOf16OzKeywords = [" bag", " coin", " gem ", " oz ", "air pods", "aloha", "backpack", "backsack", "beanie", "belt", "blanket", "blazer", "blouse", "body suit", "bodysuit", "bracelet", "buckle", "bumper case", "button down", "button up", "buttondown", "canteen", "cap", "cardingan", "cart bag", "charger", "charm", "charming", "chaser", "cinch pack", "comforter", "crew neck", "crewneck", "cufflinks", "denim", "diaper cover", "dress", "duffel", "earbuds", "earring", "fanny", "flask", "flat bill", "flatbill", "fleece", "floral", "foam", "freezer pack", "gingham", "golf bag", "gymsack", "handbag", "hat", "hawaiian", "hoodie", "hoody", "hydra", "ice pack", "jeans", "jersey", "jewel", "jigsaw", "jogger", "journal", "knee pad", "kneepad", "knit cap", "knit hat", "laptop sleeve", "leotard", "license plate", "luggage strap", "mug", "necklace", "notebook", "organizer", "paddle", "pajama", "pant", "phone case", "pillow", "pj", "pocketbook", "polo", "poncho", "popover shirt", "poster", "pull over", "pullover", "purse", "puzzle", "rain jacket", "raincoat", "rainjacket", "saddlebag", "satchel", "shot glass", "shotglass", "sign", "slumber pants", "snap shirt", "sport coat", "sport jacket", "sports coat", "sports jacket", "stand bag", "stemless", "stopper", "sweater", "sweatpants", "sweats", "sweatshirt", "throw ", "timepiece", "toboggan", "tote", "towel", "travel case", "tumbler", "tunic", "turtleneck", "umbrella", "vest", "visor", "wallet", "watch", "wind shirt", "windshirt", "work shirt", "workshirt", "wristlet", "wristwatch", "year book", "yearbook", "yoga", "zip"]
listOf24OzKeywords = ["beer mug", "carafe", "decanter", "door mat", "doormat", "highball", "mixing glass", "official glass", "old fashioned", "pilsner" , "pint glass", "rocks glass", "seat cover", "snifter", "tire cover", "tire shade", "tv cover", "welcome mat", "welcomemat", "whiskey", "wine glass"]
listOf32OzKeywords = ["bleacher chair", "bleacher cushion", "bleacher seat", "bluetooth speaker", "coat", "cow bell", "grill cover", "jacket", "picnic caddy", "ping pong balls", "seat cushion", "seat pad", "shacket", "stadium  chair", "stadium  cushion", "stadium seat", "table tennis balls", "windbreaker"]
listOf40OzKeywords = ["tv cover"]
# 3lb
listOf48OzKeywords = [" art", " canvas", "bbq set", "display case", "framed", "freezer pack", "helmet", "ice pack", "photo", "picture", "plaque"]
# 3.5lb
#listOf56OzKeywords = []
# 4lb
listOf64OzKeywords = ["dog bed", "hitch"]
# 4.5lb
#listOf72OzKeywords = []
# 5lb
listOf80OzKeywords = ["clock"]
# 5.5lb
listOf88OzKeywords = ["beach chair", "camp chair", "collapsible chair", "folding chair"]
#Placeholders for heavier products:
# 6lb
#listOf96OzKeywords = []
# 6.5lb
#listOf104OzKeywords = []
# 7lb
#listOf112OzKeywords = []
# 7.5lb
#listOf120OzKeywords = []
# 8lb
#listOf128OzKeywords = []
# 8.5lb
#listOf136OzKeywords = []
# 9lb
#listOf144OzKeywords = []
# 9.5lb
#listOf152OzKeywords = []
# 10lb
listOf160OzKeywords = ["corn hole board", "cornhole board", "dart board", "tower game", "yard dice"]

allKeywordLists = allItemGroups = []
#Combine keyword & product line name lists into lists of all values. Used to exclude groups of values in function below.
allKeywordLists = listOf13OzKeywords + listOf16OzKeywords + listOf24OzKeywords + listOf32OzKeywords + listOf40OzKeywords + listOf48OzKeywords + listOf64OzKeywords + listOf80OzKeywords + listOf88OzKeywords + listOf160OzKeywords
allItemGroups = LIST_OF_13OZ_ITEM_GROUPS + LIST_OF_16OZ_ITEM_GROUPS + LIST_OF_24OZ_ITEM_GROUPS + LIST_OF_32OZ_ITEM_GROUPS + LIST_OF_40OZ_ITEM_GROUPS

def getWeightFromProductName(productObj):
	"""Searches product object input for keywords to assign a shipping weight  in ounces (per Sales Layer). Returns a float or None."""
	global listOf13OzKeywords, listOf16OzKeywords, listOf24OzKeywords, listOf32OzKeywords, listOf40OzKeywords, listOf48OzKeywords, listOf64OzKeywords, listOf80OzKeywords, listOf88OzKeywords, listOf160OzKeywords, allKeywordLists, allItemGroups
	productWeight = None
	#Check if any work in the product's name is in the listOf13OzKeywords but ensure the product line name isn't in the list of 16/24Oz product lines or other product keyword list.
	productName = productObj.ProductName.lower()
	productLineName = productObj.ProductLineName
	print(f"Searching for keywords for {productObj.ProductSKU}, {productName}, with product line name {productLineName}")
	#print(f"allKeywordLists: {allKeywordLists}\n")
	#print(f"allItemGroups: {allItemGroups}\n")
	#Create a list of all keywords EXCEPT those in the listOf13OzKeywords.
	otherKeywords = list(set(allKeywordLists).difference(listOf13OzKeywords))
	#print(f"otherKeywords: {otherKeywords}\n")
	#Create a list of all product line names EXCEPT those in the LIST_OF_13OZ_ITEM_GROUPS.
	otherItemGroups = list(set(allItemGroups).difference(LIST_OF_13OZ_ITEM_GROUPS))
	#print(f"otherItemGroups: {otherItemGroups}\n")
	#Check if keywords in the product name match to both the specific list for a weight and any other weights' lists:
	if any(word in productName for word in listOf13OzKeywords) and any(word in productName for word in otherKeywords):
		print(f"Word(s) in {productName} found in both {listOf13OzKeywords} and {otherKeywords}\n")
	#Check if any keyword for a weight is in the name but no other keywords for other weights exists:
	if any(word in productName for word in listOf13OzKeywords) and not any(word in productName for word in otherKeywords)\
	and productLineName not in otherItemGroups:
		productWeight = 13.0
		print(f"getWeightFromProductName()/13.0 matched keyword in {productObj.ProductName}")
	otherKeywords = list(set(allKeywordLists).difference(listOf16OzKeywords))
	otherItemGroups = list(set(allItemGroups).difference(LIST_OF_16OZ_ITEM_GROUPS))
	if any(word in productName for word in listOf16OzKeywords) and any(word in productName for word in otherKeywords):
		print(f"Word(s) in {productName} found in both {listOf16OzKeywords} and {otherKeywords}\n")
	if any(word in productName for word in listOf16OzKeywords) and not any(word in productName for word in otherKeywords)\
	and productLineName not in otherItemGroups:
		productWeight = 16.0
		print(f"getWeightFromProductName()/16.0 matched keyword in {productObj.ProductName}")
	otherKeywords = list(set(allKeywordLists).difference(listOf24OzKeywords))
	otherItemGroups = list(set(allItemGroups).difference(LIST_OF_24OZ_ITEM_GROUPS))
	if any(word in productName for word in listOf24OzKeywords) and any(word in productName for word in otherKeywords):
		print(f"Word(s) in {productName} found in both {listOf24OzKeywords} and {otherKeywords}\n")
	if any(word in productName for word in listOf24OzKeywords) and not any(word in productName for word in otherKeywords)\
	and productLineName not in otherItemGroups:
		productWeight = 24.0
		print(f"getWeightFromProductName()/24.0 matched keyword in {productObj.ProductName}")
	otherKeywords = list(set(allKeywordLists).difference(listOf32OzKeywords))
	otherItemGroups = list(set(allItemGroups).difference(LIST_OF_32OZ_ITEM_GROUPS))
	if any(word in productName for word in listOf32OzKeywords) and any(word in productName for word in otherKeywords):
		print(f"Word(s) in {productName} found in both {listOf32OzKeywords} and {otherKeywords}\n")
	if any(word in productName for word in listOf32OzKeywords) and not any(word in productName for word in otherKeywords)\
	and productLineName not in otherItemGroups:
		productWeight = 32.0
		print(f"getWeightFromProductName()/32.0 matched keyword in {productObj.ProductName}")
	otherKeywords = list(set(allKeywordLists).difference(listOf40OzKeywords))
	otherItemGroups = list(set(allItemGroups).difference(LIST_OF_40OZ_ITEM_GROUPS))
	if any(word in productName for word in listOf40OzKeywords) and any(word in productName for word in otherKeywords):
		print(f"Word(s) in {productName} found in both {listOf40OzKeywords} and {otherKeywords}\n")
	if any(word in productName for word in listOf40OzKeywords) and not any(word in productName for word in otherKeywords)\
	and productLineName not in otherItemGroups:
		productWeight = 40.0
		print(f"getWeightFromProductName()/40.0 matched keyword in {productObj.ProductName}")
	otherKeywords = list(set(allKeywordLists).difference(listOf48OzKeywords))
	#Note: no corresponding item group.
	if any(word in productName for word in listOf48OzKeywords) and any(word in productName for word in otherKeywords):
		print(f"Word(s) in {productName} found in both {listOf48OzKeywords} and {otherKeywords}\n")
	if any(word in productName for word in listOf48OzKeywords) and not any(word in productName for word in otherKeywords)\
	and productLineName not in allItemGroups:
		productWeight = 48.0
		print(f"getWeightFromProductName()/48.0 matched keyword in {productObj.ProductName}")
	otherKeywords = list(set(allKeywordLists).difference(listOf64OzKeywords))
	#Note: no corresponding item group.
	if any(word in productName for word in listOf64OzKeywords) and any(word in productName for word in otherKeywords):
		print(f"Word(s) in {productName} found in both {listOf64OzKeywords} and {otherKeywords}\n")
	if any(word in productName for word in listOf64OzKeywords) and not any(word in productName for word in otherKeywords)\
	and productLineName not in allItemGroups:
		productWeight = 64.0
		print(f"getWeightFromProductName()/64.0 matched keyword in {productObj.ProductName}")
	otherKeywords = list(set(allKeywordLists).difference(listOf80OzKeywords))
	#Note: no corresponding item group.
	if any(word in productName for word in listOf80OzKeywords) and any(word in productName for word in otherKeywords):
		print(f"Word(s) in {productName} found in both {listOf80OzKeywords} and {otherKeywords}\n")
	if any(word in productName for word in listOf80OzKeywords) and not any(word in productName for word in otherKeywords)\
	and productLineName not in allItemGroups:
		productWeight = 80.0
		print(f"getWeightFromProductName()/80.0 matched keyword in {productObj.ProductName}")
	otherKeywords = list(set(allKeywordLists).difference(listOf88OzKeywords))
	#Note: no corresponding item group.
	if any(word in productName for word in listOf88OzKeywords) and any(word in productName for word in otherKeywords):
		print(f"Word(s) in {productName} found in both {listOf88OzKeywords} and {otherKeywords}\n")
	if any(word in productName for word in listOf88OzKeywords) and not any(word in productName for word in otherKeywords)\
	and productLineName not in allItemGroups:
		productWeight = 88.0
		print(f"getWeightFromProductName()/88.0 matched keyword in {productObj.ProductName}")
	otherKeywords = list(set(allKeywordLists).difference(listOf160OzKeywords))
	#Note: no corresponding item group.
	if any(word in productName for word in listOf160OzKeywords) and any(word in productName for word in otherKeywords):
		print(f"Word(s) in {productName} found in both {listOf160OzKeywords} and {otherKeywords}\n")
	if any(word in productName for word in listOf160OzKeywords) and not any(word in productName for word in otherKeywords)\
	and productLineName not in allItemGroups:
		productWeight = 160.0
		print(f"getWeightFromProductName()/160.0 matched keyword in {productObj.ProductName}")
	#Exceptions and call outs:
	if not bool(productWeight):
		if (("applique" in productName) and ("fleece" in productName)):
			productWeight = 16.0
			print(f"getWeightFromProductName()/16.0 EXCEPTION CHECK matched keyword in {productObj.ProductName}")
	return productWeight

def assignSportsTeamAndMemorabilia(productObj):
	"""Primarily scans the product name to set additional product obj attr: Sports Team (also check property tag), and Memoribilia attributes. Returns the product object"""
	#This function is intended to be a final scan of the product name to set multiple attributes and may be extended to set additional attributes in the future (01/12/23).
	productName = productObj.ProductName.lower()
	propTag = productObj.ProdTags
	#Note we currently don't manage BEC (01/12/23):
	#Check if any of the team names from the official list are in the product name and whether the property tag indicates it's a "conference" product.
	#print(TEAM_NAME_LIST)
	if (propTag == "BEC" or propTag == "WCC") and any(word in productName for word in TEAM_NAME_LIST):
		for teamName in TEAM_NAME_LIST:
			if teamName in productName:
				print(f"Team found for {productName}: {teamName}")
				#Get the normalized team name from the 
				productObj.SportsTeam = TEAM_NAMES[teamName]
				print(productObj.SportsTeam, type(productObj.SportsTeam))
	else:
		productObj.SportsTeam = None
	if any(word in productName for word in MEMORABILIA_TERMS):
		productObj.Memorabilia = True
	else:
		productObj.Memorabilia = False
	return productObj

if __name__ == "__main__":
	from Product_Class import *
	origPrice = "50.01"
	testProduct = productClass("ARKM100282", "Mens>Outerwear", "Arkansas Razorbacks Take Your Time 1/4 Zip Windshirt", ["PRODUCT", "All Product", "New Arrivals"], ["PRODUCT", "ALL ", "NEWA01"], "", "ARK", origPrice, "", "0", "ARKM100282.jpg", "Colosseum", "26", "Adult", "Men", "No", "True", "SP23", "Wiffle Ball", "False", "", "", "", "", "", "", "", "", "NationalWiffleBallPlayOffs", "", "", "Imported", "WSD", "", "", "0", "16.0", "Default Tax Class", "PC040100", "Default Tax Class", "", "", "2", "", "", "", "", "V500027", "COUZ11523W", "Mens", "LONG SLEEVE", "MENS", "", "Variant", "arkansas-razorbacks-take-your-time-1-4-zip-windshirt-ARKM100282", "Fleece, pullover, sweats, hoodie, windshirt, sweatshirt, wind shirt, sweat shirt, pull over, 1/4 zip, quarter zip, Shep Shirt, Shepshirt, Colosseum", ",New,White,Men,Adult", "Age>Adult;Gender>Men;Color>White;Origin>Imported", "07/15/22", "20.70", "Yes", True, True, ["999"], True, ["XS", "S", "M", "L", "XL", "2XL"], ["Multi"], "TestProductLineName")
	#testKeywords = generateOnsiteSearchKeywords(testProduct)
	#print(f"testKeywords: {testKeywords}")
