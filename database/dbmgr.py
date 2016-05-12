
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
        return fdb.get('/students/', name)
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
            fdb.delete('/offenders/' + name)
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
     If found, returns dictionary representing an offender
     (or dictionary of dictionaries of many offenders by name
        if name was None, None if not found, and "ERROR" if 
            connection/authentication issue)
'''
def getCrassWord(word=None):
    try:
        return fdb.get('/crasswords/', word)
    except HTTPError:
        return "ERROR"

'''
function: removeOffender()

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
            fdb.delete('/crasswords/' + word)
            return True
        except HTTPError:
            return "ERROR"
    elif (isPresent == "ERROR"):
        return "ERROR"
    else:
        return False
    
#Tester client
def main():
    '''UNPROTECTED FIREBASE FOR RANDOM TESTING
    FIREBASE_URL = "https://fbtest123.firebaseio.com/"
    fdb = firebase.FirebaseApplication(FIREBASE_URL, authentication=None)
    '''
    ilya = dict()
    ilya['netid'] = "ilyak"
    ilya['freelist'] = ['2016-01-17T13:30:00', '2016-01-25T134:00:00']
    andrea = dict()
    andrea['netid'] = "amalleo"
    andrea['freelist'] = ['2016-01-17T13:30:00', '2016-01-25T134:00:00']
    nick = dict()
    nick['netid'] = "nmaselli"
    nick['freelist'] = ['2016-01-17T13:30:00', '2016-01-25T134:00:00']
    cos333 = dict()
    cos333['name'] = "COS 333"
    cos333['students'] = ["ilyak", "amalleo", "nmaselli"]
    cos333['duedates'] = ['2016-01-26', '2016-02-04' ]
    mae426 = dict()
    mae426['name'] = "MAE 426"
    mae426['students'] = ["ilyak", "nmaselli"]
    mae426['duedates'] = ['2016-01-27', '2016-02-05']

    print ("TESTING addStudent")
    status = addStudent(ilya)
    print (status)
    status = addStudent(andrea)
    print (status)
    status = addStudent(nick)
    print (status)
    status = addStudent(ilya)
    print (status)
    status = addStudent(andrea)
    print (status)
    status = addStudent(nick)
    print (status)

    print ("TESTING getStudent")
    status = getStudent("ilyak")
    print (status)
    status = getStudent("amalleo")
    print (status)
    status = getStudent("nmaselli")
    print (status)

    print ("TESTING addCourse")
    status = addCourse(cos333)
    print (status)
    status = addCourse(mae426)
    print (status)
    status = addCourse(cos333)
    print (status)
    status = addCourse(mae426)
    print (status)

    print ("TESTING getCourse")
    status = getCourse("COS 333")
    print (status)
    status = getCourse("MAE 426")
    print (status)

    print ("TESTING addTimesToStudent")
    ilya_updates = {"freelist" : ['2016-01-25T134:00:00', '2016-01-25T134:00:00']}
    status = addTimesToStudent("ilyak", ilya_updates)
    print (status)
    andrea_updates = {"freelist" : ['2016-01-25T134:00:00', '2016-01-25T134:00:00']}
    status = addTimesToStudent("amalleo", andrea_updates)
    print (status)
    status = addTimesToStudent("asdf", andrea_updates)
    print (status)

    print ("TESTING updateCourse")
    cos333_updates = {"students" : ['ilyak', 'amalleo', 'nmaselli']}
    status = updateCourse("COS 333", cos333_updates)
    print (status)
    mae426_updates = {"duedates" : ['2016-01-25']}
    status = updateCourse("MAE 426", mae426_updates)
