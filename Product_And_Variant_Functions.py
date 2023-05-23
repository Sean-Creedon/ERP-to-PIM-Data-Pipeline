#!/usr/bin/python3

#Use SPORTS to find sports in names and limit what appears in SL product names when filtering "pick-a-sport" products to make them "sport agnostic" (replace the sport substring with "Pick-a-Sport").
from Constants import *
#
from SAP_Data_Class import *
from Product_Class import *
from Variant_Class import *

#Will need a back up func to pull sport from name if field is blank.
def findSportInProductName(productName):
	"""Checks input product name against a list of sports, assigns & returns any found sport name to a variable. Returns None when no match found."""
	#print(f"Checking for sport in product named: {productName}")
	associatedSport = None
	for sport in SPORTS:
		if (productName.startswith(f" {sport}")) or (f" {sport} " in productName) or (productName.endswith(f" {sport}")):
			#print(f"Sport {sport} found in {productName}")
			associatedSport = sport
	return associatedSport

def fixSportName(sport):
	sport = "".join(list(filter(str.isalpha, sport))) #09/16/22 Remove any numbers from input.
	if ("band") not in sport.lower():
		sport = sport.replace("AND", " & ")
	sport = sport.replace("Track", "Track & Field") if sport == "Track" else sport
	sport = sport.title()
	sport = sport.replace("Nfr", "").replace(" And ", " & ").replace("Oht", "").replace("Myaamia", "")
	sport = sport.replace("Belmont", "Equestrian").replace("Saratoga", "Equestrian").replace("Ice Hockey", "Hockey").replace("Figureskating", "Figure Skating")
	sport = sport.replace("Crosscountry", "Cross Country").replace("Synchronizedskating", "Synchronized Skating").replace("Fieldhockey", "Field Hockey").replace("Icehockey", "Ice Hockey").replace("Beachvolleyball", "Beach Volleyball")
	sport = sport.replace("Tugofwar", "Tug of War").replace("Wheelchairrugby", "Wheelchair Rugby").replace("Rollersports", "Roller Sports").replace("Flyingdisc", "Flying Disc").replace("Muaythai", "Muay Thai").replace("Flagfootball", "Flag Football")
	sport = sport.replace("Orienteeing", "Orienteering").replace("Beachh and Ball", "Beach & Ball").replace("Dualthon", "Duathlon").replace("Airsports", "Air Sports")
	sport = sport.replace("Sportclimbing", "Sport Climbing").replace("Sideline", "").replace("Evergreen", "").replace("Bec", "").replace("Conferencechamps", "")
	sport = sport.replace("Seasons", "").replace("Pitchingribby", "").replace("Vault", "").replace("Classic", "").replace("Blackhistory", "").replace("Dance Sport", "Dancesport")
	sport = sport.replace("Holiday", "").replace("Bec", "").replace("Auburnvault", "").replace("Swingingjonathan", "").replace("Wcc", "").replace("Fall", "")
	sport = sport.replace("Twg", "").replace("Pride", "").replace("Realtree", "").replace("Aod", "").replace("Military", "").replace("Starkvegas", "").replace("Track & Field & Field", "")
	sport = sport.replace("Consignment", "").replace("Fin Swimming", "Finswimming").replace("Floor Ball", "Floorball").replace("Samforddonahue", "")
	sport = sport.replace("Worldgames", "").replace("Bny", "Cycling").replace("Flying Disk", "Flying Disc").replace("Graduation", "").replace("Ju-Jitsu", "Jujitsu")
	sport = sport.replace("Life Saving", "Lifesaving").replace("Muay-Thai", "Muay Thai").replace("Power Lifting", "Powerlifting").replace("Sxonly", "")
	sport = sport.replace("Rollersports", "Roller Sports").replace("SAMFORDDONAHUE", "").replace("Sotball", "Softball").replace("Swingingaubie", "").replace("Custom", "")
	sport = sport.replace("Titleix", "").replace("Trackfield", "Track & Field").replace("Travers", "").replace("Travers", "")
	sport = sport.replace("Wake Boarding", "Wakeboarding").replace("Wrangler", "").replace("Bowl", "Bowling").replace("Wheel Chair Rugby", "Wheelchair Rugby")
	sport = sport.replace("Prca", "").replace("Johnnymajors", "").replace("Womenssoccer", "").replace("Baseballaubie", "").replace("Swimdive", "Swimming & Diving")
	sport = sport.replace("Statepride", "").replace("Alumni", "").replace("Speedlimit", "").replace("Sportdrop", "").replace("Vintage", "").replace("Iconic", "")
	sport = sport.replace("Mom", "").replace("Dad", "").replace("Gr and Parent", "").replace("Staffuniforms", "").replace("Wso", "").replace("Gameday", "")
	sport = sport.replace("Farmstrong", "").replace("Oldaggie", "").replace("Onfield", "").replace("Stalwart", "").replace("Wholesale", "").replace("Champs", "")
	sport = sport.replace("Jordan", "").replace("Womensbasketball", "").replace("Aubie", "").replace("Stadium", "").replace("Onfield", "").replace("Csuw", "")
	sport = sport.replace("Equestrianstakes", "").replace("Bowlingbound", "").replace("Uniform", "").replace("Bowlingchamps", "").replace("Aqueduct", "Equestrian")
	sport = sport.replace("Essentials", "").replace("Elite", "").replace("Wlacrosse", "Lacrosse").replace("Spartanstrong", "").replace("Junior", "").replace("Highschool", "")
	sport = sport.replace("Preakness", "Equestrian").replace("Cradleofcoaches", "")
	return sport

def assignProductOrVariantSport(SAPProductObj, SLProductOrVariantObj):
	"""Uses SAP Product obj's ProductCollection attr to set Sales Layer Product obj's Sport attr OR Variant obj's VariantSport attr."""
	possibleProductSport = fixSportName(SAPProductObj.ProductCollection)
	SAPProductAssignedSport = possibleProductSport if possibleProductSport in SPORTS else None
	productName = SAPProductObj.ItemDescription.title()#Use original SAP var name converted to title case (no way to reliably use SL product name w/ all replacements/corrections??).
	#Get correct attribute name depending on whether input is prod or var class:
	#print("\nassignProductOrVariantSport:", productName, type(SLProductOrVariantObj), SAPProductAssignedSport, sep = "\t")
	if not bool(SAPProductAssignedSport):
		#print("SAP sport value NOT found; searching name:", productName, sep="\t")
		SAPProductAssignedSport = findSportInProductName(productName)
	#Set sport to None if no sport found in SAP obj Product Collection attr or if sport not in SPORTS list constant.
	SAPProductAssignedSport = SAPProductAssignedSport if (bool(SAPProductAssignedSport) and SAPProductAssignedSport in SPORTS) else None
	if isinstance(SLProductOrVariantObj, productClass):
		SLProductOrVariantObj.Sport = [SAPProductAssignedSport]
	else:
		SLProductOrVariantObj.VariantSport = SAPProductAssignedSport
	return SLProductOrVariantObj

def compileSLProductSportsList(saleLayerProductObj, SAPVariantObj):
	""""""
	#Use list data type in all cases (even for single sport)? Return None if no sport?
	productSportList = saleLayerProductObj.Sport
	newSAPSport = SAPVariantObj.ProductCollection
	SAPVariantName = SAPVariantObj.ItemDescription
	#Get the SAP obj's sport value if it exists, otherwise search the SAP variant's name:
	newProductSport = fixSportName(newSAPSport) if (bool(newSAPSport)) else findSportInProductName(SAPVariantName)
	#If the new SAP data/variant obj has a sport value, the sport value is in the "official" list of SPORTS, and isn't already in the SL prod obj list of sports:
	if (bool(newProductSport)) and (newProductSport in SPORTS) and (newProductSport not in productSportList):
		productSportList.append(newProductSport)
	return saleLayerProductObj

#To be imported into Product and Variant Classes to set size and color lists to None.
def setEmptyListsToNone(inputList):
	"""Removes empty/None values from input list. Return either the list if it still contains values or None if the list is empty or only empty strings."""
	inputList = list(filter(None, inputList))#Remove empties.
	return inputList if any(inputList) else None

