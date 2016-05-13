'''
module : dbclient (database client)

supports client class for dbmgr

classes:
	DbClient
'''

from dbmgr import Dbmgr
import getpass
import time
import dbutils

'''
class: DbClient

description:
    -acts as a client for dbmgr module, features higher level
    functions

attributes:
	dbmgr : instance of the Dbmgr class

initializer input:
	dbmgr : instance of the Dbmgr class

functions:
	registerOffender()
	changeOffender()
	unregisterOffender()

'''

class DbClient():
	def __init__(self, dbmgr):
		self.dbmgr = dbmgr
		myname = getpass.getuser()
		self.registerOffender(myname)

	'''
    function: registerOffender()

    description:
        -Registers a Crass offender in the database with default
        attributes (5,5,5,5)

    inputs: 
        name : A string name of the offender to be Registers

    outputs:
    	None
    '''
	def registerOffender(self, name):
		print ("Welcome to Crass! You're such an asshole."
			   " Registering you as an offender ...")
		print()
		newOffender = {
			"name" : name,
			"attr" : {
		        'speed' : 5,
		        'accuracy' : 5,
		        'readability' : 5,
		        'confidence' : 5 
			}
		}
		status = self.dbmgr.addOffender(newOffender)
		time.sleep(3)
		if (status == False):
			print ("Oh wait, it looks like you're fucking in here"
				" already. Bullshit. Well, good for you, asshole.")
		else:
			print ("Done! Do you feel good about yourself?")

	'''
    function: changeOffender()

    description:
        -Changes another offender's attributes

    inputs: 
        name : A string name of the offender to be changed
        attr : a dictionary of the form 
        		{
        			'speed' : int,
        			'accuracy' : int,
        			'readability' : int,
        			'confidence' : int 
        		}
    outputs:
    	None
    '''
	def changeOffender(self, name):
		#check to make sure that that the offender you're
		#changing is not you
		if (name == getpass.getuser()):
			print ("You're trying to change information about yourself!?"
					" WTF?! You can't do that.")
		else:
			print ("")

	def unregisterOffender(self):
		#Say something like "you're in this for life"
		pass

	def findFellowOffenders(self):
		offenders = self.dbmgr.getOffender()
		if (offenders != None):
			print ("Your 'honorary' fellow offenders are : ")
		else:
			print ("Looks like you're the only bitch on crass right now.")
		return offenders 

	def learnVocabulary(self):
		#call getCrassWord()
		pass

#Tester client
def main():
	dbmgr = Dbmgr()
	dbclient = DbClient(dbmgr)
	time.sleep(3)
	print(dbclient.findFellowOffenders()) 
	#valid = False	
	#while(valid != True):
	#	welcome = input()

if __name__ == '__main__':
    main()