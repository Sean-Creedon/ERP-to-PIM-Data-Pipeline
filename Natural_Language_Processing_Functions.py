
import nltk, re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn

lemmatizer = WordNetLemmatizer()

def listNamedEntitiesInProductName(productName):
    """"""
    words = word_tokenize(productName)
    tags = nltk.pos_tag(words)
    tree = nltk.ne_chunk(tags, binary=True)
    setOfTags = set(" ".join(item[0].lower() for item in tag) for tag in tree if hasattr(tag, "label") and tag.label() == "NE")
    return setOfTags

def extractNamedEntitiesFromProductName(text, namedEntityList):
    """"""
    temporaryText = text.lower()
    for entity in namedEntityList:
        print(f"entity: {entity}")
        temporaryText = temporaryText.replace(entity, "")
    return temporaryText.strip()

#List of regex rules for extracting common product names/noun phrases from product names: "1/4 Zip", "1/2 Zip"
#Find and capture/"remember" any quarter zips, half zips, etc. Note: Don't think we see "1/4-zip"; also special character fractions will be missed ("\u00BC").
zipperedPulloverProductRule = "([0-9]/[0-9] [A-Za-z]*)"
#Add rule for spelled out "quarter zip"?
#Add more rules here.
#
#List of all company-specific noun phrases:
PRODUCT_REGEX_LIST = [zipperedPulloverProductRule]

def extractCustomProductNounPhrases(text):
    """"""
    temporaryText = text
    for productRule in PRODUCT_REGEX_LIST:
        #Loop through the regex rules and search for matches, assign matches to a variable to add to
        #keywords to look up, then remove match from placeholder name.
        if phraseFound := re.search(productRule, temporaryText):
            match = phraseFound.group(1)
            print(f"phraseFound: {match}")
            keywordSeedList.append(match.lower())
            temporaryText = re.sub(match, "", temporaryText)
    return temporaryText.strip()


def parseProductNameForSearchKeywords(productName):
    """"""
    keywordSeedList = []

    print(f"productName: {productName}\n\n")

    #Use this to pull out prop/team name: Arkansas Razorbacks
    namedEntities = listNamedEntitiesInProductName(productName)
    print(f"namedEntities: {namedEntities}\n\n")
    #Something for pattern matching. Keep '1/4' & 'zip' together to add to phrases to synonym search.
    keywordSeedList.extend(namedEntities)

    wordsInproductNameWithoutNamedEntities = extractNamedEntitiesFromProductName(productName, namedEntities)
    print(f"wordsInproductNameWithoutNamedEntities: {wordsInproductNameWithoutNamedEntities}\n\n")

    wordsInproductNameWithoutCustomNamedEntities = extractCustomProductNounPhrases(wordsInproductNameWithoutNamedEntities)
    print(f"wordsInproductNameWithoutCustomNamedEntities: {wordsInproductNameWithoutCustomNamedEntities}")

    wordsInproductName = word_tokenize(wordsInproductNameWithoutCustomNamedEntities)
    print(f"wordsInproductName: {wordsInproductName}\n\n")

    stop_words = set(stopwords.words("english"))
    #Filter out punctuation? DO need to keep "1/4 Zip"
    filteredList = [word.lower() for word in wordsInproductName if word.casefold() not in stop_words]
    #Activate this line and deactivate the previous 3 lines to test with stop words:
    #filteredList = wordsInproductName
    print(f"filteredList: {filteredList}\n\n")

    taggedWords = nltk.pos_tag(filteredList)
    print(f"taggedWords: {taggedWords}\n\n")

    lemmatizedWords = [lemmatizer.lemmatize(word) for word in filteredList]
    print(f"lemmatizedWords: {lemmatizedWords}\n\n")

    print(f"keywordSeedList: {keywordSeedList}\n\n")

    keywordSeedList.extend(lemmatizedWords)

    print(f"keywordSeedList: {keywordSeedList}\n\n")

    keywordPOS = nltk.pos_tag(keywordSeedList)#[4:6]
    print(f"keywordPOS: {keywordPOS} {type(keywordPOS)}")

    onsiteSearchKeywords = keywordSeedList
    replaceUnderscore = lambda term: term.replace("_"," ")
    partsOfSpeachToExtract = ["NN", "VBG", "VB", "VBZ", "CD", "NNS"]#Need nouns/gerunds & verbs from product name for synonym search

    for keyword in keywordPOS:
        #keyword[0] = word: "windshirt", keyword[1] =  POS code: "NN"
        #Want to get only synonyms for correct form: synonymList = wn.synsets("windshirt", wn.NOUN)
        searchTerm = keyword[0]
        searchTermPOS =  keyword[1]#Need nouns/gerunds & verbs: NN, VBG, VB, VBZ
        synonymList = wn.synsets(searchTerm)
        print(f"\n\nkeyword: {keyword}, searchTermPOS: {searchTermPOS}, synonymList: {synonymList} {type(synonymList)}\n\n")
        if searchTermPOS in partsOfSpeachToExtract:
            for synonym in synonymList:
                newOnsiteSearchKeyword = [replaceUnderscore(term) for term in synonym.lemma_names()]
                #print(newOnsiteSearchKeyword)
                onsiteSearchKeywords.extend(newOnsiteSearchKeyword)
                #print(f"synonym: {newOnsiteSearchKeyword} {type(synonym)}")
        onsiteSearchKeywords = list(set(onsiteSearchKeywords))#Dedupe list

    print(f"{productName}:\n{onsiteSearchKeywords}")
    #Change list output to string:
    onsiteSearchKeywords = ", ".join(onsiteSearchKeywords)
    return onsiteSearchKeywords

if __name__ == "__main__":
    nltk.help.upenn_tagset()
    testProductName = "Arkansas Razorbacks Take Your Time 1/4 Zip Windshirt"
    pass