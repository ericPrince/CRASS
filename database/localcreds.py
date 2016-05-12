'''
Sets up FIREBASE_KEY for developing our 
application locally on your machine. Run:

$ python localcreds.py '<FIREBASE_KEY_HERE>'

to set it up (NOTE THE QUOTES!). This only needs to be done once.
'''
import os, sys

def get_credentials(key=None):
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'CRASS_FIREBASE_SECRET.txt')
    if (key != None):
        with open (credential_path, 'w') as secret_file:
            secret_file.write(key)    
    with open (credential_path, 'r') as secret_file:
        FIREBASE_KEY = secret_file.read()
    return FIREBASE_KEY

#Tester client
def main(argv):
    if (len(argv) >= 1):
        FIREBASE_KEY = argv[0]
    else:
        FIREBASE_KEY = None
    print ('FIREBASE_KEY SET TO : ' + get_credentials(FIREBASE_KEY))

if __name__ == '__main__':
    main(sys.argv[1:])