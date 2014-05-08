#!/usr/bin/env python3
import hashlib, sys, time
from itertools import product


def get_algorithm( _type ):
    def algorithm( string ):
        """
           This uses Python closure to dynamically select the hashtype.
        """
        h = _type()
        h.update(string.encode('utf-8'))
        return h.hexdigest()
    return algorithm


TYPES_DICT = { 32 : get_algorithm( hashlib.md5 ),
               40 : get_algorithm( hashlib.sha1 ),
               56 : get_algorithm( hashlib.sha224 ),
               64 : get_algorithm( hashlib.sha256 ),
               96 : get_algorithm( hashlib.sha384 ),
               128 : get_algorithm( hashlib.sha512 ) }



class Control( object ):
    
    
    def __init__( self ):
        """
           The 3 attributes below are set to None for the purpose
           of looping should the user accidentally enter incorrect
           information
        """
        self.decrypt_method = None
        self.decrypted_hash = None
        self.user_file = None
    
    
    def main( self ):
        """
           This method just calls on all of the other methods in the 
           class, kind of a 'central hub'. There is also a while loop
           so that if no match is found the retry() method is called.
        """
        self.user_hash = self.get_hash()
        
        while self.decrypted_hash == None: 
            self.crack_method = self.get_crack_method()
            
            if self.crack_method == 'd':
                self.wordlist = self.gen_wordlist()
                self.decrypted_hash = self.dict_attack()
            elif self.crack_method == 'b':
                self.decrypted_hash = self.brute_force()
                
            
            if self.decrypted_hash != None: 
                self.elapsed = (time.time() - self.start) 
                print('Hash cracked in '+str( self.elapsed )+' seconds. The correct word is: '+self.decrypted_hash )
                sys.exit()
            else:
                self.retry('no matches found')

            
    def get_hash( self ):
        """
           Prompts the user for a hash. If an invalid hash is entered 
           calls the retry method.
        """
        while True:
            hash_input = input('Please enter the hash: ')
            
            if hash_input.isalnum(): 
                length = len( hash_input )
                
                if TYPES_DICT.get( length, None ):
                    self.hashtype = TYPES_DICT[length]
                    return hash_input

                else:
                    self.retry('invalid hash')
            
            else:
                self.retry('invalid hash')
                    
                    
    def gen_wordlist( self ):
        """
           Prompts the user to enter the name of a wordlist, or a full 
           path to the wordlist. If the file does not exist the retry 
           method is called. If the file does exist then the words are 
           split into a list and returned to the main() method.
        """
        
        while self.user_file == None:
            self.filename = input('Please enter the name of the wordlist: ')
            
            try:
                self.user_file = open( self.filename, 'r', encoding='utf-8' )
            
            except FileNotFoundError:
                self.retry('no file named '+self.filename)
        
        words = self.user_file.read()
        self.user_file.close()
        return words.split()
         
    
    def get_crack_method( self ):
        """
           Gives the user two choices of attack method, bruteforce or 
           dictionary. If an invalid option is chosen, the retry method 
           is called.
        """
        while True: 
            crack_method = input("Please enter 'b' for brute-force or 'd' for dictionary attack: ")
            if crack_method.lower() == 'b':
                return crack_method
            elif crack_method.lower() == 'd':
                return crack_method
            else:
                self.retry('invalid option')
            
    
    def dict_attack(  self):
        """
           Loops through the wordlist, converting each word to the correct
           hashtype and comparing to the hash that needs to be cracked.
           If there is no match found, the value of cracked_hash attribute in the 
           main() method will be None, and the retry method will be called.
           Also initiates the timer.
        """
        self.start = time.time()
        print('Checking...\n\n')
        for word in self.wordlist:
            test = self.hashtype( word )
            if test == self.user_hash:
                return word
                
                
    def brute_force( self ):
        """
           The user enters a desired character set, minimum length and
           maximum length. It will then use itertools.product() to generate
           every possible combination of the characters, and converts to
           the correct hash type for each combination.
        """
        charset = input('Please enter required character set: ')
        minlen = int(input('Please enter minimum length: '))
        maxlen = int(input('Please enter maximum length: '))
        
        print('Checking... (this could take a while) \n\n')
        self.start = time.time()
        for i in range( minlen, maxlen+1 ):
            for p in product( charset, repeat=i ):
                word = ''.join( p )
                if self.hashtype(word) == self.user_hash:
                    return word
                
                
    def retry( self, failure_type ):
        """
           Last but certainly not least, the retry method. The parameter
           passed is a string. It is in a loop in case the user enters
           another invalid option. 
        """
        print('Sorry, '+failure_type+'. Would you like to try again? (y/n)')
        while True:
            choice = input()
            if choice.lower() == 'y':
                return
            elif choice.lower() == 'n':
                print('Thanks for using, goodbye.')
                sys.exit()
            else:
                print('Invalid option. Please press y or n.')

                    
                    
if __name__ == "__main__":
    run_it = Control()
    run_it.main()
