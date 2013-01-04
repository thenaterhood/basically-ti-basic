"""
file: ti_decode.py
language: python3
author: Nate Levesque <public@thenaterhood.com>
description: Decodes TI83 calculator programs to text
"""
import binascii
from copy import deepcopy
import dictionaries


def init():    
    print("TI BASIC file decoder.  Decodes TIBASIC files into plaintext.\n")
    print("Nate Levesque <public@thenaterhood.com>.")
    print("Visit www.thenaterhood.com/projects for more software\n")
    
def getName():
    """
    Requests the name of a file to decode from the user and checks
    that the file exists before returning it.
    
    Arguments:
        none
        
    Returns:
        string with the name of the file
    """
        
    # Implements a catchblock and tests if the file exists
    while True:
        filename = input("Enter the name of the file to decode, including the .8Xp extension: ")

        try:
            file = open(filename, 'r')
            file.close()
            return filename
        except:
            print("File could not be found.")
    # Code below is for rapid debugging, should be commented
    #return "FIBO.8Xp"
    
def readFile(filename):
    """
    Reads a file into an array as byte values
    
    Arguments:
        filename (string): the name of the file to open
    Returns:
        fileContents (list): byte values from the file
        
    """
    fileContents = []
    
    # Open the file as hex and read it one byte at a time into the
    # list fileContents
    with open(filename, "rb") as f:
        byte = f.read(1)
        while byte:
            byte = f.read(1)
            fileContents.append(byte)
    return fileContents

    
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
        if (escapeCharExists and 
        translation[i] == escapeChar and 
        translation[i+1] in dictionary):
            translation[i] = ""
            translation[i+1] = dictionary[translation[i+1]]
                
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
    ascii_dict = dictionaries.standardASCII()
    
    # Call translate with the uppercase dictionary, the file contents
    # and no escape code set.
    ascii_parsed = translate(ascii_dict, ascii_parsed, False, '')
      
    # A dictionary mapping each TI83 lowercase letter code to its
    # ascii lowercase equivalent
    ascii_lower_dict = dictionaries.lowercaseASCII()
    
    # Call translate with the lowercase dictionary, the file contents,
    # and the escape character b'\xbb' set
    ascii_parsed = translate(ascii_lower_dict, ascii_parsed, True, b'\xbb')
    
    # Dictionary mapping each TI83 symbol with its ascii equivalent.
    # MUST be called AFTER the lowercase letters are replaced because
    # some lowercase letters have the same hex value and need to be
    # interpreted with their escape characters first                
    ascii_symbol_dict = dictionaries.symbolsASCII()
    
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
    whitespace_dict = dictionaries.whitespace()
            
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
    function_dict = dictionaries.tibasicFunctions()

    # calls the translate function with the function dictionary,
    # contents of the file, and no escape character set
    return translate(function_dict, fileContents, False, '')
    
def trim(bigList, top, indexes):
    """
    Trim a number of items from the front or back (top or bottom, here)
    of a list
    
    Arguments:
        fileContents (list): the list to trim items from
        top (boolean): whether to trim from the top/front of the list
            (True) or from the bottom/back (False)
        indexes (int): the number of items to trim from the list
    """
    
    # Deepcopy the original so it doesn't get modified
    trimmed = deepcopy(bigList)
    # trim items from the top if top is set and add a colon at the new
    # front of the list
    if (top):
        trimmed = trimmed[indexes:]
        trimmed.insert(0, ':')
        
    # trim items from the bottom if top is not set
    if (not top):
        i = 0
        while i < indexes:
            trimmed.pop()
            i+=1
    
    return trimmed
    
def saveFile(contents, save, filename):
    """
    Saves a file to disk
    
    Arguments:
        contents (list): a list of lines to store into the file
        save (string): a y or an n of whether or not to create the file
        filename (string): the filename to save the file into
    Returns:
        nothing
    """
    # Adds a txt extension to the filename
    filename = (filename + ".txt")
    
    # Determins whether or not to save the file
    if (save == 'n'):
        print("Okay, done without saving")
        pass
    if (save == 'y'):
        # Opens the file for writing and saves the content into it
        with open(filename, "w") as output:
            for item in contents:
                output.write(item)
            output.write("\n")
        print("Saved file as " + filename)
            

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
    filename = getName()
    
    # Read the file
    fileContents = readFile(filename)
    
    # Parse the file.  Again, order matters here
    parsedFile = parseASCII(fileContents)
    parsedFile = parseWhitespace(parsedFile)
    parsedFile = parseFunction(parsedFile)
    
    # Cut off the extraneous garbage bytes from the top and bottom.
    parsedFile = trim(parsedFile, True, 73)
    parsedFile = trim(parsedFile, False, 3)
    
    # Create a string representation of the parsed file that can be
    # printed to the console
    string = ""
    for item in parsedFile:
        string += str(item)
    print(string)
    save = input("\n Would you like to save this output?  y/n: ")
    
    # Call saveFile to determine whether to save the output and save it
    saveFile(parsedFile, save, filename)
    

# Call the main method
main()
