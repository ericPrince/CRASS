
'''
module : dbmgr

features firebase wrapper functions

functions:
    addOffender()
    getOffender()
    updateOffender()
    removeOffender()
    addCrassWord()
    getCrassWord()
    removeCrassWord()
'''

from firebase import firebase
from requests import HTTPError
from localcreds import get_credentials

#Authentication 
FIREBASE_URL = "https://crass.firebaseio.com/"
FIREBASE_KEY = get_credentials()
authentication = firebase.FirebaseAuthentication(FIREBASE_KEY, 'ilyakrasnovsky@gmail.com', admin = True)
fdb = firebase.FirebaseApplication(FIREBASE_URL, authentication=authentication)

'''
function: addOffender()

description:
    -Adds an offender to the CRASS database from a dictionary
    of values

inputs: 
    Odict : A dictionary describing and offender to be added

outputs:
    status : True if addition was successful,
            False if name of offender already taken,
            "ERROR" (string) in the case of connection
            issue or authentication problem.
'''
def addOffender(Odict):
    isPresent = getOffender(Odict['name'])
    if (isPresent == None):
        try:
            fdb.put('/offenders/', Odict['name'], Odict)
            return True
        except HTTPError:
            return "ERROR"
    elif (isPresent == "ERROR"):
        return "ERROR"
    else:
        return False

'''
function: getOffender()

description:
    -Searches for an offender in the CRASS database from a name,
    DEFAULT gets all offenders

inputs: 
    name : name (string) of offender to look for (optional, if None,
        returns all offenders)

outputs:
     If found, returns dictionary representing an offender
     (or dictionary of dictionaries of many offenders by name
        if name was None, None if not found, and "ERROR" if 
            connection/authentication issue)
'''
def getOffender(name=None):
    try:
        return fdb.get('/offenders/', name)
    except HTTPError:
        return "ERROR"

'''
function: updateOffender()

description:
    -Updates the data for an offender in the CRASS database from a name,

inputs: 
    name : name (string) of offender to look for (optional, if None,
        returns all offenders)
    attr : dictionary of updated attributes (values) describing the offender

outputs:
    status : True if update was successful,
            False if selected offender not in database,
            "ERROR" (string) in the case of connection
            issue or authentication problem.
'''
def updateOffender(name, attr):
    isPresent = getOffender(name)
    if (isPresent != None):
        try:
            fdb.patch('/offenders/' + name + "/attr/", attr)
            return True
        except HTTPError:
            return "ERROR"
    elif (isPresent == "ERROR"):
        return "ERROR"
    else:
        return False

'''
function: removeOffender()

description:
    -Removes an offender from the database by name

inputs: 
    name : name (string) of offender to delete
    
outputs:
    status : True if delete was successful,
            False if selected offender not in database,
            "ERROR" (string) in the case of connection
            issue or authentication problem.
'''
def removeOffender(name):
    isPresent = getOffender(name)
    if (isPresent != None):
        try:
            fdb.delete('/offenders/', name)
            return True
        except HTTPError:
            return "ERROR"
    elif (isPresent == "ERROR"):
        return "ERROR"
    else:
        return False

'''
function: addCrassWord()

description:
    -Adds a crass word (string) to the database.

inputs: 
    word : a string of the crass word to be added

outputs:
    status : True if addition was successful,
            False if name of word already taken,
            "ERROR" (string) in the case of connection
            issue or authentication problem.
'''
def addCrassWord(word):
    isPresent = getCrassWord(word)
    if (isPresent == None):
        try:
            fdb.put('/crasswords/', word, word)
            return True
        except HTTPError:
            return "ERROR"
    elif (isPresent == "ERROR"):
        return "ERROR"
    else:
        return False

'''
function: getCrassWord()

description:
    -Searches for a crass word in the database from a name,
    DEFAULT gets all crasswords

inputs: 
    word : name (string) of crassword to look for (optional, if None,
        returns all crasswords)

outputs:
     If found, returns the crassword
     (or dictionary of many crasswords by name
        if name was None, None if not found, and "ERROR" if 
            connection/authentication issue)
'''
def getCrassWord(word=None):
    try:
        return fdb.get('/crasswords/', word)
    except HTTPError:
        return "ERROR"

'''
function: removeCrassWord()

description:
    -Removes a crassword from the database by name

inputs: 
    word : name (string) of crassword to delete
    
outputs:
    status : True if delete was successful,
            False if selected crassword not in database,
            "ERROR" (string) in the case of connection
            issue or authentication problem.
'''
def removeCrassWord(word):
    isPresent = getCrassWord(word)
    if (isPresent != None):
        try:
            fdb.delete('/crasswords/', word)
            return True
        except HTTPError:
            return "ERROR"
    elif (isPresent == "ERROR"):
        return "ERROR"
    else:
        return False
    
#Tester client
def main():
    ilya = {
        'name' : 'ilya',
        'attr' : {
            'speed' : 3,
            'accuracy' : 3,
            'readability' : 7,
            'confidence' : 7        
        }
    }
    danny = {
        'name' : 'danny',
        'attr' : {
            'speed' : 5,
            'accuracy' : 5,
            'readability' : 5,
            'confidence' : 5        
        }
    }
    hannah = {
        'name' : 'hannah',
        'attr' : {
            'speed' : 7,
            'accuracy' : 7,
            'readability' : 3,
            'confidence' : 3        
        }
    }
    
    print ("TESTING addOffender")
    status = addOffender(ilya)
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(True))
    status = addOffender(danny)
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(True))
    status = addOffender(hannah)
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(True))
    status = addOffender(ilya)
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(False))
    status = addOffender(danny)
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(False))
    status = addOffender(hannah)
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(False))
    
    print ("TESTING getOffender")
    status = getOffender("ilya")
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(ilya))   
    status = getOffender("danny")
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(danny))   
    status = getOffender("hannah")
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(hannah))   
    status = getOffender("eric")
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(None))   
    status = getOffender("shirley")
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(None))   
    
    print ("TESTING getOffender WITH NO INPUT")
    status = getOffender()
    allOffenders = {
        "ilya" : ilya,
        "danny" : danny,
        "hannah" : hannah
    }
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(allOffenders))   

    print ("TESTING updateOffender")
    updateIlya = {
        'speed' : 1,
        'accuracy' : 1,
        'readability' : 1,
        'confidence' : 1   
    }
    status = updateOffender("ilya", updateIlya)
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(True))   
    updateDanny = {
        'speed' : 1,
        'accuracy' : 1,
        'readability' : 1,
        'confidence' : 1   
    }
    status = updateOffender("danny", updateDanny)
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(True))   
    updateHannah = {
        'speed' : 2,
        'accuracy' : 2,
        'readability' : 2,
        'confidence' : 2 
    }
    status = updateOffender("hannah", updateHannah)
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(True))   
    updateEric = {
        'speed' : 2,
        'accuracy' : 2,
        'readability' : 2,
        'confidence' : 2   
    }
    status = updateOffender("eric", updateEric)
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(False))   
    
    print ("TESTING getOffender after updateOffender")
    status = getOffender("ilya")
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(updateIlya))   
    status = getOffender("danny")
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(updateDanny))   
    status = getOffender("hannah")
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(updateHannah))   
    status = getOffender("eric")
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(None))   
    
    print ("TESTING removeOffender")
    status = removeOffender("ilya")
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(True))   
    status = removeOffender("danny")
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(True))   
    status = removeOffender("eric")
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(False))   
    
    print ("TESTING getOffender after removeOffender")
    status = getOffender("ilya")
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(None))   
    status = getOffender("danny")
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(None))   
    status = getOffender("hannah")
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(updateHannah))   
    status = getOffender("eric")
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(None))   
    
    print ("TESTING addCrassWord")
    status = addCrassWord("fuck")
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(True))   
    status = addCrassWord("fuck")
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(False))   
    status = addCrassWord("shit")
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(True))   
    
    print ("TESTING getCrassWord")
    status = getCrassWord("shit")
    print ("REAL : " + str(status) + "   |   CORRECT : " + str("shit"))   
    status = getCrassWord("lol")
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(None))   
    
    print("TESTING getCrassWord WITH NO INPUT")
    status = getCrassWord()
    allCrassWords = {
        "fuck" : "fuck",
        "shit" : "shit"
    }
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(allCrassWords))   
    
    print ("TESTING removeCrassWord")
    status = removeCrassWord("fuck")
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(True))   
    status = removeCrassWord("lol")
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(False))   
    
    print ("TESTING getCrassWord after removeCrassWord")
    status = getCrassWord("shit")
    print ("REAL : " + str(status) + "   |   CORRECT : " + str("shit"))   
    status = getCrassWord("lol")
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(None))   
    status = getCrassWord("fuck")
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(None))   

if __name__ == '__main__':
    main()