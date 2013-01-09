"""
file: ti_decode.py
language: python3
author: Nate Levesque <public@thenaterhood.com>
description: Decompiles TI83 calculator programs to plaintext and saves
    the decompiled data.
    
TODO:
    add ability to parse lists called in the code
    
    add validity checking for TI-Basic files
"""
import binascii
from copy import deepcopy
import dictionaries
import tiFile
import common


def init():    
    print("TI BASIC file decoder.  Decodes TIBASIC files into plaintext.\n")
    print("Nate Levesque <public@thenaterhood.com>.")
    print("Visit www.thenaterhood.com/projects for more software\n")

def translate(dictionary, content, escapeCharExists, escapeChar):
    """
    Takes a dictionary and a list of items (such as bytes in a file)
    and checks each byte to see if it's a key in the dictionary.  If it
    is, it replaces the item with the key's value.  Supports having
    preceding escape characters.
    
    Arguments:
        dictionary (dict): a dictionary mapping byte values to values
        content (list): a list containing byte values
        escapeCharExists (boolean): whether or not to look for an escape
            character when replacing values
        escapeChar (string): an escape character to look for. Has no
            effect if escapeCharExists is valse
        
    Returns:
        translation (list): a copy of the content list with every
            recognized value replaced
    """
    
    # Make a copy of the input so the original isn't modified
    translation = deepcopy(content)
    
    # Iterate through each index of the copy of the content
    for i in range(0, len(translation)):
        # If there is no escape character set, check if the item
        # exists in the dictionary and replace it with its value if it does
        if ( not escapeCharExists):
            if (translation[i] in dictionary):
                translation[i] = dictionary[translation[i]]
                
        # If an escape character is set, the iteration has found it, and
        # the item at the index after it is in the dictionary, replace
        # the escape character with an emptyString and replace the next
        # character with its value from the dictionary
        try:
            if (escapeCharExists and 
            translation[i] == escapeChar and 
            translation[i+1] in dictionary):
                translation[i] = ""
                translation[i+1] = dictionary[translation[i+1]]
        except:
            pass 
                
    return translation
    
def parseFile(unparsedFile):
    """
    Parses the TI-Basic .8Xp file and translates the byte values
    for tokens and characters into their plaintext equivalent
    so the file can be viewed off the calculator.  Replaces the former
    parseWhitespace and parseFunction functions, as they weren't
    specialized in any particular way after the dictionaries were
    moved out of them.
    
    Arguments:
        fileContents (list): the byte contents of the file to parse
        
    Returns:
        parsedFile (list): a list containing the converted file, but with
            unparsed byte values still intact (python will convert these
            to a string representation when printing/saving)
            
    """
    fileContents = deepcopy(unparsedFile)
    
    # Parse the uppercase letters and numbers
    ascii_dict = dictionaries.standardASCII(False)
    parsedFile = translate(ascii_dict, fileContents, False, '')
    
    # Parse the lowercase letters, with their escape values
    ascii_lower_dict = dictionaries.lowercaseASCII(False)
    parsedFile = translate(ascii_lower_dict, parsedFile, True, b'\xbb')
    
    # Parses the ascii symbols to their plaintext equivalents.
    # NOTE: this must be called AFTER lowercase letters are parsed,
    # as some symbols have the same byte values as lowercase letters
    # in TI-Basic.
    ascii_symbol_dict = dictionaries.symbolsASCII(False)
    parsedFile = translate(ascii_symbol_dict, parsedFile, False, '')
    
    # Parse whitespace byte codes into plaintext
    whitespace_dict = dictionaries.whitespace(False)
    parsedFile = translate(whitespace_dict, parsedFile, False, '')
    
    # Parse the ti-basic tokens to plaintext words
    function_dict = dictionaries.tibasicFunctions(False)
    parsedFile = translate(function_dict, parsedFile, False, '')
    
    return parsedFile

def main():
    """
    Calls the functions in order to decode the .8Xp file.  Order
    DOES matter here for each parsing function or garbage results
    
    Arguments:
        none
    Returns:
        none
    """
    init()
    
    # Request a filename from the user
    filename = common.getFName()
    
    # Read the file
    tiData = tiFile.read(filename)
    
    if (not tiFile.validate(tiData)):
        raise RuntimeError("The file requested doesn't appear to be a TI-Basic file.")
    
    # A basic check to make sure the file contains program data,
    # raises an error if not
    if (tiData.prgmdata != 'null'):
        fileContents = tiData.prgmdata
    else:
        raise RuntimeError("FATAL: The file requested does not contain program data")
        
    parsedFile = parseFile(fileContents)
    
    # Create a string representation of the parsed file that can be
    # printed to the console
    string = ""
    for item in parsedFile:
        string += str(item)
    print(string)
    save = input("\n Would you like to save this output?  y/n: ")
    
    if (save in ['y', 'Y']):
        common.saveFile(parsedFile, filename)
    else:
        print("Done.  Exiting without saving.")    
    

# Call the main method
main()
