'''
module : dbclient (database client)

supports client class for dbmgr

classes:
	DbClient
'''

from dbmgr import Dbmgr
import getpass

'''
class: DbClient

description:
    -acts as a client for dbmgr module, features higher level
    functions

attributes:
	dbmgr : instance of the Dbmgr class

initializer input:
	dbmgr : instance of the Dbmgr class

'''

class DbClient():
	def __init__(self, dbmgr):
		self.dbmgr = dbmgr
		myname = getpass.getuser()

	def registerOffender(self, name):
		pass

	def changeOffender(self):
		pass

	def unregisterOffender(self):
		pass

if __name__ == '__main__':
    main()