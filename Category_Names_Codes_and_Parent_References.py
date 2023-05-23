"""A collection of dictionaries for translating product categorys names to codes and for assigning duplicated category names to correct parent category."""

#"Major" parent category name/codes:
primaryParentCategories = {
	"PRODUCT": "PRODUCT",
	"Men": "MENS01",
	"Women": "WOME01",
	"Youth": "YOUT01",
	"Headwear": "HEAD01",
	"Gifts & Accessories": "GIFT01",
	"Jerseys": "JERS02",
	"Shop Sport": "SPORTSP",
	"Special Collection": "SPEC01",
	"Events": "EVE21",
	"Bowls": "BOWLS"
}

parentCategoryNameList = primaryParentCategories.keys()

#"All Product" parent category name/codes:
PRODUCT = {
	"PRODUCT": "PRODUCT", #Parent Category
	"All Product": "ALL",
	"New Arrivals": "NEWA01",
	"All Outerwear": "OUTER",
	"All Long Sleeves": "ALLLS",
	"All Footwear": "ALLFTW",
	"Dropship & Non-Discount": "DSND21",
	"All Short Sleeve": "SHRTSLV"
}

Men = {
	"Men": "MENS01", #Parent Category
	"T-Shirts & Tanks": "METS01",
	"Short Sleeve": "MTST01",
	"Long Sleeve": "MTST02",
	"Sweatshirts": "MENS02",
	"Crewneck": "MESW01",
	"Hoodies": "MESW02",
	"Polos & Shirts": "MEPO01",
	"Polos": "POLO01",
	"Shirts": "MSRT01",
	"Outerwear": "MENS03",
	"Jackets": "JACK04",
	"Sweaters": "JACK05",
	"Vests": "VEST02",
	"Pullovers": "MEOU01",
	"Footwear": "MFTW01",
	"Socks": "SOCK02",
	"Shoes": "SHOEO2",
	"Bottoms": "MBTM01",
	"Pants": "MEPA01",
	"Shorts": "MESH01",
	"Pajama Bottoms": "MEPA2"
}

Women = {
	"Women": "WOME01", #Parent Category
	"Tees & Tops": "WOTE01",
	"Long Sleeve": "WTTL01",
	"Short Sleeve": "WTTS01",
	"Outerwear": "WOME02",
	"Sweaters": "SWEA04",
	"Vests": "VEST04",
	"Pullovers": "WOOU01",
	"Jackets": "WJKT01",
	"Dresses": "DRES01",
	"Sweatshirts": "WSWT01",
	"Crewneck": "WCRW01",
	"Hoodies": "WHDS01",
	"Polos & Shirts": "WPOL01",
	"Shirts": "WPOL02",
	"Polos": "WPOL03",
	"Fashion": "WFAS01",
	"Footwear": "WFTW01",
	"Socks": "SOCK03",
	"Shoes": "SHOEO3",
	"Bottoms": "WOBO01",
	"Pajama Bottoms": "PAJA02",
	"Shorts": "WOSH01",
	"Pants": "WOPA01",
	"Tights & Leggings": "WOTL01",
	"Skirts": "WOSK01"
}

Youth = {
	"Youth": "YOUT01", #Parent Category
	"Dresses": "YODR01",
	"Hats": "HATS01",
	"Polos & Shirts": "POLO02",
	"Shirts": "SHIR01",
	"Polos": "POLO08",
	"Accessories": "ACCE01",
	"Sweatshirts": "YOSW",
	"Crewneck": "YOCR01",
	"Hoodies": "YOHO01",
	"Outerwear": "YOOU01",
	"Jackets": "JACK03",
	"Sweaters": "SWEA05",
	"Vests": "VEST03",
	"Pullovers": "YOPU01",
	"Tees & Tops": "YOTE01",
	"Long Sleeve": "YOLS01",
	"Short Sleeve": "YTTS01",
	"Footwear": "YOFT01",
	"Shoes": "SHOEO4",
	"Socks": "SOCK04",
	"Bottoms": "YOBO01",
	"Pajama Bottoms": "PAJA01",
	"Tights & Leggings": "YOTL01",
	"Pants": "YOPA01",
	"Shorts": "YOSH01",
	"Skirts": "YODS01",
	"Outfits": "YOOT01"
}

Headwear = {
	"Headwear": "HEAD01", #Parent Category
	"Adjustable": "HEAD02",
	"Fitted": "HEFI01",
	"Flex": "HEFL01",
	"Knit": "HEKN01",
	"Visors & Headbands": "HEVH01"
}


#Novelties
GiftsAndAccessories = {
	"Gifts & Accessories": "GIFT01", #Parent Category
	"Bags": "GABA02",
	"Backpacks": "BABA01",
	"Totes": "BATO01",
	"Handbags & Wallets": "BAHW01",
	"Luggage & Travel": "BALT01",
	"Home & Office": "GIAC01",
	"Holiday": "HOLI02",
	"Home Decor": "GAHO01",
	"Autograph Memorabilia": "GAHO02",
	"Flags": "GAHO03",
	"Wall Art": "GAHO04",
	"Banners": "GABA01",
	"Cell Phone Accessories": "HOPA01",
	"Stickers & Tattoos": "HOST01",
	"Bed & Bath": "HOBB01",
	"Collectibles": "HOCO01",
	"Magnets": "HOMA01",
	"Tailgate Gear": "GIAC02",
	"Balls & Games": "BALL01",
	"Buttons & Pins": "BUTT01",
	"Grilling": "GATG01",
	"Stadium Accessories": "GATG02",
	"Poms": "POMS01",
	"Seat Cushions": "SEAT01",
	"Miscellaneous": "GIAC03",
	"Sporting Equipment": "GIAC04",
	"Helmets": "SPHE01",
	"Golf Gear": "GOLF01",
	"Balls": "GASE01",
	"Auto": "GIAC05",
	"Flags": "AUFL01",
	"Magnets": "AUMA01",
	"Accessories": "AUAC01",
	"License Plates": "LICE01",
	"Decals": "GIAC06",
	"Personal Accessories": "GIAC07",
	"Hair Accessories": "PEHA01",
	"Umbrellas": "PEUM01",
	"Lanyards": "PELA01",
	"Sunglasses": "PESU01",
	"Gloves & Scarves": "PEGS01",
	"Watches": "PEWA01",
	"Buttons & Pins": "PABP01",
	"Jewelry": "JEWE01",
	"Keychains": "GAPA01",
	"Drinkware": "GIAC08",
	"Mugs": "DRMU01",
	"Tumblers": "TUMB01",
	"Stemware": "STEM01",
	"Coozies": "COOZ01",
	"Water Bottles": "WATE01",
	"Shot Glasses": "SHOT02",
	"Pint Glasses": "PINT01",
	"Toys & Games": "GIAC09",
	"Pet Accessories": "PETS"
}

Jerseys = {
	"Jerseys": "JERS02", #Parent Category
	"Adult": "ADUL01",
	"Youth": "YTJS01"
}

ShopSports = {
	"Shop Sports": "SPORTSP", #Parent Category
	"Band": "BAND01",
	"Baseball": "BASEBL",
	"Basketball": "BASKBL",
	"Cheer": "CHEER",
	"Cross Country": "XCOUNT",
	"Dance": "DANCE1",
	"Football": "FUTBLL",
	"Gymnastics": "GYMNAS",
	"Lacrosse": "LAXOSS",
	"Soccer": "SOCCER",
	"Softball": "SOFTBL",
	"Swimming & Diving": "SWMDIV",
	"Track & Field": "TRKFLD",
	"Volleyball": "VLYBLL",
	"Wrestling": "WRSTLG",
	"Golf": "GOLF",
	"Hockey": "HOCKEY",
	"Tennis": "SPTENN",
	"Rowing": "ROW",
	"Fencing": "FENCING"
}

SpecialCollection = {
	"Special Collection": "SPEC01", #Parent Category
	"Art Of The Kentucky Derby": "ART01",
	"Shop By Sport": "SHBY01",
	"Clearance": "CLEA01",
	"Ohio State Buckeyes": "OHST01",
	"2021 Gear": "202101",
	"Clemson Tigers": "CLEM01",
	"Matchup": "MATC01",
	"Graduation": "GRAD21",
	"Mother's Day": "MOTH21",
	"2022 Kit Collection": "KITCO22",
	"Lumberjacks Summer": "LUSUM21",
	"Pride Collection": "PRD21",
	"Father's Day": "FATH21",
	"BIG EAST Championships": "BECHAMPS",
	"Vault": "VAULT1",
	"Game Worn": "GAMEWOR",
	"SEC Basketball": "SECBB1",
	"Final Four": "FINAL4",
	"Women's Cup": "WOCU21",
	"SALE": "SALE",
	"Delaware Blue Hens": "DEL21",
	"Ole Miss Rebels": "OMI21",
	"Game Day": "GMED21",
	"College Color Days": "CCD21",
	"USAV Authentics": "USAVAUTH",
	"18 Collection": "SPD18",
	"Eli Manning Collection": "10COL",
	"Black Friday 2021": "BF2021",
	"Cyber Monday": "CYM2021",
	"Holiday Gift Guide": "HGG2021",
	"Football": "FB01",
	"St. Patricks Day": "STPTK",
	"Kentucky Derby Festival": "KDF22",
	"Spring Sports": "SSports1",
	"LCFC Academy": "LCAC22",
	"OHT": "OHT",
	"Yosef": "Yosef",
	"Fan Cave": "FNCV22",
	"Best Sellers": "BESTSLR22",
	"Beach Volleyball": "BCHVB",
	"Rex Collection	T-Rex Collection": "T",
	"Post Season Gear": "PSTSPRTS22",
	"Americana Collection": "MERCANA22",
	"CWS Champs Gear": "CWSCHMP22",
	"Rutgers Scarlet Knights": "TOPRUT",
	"Collage Collection": "COLCOL",
	"High School Championship": "HISCHOOL",
	"Pick-A-Sport": "PICK",
	"Back to School": "B2SCH",
	"USA Volleyball Logo": "USVLOGO",
	"Fill the Fam": "FTFAM",
	"Rodeo Quincy": "ROQUIN",
	"Breast Cancer Awareness '22": "BCAW22",
	"Realtree WAV3": "RLTRWV",
	"Holiday Season": "HLDYSZN",
	"Holiday Deals": "HOLIDEALS",
	"NFR Champions": "NFRCHAMP",
	"Liberty Bowl Champs": "LBCHAMPS22",
	"Texas Bowl Champs": "TXBWLCHAMPS",
	"Sun Bowl Champs": "SNBWLCHAMPS",
	"Valentine's Day": "VALENTINE",
	"2023 Kit Collection": "2023KIT",
	"Retro Collection": "RETRO",
	"Belmont Stakes 2023": "BelST23",
	"Essentials Collection": "ESSENTIAL"
}

Events = {
	"Events": "EVE21", #Parent Category
	"Saratoga": "SAR21",
	"NYRA": "NYR21",
	"Belmont Stakes": "BEL21",
	"Belmont Park": "BELP21",
	"Aqueduct": "AQU21",
	"Travers Stakes": "TRV21"
}

Bowls = {
	"Bowls": "BOWLS", #Parent Category
	"Vrbo Fiesta Bowl": "FIBOWL",
	"TCU": "FIB1",
	"Michigan": "FIB2",
	"TCU V Michigan": "FIB3",
	"Vrbo Fiesta Bowl Champs": "FIB4",
	"Military Bowl": "MIBOWL",
	"Boston College": "MIB1",
	"ECU": "MIB2",
	"Boston College V ECU": "MIB3",
	"Music City Bowl": "MCBOWL",
	"Purdue": "MCB1",
	"Tennessee": "MCB2",
	"Purdue V Tennessee": "MCB3",
	"Arizona Bowl": "AZBOWL",
	"Central Michigan": "AZB1",
	"Boise State": "AZB2",
	"Central Michigan V Boise State": "AZB3",
	"Sugar Bowl": "SGBOWL",
	"Alabama": "SGB1",
	"Kansas State": "SGB2",
	"Kansas State V Alabama": "SGB3",
	"Sugar Bowl Champs": "SGBWLCHAMPS",
	"Guaranteed Rate Bowl": "GRBOWL",
	"Wisconsin": "GRB1",
	"Oklahoma State": "GRB2",
	"Wisconsin V Oklahoma State": "GRB3",
	"Guaranteed Rate Bowl Champs": "GRB4"
}

#Categories without Parent Categories:
miscellaneousCategories = {
	"Post Season Gear": "PSTSZN22",
	"SFA Authentics": "SFAA01",
	"Blue Hen's Authentics": "BLHN01",
	"Adidas": "ADID01",
	"TWG Sports": "SPSP21",
	"Nike": "NIKE01",
	"Kelsey Robinson": "TOK20",
	"Big Ten": "BIG10",
	"Michigan State": "MSU",
	"SEC": "SEC",
	"BIG 12": "BIG12",
	"PAC-12": "PAC12",
	"ACC": "ACC",
	"Sun Belt": "SBELT",
	"Coastal Carolina": "COASC",
	"AAC": "AAC",
	"SMU": "SMU",
	"Independent": "IND",
	"BYU": "BYU",
	"ASUN": "ASUN",
	"MWC": "MTNWST",
	"MAC": "MIDAM",
	"C-USA": "CUSA",
	"Apparel": "BASMAPP",
	"Scarves": "SCARF",
	"Classic": "CLSIC",
	"Elite Series": "BSMELITE",
	"NFR": "NFR",
	"Allstate Louisiana Kickoff": "ALLST",
	"2022 Kickoff Collection": "SGBKCKOFF"
}


#Duplicate Gifts & Accessories Subcategories:
duplicateNoveltySubcategoryList = ["Football", "Post Season Gear", "Flags", "Magnets", "Buttons & Pins"]



#"Parent to child" category dict:
subcategoryDicts = {
	"PRODUCT": PRODUCT,
	"Men": Men,
	"Women": Women,
	"Youth": Youth,
	"Headwear": Headwear,
	"Gifts & Accessories": GiftsAndAccessories,
	"Jerseys": Jerseys,
	"Shop Sport": ShopSports,
	"Special Collection": SpecialCollection,
	"Events": Events,
	"Bowls": Bowls
}