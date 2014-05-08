#!/usr/bin/env python3
import hashlib


def hash( _type, string ):
    """
       The _type parameter is a hashlib function, which is selected from
       the TYPES_DICT dictionary below. The string is the text to be 
       encrypted.
    """
    h = _type()
    h.update(string.encode('utf-8'))
    return h.hexdigest()
    
    
def main():
    """
       Prompts for a string, and then for a hashing method. The hashing 
       method entered will select the correct hash function from the 
       TYPES_DICT constant
    """
    string = input("Please enter the string to be hashed: ")
    print("Please choose from the following hash methods:")
    choice = int(input("1: md5\n2: sha1\n3: sha224\n4: sha256\n5: sha384\n6: sha512\n\n"))
    print('\n')
    
    if TYPES_DICT.get( choice ):
        print( TYPES_DICT[choice][0], 'selected.' )
        print( string, '=>', hash( TYPES_DICT[choice][1], string ))
    else:
        print('Invalid option! Learn to type...')
         
    
    

if __name__ == "__main__":
    TYPES_DICT = { 1: ['md5', hashlib.md5],
                   2: ['sha1', hashlib.sha1],
                   3: ['sha224', hashlib.sha224],
                   4: ['sha256', hashlib.sha256],
                   5: ['sha384', hashlib.sha384],
                   6: ['sha512', hashlib.sha512] }
                   
    main()
