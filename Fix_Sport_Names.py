#!/usr/bin/python3

def fixSportName(sport):
	sport = "".join(list(filter(str.isalpha, sport))) #09/16/22 Remove any numbers from input.
	if ("band") not in sport.lower():
		sport = sport.replace("AND", " & ")
	sport = sport.title()
	sport = sport.replace("Nfr", "").replace(" And ", " & ").replace("Oht", "").replace("Myaamia", "")
	sport = sport.replace("Belmont", "Equestrian").replace("Saratoga", "Equestrian").replace("Ice Hockey", "Hockey").replace("Figureskating", "Figure Skating")
	sport = sport.replace("Crosscountry", "Cross Country").replace("Synchronizedskating", "Synchronized Skating").replace("Fieldhockey", "Field Hockey").replace("Icehockey", "Ice Hockey").replace("Beachvolleyball", "Beach Volleyball")
	sport = sport.replace("Tugofwar", "Tug of War").replace("Wheelchairrugby", "Wheelchair Rugby").replace("Rollersports", "Roller Sports").replace("Flyingdisc", "Flying Disc").replace("Muaythai", "Muay Thai").replace("Flagfootball", "Flag Football")
	sport = sport.replace("Orienteeing", "Orienteering").replace("Beachh and Ball", "Beach & Ball").replace("Dualthon", "Duathlon").replace("Airsports", "Air Sports")
	sport = sport.replace("Sportclimbing", "Sport Climbing").replace("Sideline", "").replace("Evergreen", "").replace("Bec", "").replace("Conferencechamps", "")
	sport = sport.replace("Seasons", "").replace("Pitchingribby", "").replace("Vault", "").replace("Classic", "").replace("Blackhistory", "").replace("Dance Sport", "Dancesport")
	sport = sport.replace("Holiday", "").replace("Bec", "").replace("Auburnvault", "").replace("Swingingjonathan", "").replace("Wcc", "").replace("Fall", "")
	sport = sport.replace("Twg", "").replace("Pride", "").replace("Realtree", "").replace("Aod", "").replace("Military", "").replace("Starkvegas", "")
	sport = sport.replace("Consignment", "").replace("Fin Swimming", "Finswimming").replace("Floor Ball", "Floorball").replace("Samforddonahue", "")
	sport = sport.replace("Worldgames", "").replace("Bny", "Cycling").replace("Flying Disk", "Flying Disc").replace("Graduation", "").replace("Ju-Jitsu", "Jujitsu")
	sport = sport.replace("Life Saving", "Lifesaving").replace("Muay-Thai", "Muay Thai").replace("Power Lifting", "Powerlifting")
	sport = sport.replace("Rollersports", "Roller Sports").replace("SAMFORDDONAHUE", "").replace("Sotball", "Softball").replace("Swingingaubie", "")
	sport = sport.replace("Titleix", "").replace("Trackfield", "Track & Field").replace("Travers", "")
	sport = sport.replace("Wake Boarding", "Wakeboarding").replace("Wrangler", "").replace("Bowl", "Bowling").replace("Wheel Chair Rugby", "Wheelchair Rugby")
	sport = sport.replace("Prca", "").replace("Johnnymajors", "").replace("Womenssoccer", "").replace("Baseballaubie", "").replace("Swimdive", "Swimming & Diving")
	sport = sport.replace("Statepride", "").replace("Alumni", "").replace("Speedlimit", "").replace("Sportdrop", "").replace("Vintage", "")
	sport = sport.replace("Mom", "").replace("Dad", "").replace("Gr and Parent", "").replace("Staffuniforms", "").replace("Wso", "")
	sport = sport.replace("Farmstrong", "").replace("Oldaggie", "").replace("Onfield", "").replace("Stalwart", "").replace("Wholesale", "")
	sport = sport.replace("Jordan", "").replace("Womensbasketball", "").replace("Aubie", "").replace("Stadium", "")
	return sport

def compileSLProductSportsList(saleLayerProductObj, SAPVariantObj):
	""""""
	saleLayerProductObj.Sport.append(SAPVariantObj.ProductCollection)
	return saleLayerProductObj