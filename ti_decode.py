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

def parseASCII(fileContents):
    """
    Parses the TI83 hex codes for standard ascii characters and replaces
    them with the ascii equivalent.
    
    Arguments:
        fileContents (list): a list containing byte values read from
            a file
    Returns:
        a list containing the file with ascii characters in the place
        of byte values that were interpreted and converted
    """
    # make a deepcopy of the list so the original isn't modified
    ascii_parsed = deepcopy(fileContents)
    
    # A dictionary mapping each TI83 uppercase character code with its
    # ASCII equivalent
    ascii_dict = dictionaries.standardASCII(False)
    
    # Call translate with the uppercase dictionary, the file contents
    # and no escape code set.
    ascii_parsed = translate(ascii_dict, ascii_parsed, False, '')
      
    # A dictionary mapping each TI83 lowercase letter code to its
    # ascii lowercase equivalent
    ascii_lower_dict = dictionaries.lowercaseASCII(False)
    
    # Call translate with the lowercase dictionary, the file contents,
    # and the escape character b'\xbb' set
    ascii_parsed = translate(ascii_lower_dict, ascii_parsed, True, b'\xbb')
    
    # Dictionary mapping each TI83 symbol with its ascii equivalent.
    # MUST be called AFTER the lowercase letters are replaced because
    # some lowercase letters have the same hex value and need to be
    # interpreted with their escape characters first                
    ascii_symbol_dict = dictionaries.symbolsASCII(False)
    
    # Call translate with the ascii symbol dictionary, the file contents,
    # and no escape character set
    ascii_parsed = translate(ascii_symbol_dict, ascii_parsed, False, '')
    
    return ascii_parsed

def parseWhitespace(fileContents):
    """
    Parses the TI83 whitespace codes
    
    Arguments:
        fileContents (list): a list of the byte values read from the file
    Returns:
        a list of byte values with the whitespace codes replaced with
        their ascii equivalents
    """
    whitespace_dict = dictionaries.whitespace(False)
            
    return translate(whitespace_dict, fileContents, False, '')

def parseFunction(fileContents):
    """
    Converts the TI83 byte values for TI-BASIC functions to plaintext
    
    Arguments:
        fileContents (list): a list of byte values read from the file
    Returns:
        a list with the byte values for functions replaced with their
        plaintext equivalents
    """
    
    # Dictionary mapping function hex codes to their plaintext values
    function_dict = dictionaries.tibasicFunctions(False)

    # calls the translate function with the function dictionary,
    # contents of the file, and no escape character set
    return translate(function_dict, fileContents, False, '')
            

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
        
    
    # Parse the file.  Again, order matters here
    parsedFile = parseASCII(fileContents)
    parsedFile = parseWhitespace(parsedFile)
    parsedFile = parseFunction(parsedFile)
    
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
