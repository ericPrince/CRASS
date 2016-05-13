'''
module : dbclient (database client)

supports client class for dbmgr

classes:
	DbClient
'''

from dbmgr import Dbmgr
import getpass
import time

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

	def changeOffender(self):
		pass

	def unregisterOffender(self):
		pass

#Tester client
def main():
	dbmgr = Dbmgr()
	dbclient = DbClient(dbmgr)
	#while(True):
	#	welcome = input()

if __name__ == '__main__':
    main()