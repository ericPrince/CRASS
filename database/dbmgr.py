'''
module : dbmgr

features firebase wrapper class called Dbmgr

'''

from firebase import firebase
from requests import HTTPError
from localcreds import get_credentials

'''
class: Dbmgr

description:
    - database manager class

attributes:
    fdb : instance of the FirebaseApplication class    

initializer input:
    None

functions:
    addOffender()
    getOffender()
    updateOffender()
    removeOffender()
    addCrassWord()
    getCrassWord()
    removeCrassWord()
'''

class Dbmgr():
    def __init__(self):
        #Authentication 
        FIREBASE_URL = "https://crass.firebaseio.com/"
        FIREBASE_KEY = get_credentials()
        authentication = firebase.FirebaseAuthentication(FIREBASE_KEY, 'ilyakrasnovsky@gmail.com', admin = True)
        self.fdb = firebase.FirebaseApplication(FIREBASE_URL, authentication=authentication)

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
    def addOffender(self,Odict):
        isPresent = self.getOffender(Odict['name'])
        if (isPresent == None):
            try:
                self.fdb.put('/offenders/', Odict['name'], Odict)
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
    def getOffender(self,name=None):
        try:
            return self.fdb.get('/offenders/', name)
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
    def updateOffender(self, name, attr):
        isPresent = self.getOffender(name)
        if (isPresent != None):
            try:
                self.fdb.patch('/offenders/' + name + "/attr/", attr)
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
    def removeOffender(self, name):
        isPresent = self.getOffender(name)
        if (isPresent != None):
            try:
                self.fdb.delete('/offenders/', name)
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
    def addCrassWord(self, word):
        isPresent = self.getCrassWord(word)
        if (isPresent == None):
            try:
                self.fdb.put('/crasswords/', word, word)
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
    def getCrassWord(self, word=None):
        try:
            return self.fdb.get('/crasswords/', word)
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
    def removeCrassWord(self, word):
        isPresent = self.getCrassWord(word)
        if (isPresent != None):
            try:
                self.fdb.delete('/crasswords/', word)
                return True
            except HTTPError:
                return "ERROR"
        elif (isPresent == "ERROR"):
            return "ERROR"
        else:
            return False
    
#Tester client
def main():
    dbmgr1 = Dbmgr()
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
    status = dbmgr1.addOffender(ilya)
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(True))
    status = dbmgr1.addOffender(danny)
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(True))
    status = dbmgr1.addOffender(hannah)
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(True))
    status = dbmgr1.addOffender(ilya)
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(False))
    status = dbmgr1.addOffender(danny)
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(False))
    status = dbmgr1.addOffender(hannah)
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(False))
    
    print ("TESTING getOffender")
    status = dbmgr1.getOffender("ilya")
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(ilya))   
    status = dbmgr1.getOffender("danny")
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(danny))   
    status = dbmgr1.getOffender("hannah")
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(hannah))   
    status = dbmgr1.getOffender("eric")
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(None))   
    status = dbmgr1.getOffender("shirley")
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(None))   
    
    print ("TESTING getOffender WITH NO INPUT")
    status = dbmgr1.getOffender()
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
    status = dbmgr1.updateOffender("ilya", updateIlya)
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(True))   
    updateDanny = {
        'speed' : 1,
        'accuracy' : 1,
        'readability' : 1,
        'confidence' : 1   
    }
    status = dbmgr1.updateOffender("danny", updateDanny)
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(True))   
    updateHannah = {
        'speed' : 2,
        'accuracy' : 2,
        'readability' : 2,
        'confidence' : 2 
    }
    status = dbmgr1.updateOffender("hannah", updateHannah)
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(True))   
    updateEric = {
        'speed' : 2,
        'accuracy' : 2,
        'readability' : 2,
        'confidence' : 2   
    }
    status = dbmgr1.updateOffender("eric", updateEric)
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(False))   
    
    print ("TESTING getOffender after dbmgr1.updateOffender")
    status = dbmgr1.getOffender("ilya")
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(updateIlya))   
    status = dbmgr1.getOffender("danny")
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(updateDanny))   
    status = dbmgr1.getOffender("hannah")
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(updateHannah))   
    status = dbmgr1.getOffender("eric")
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(None))   
    
    print ("TESTING removeOffender")
    status = dbmgr1.removeOffender("ilya")
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(True))   
    status = dbmgr1.removeOffender("danny")
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(True))   
    status = dbmgr1.removeOffender("eric")
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(False))   
    
    print ("TESTING getOffender after removeOffender")
    status = dbmgr1.getOffender("ilya")
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(None))   
    status = dbmgr1.getOffender("danny")
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(None))   
    status = dbmgr1.getOffender("hannah")
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(updateHannah))   
    status = dbmgr1.getOffender("eric")
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(None))   
    
    print ("TESTING addCrassWord")
    status = dbmgr1.addCrassWord("fuck")
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(True))   
    status = dbmgr1.addCrassWord("fuck")
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(False))   
    status = dbmgr1.addCrassWord("shit")
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(True))   
    
    print ("TESTING getCrassWord")
    status = dbmgr1.getCrassWord("shit")
    print ("REAL : " + str(status) + "   |   CORRECT : " + str("shit"))   
    status = dbmgr1.getCrassWord("lol")
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(None))   
    
    print("TESTING getCrassWord WITH NO INPUT")
    status = dbmgr1.getCrassWord()
    allCrassWords = {
        "fuck" : "fuck",
        "shit" : "shit"
    }
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(allCrassWords))   
    
    print ("TESTING removeCrassWord")
    status = dbmgr1.removeCrassWord("fuck")
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(True))   
    status = dbmgr1.removeCrassWord("lol")
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(False))   
    
    print ("TESTING getCrassWord after removeCrassWord")
    status = dbmgr1.getCrassWord("shit")
    print ("REAL : " + str(status) + "   |   CORRECT : " + str("shit"))   
    status = dbmgr1.getCrassWord("lol")
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(None))   
    status = dbmgr1.getCrassWord("fuck")
    print ("REAL : " + str(status) + "   |   CORRECT : " + str(None))   

if __name__ == '__main__':
    main()