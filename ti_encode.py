"""
file: ti_encode.py
language: python3
author: Nate Levesque <public@thenaterhood.com>
description: Compiles plaintext to TI-Basic files and saves the file.

TODO:
    complete overhaul of how the file is read so that comments and
    text stop being a problem.
    
    Syntax checking.  Dream big, right?  Few basics would be nice, shouln't
    be too hard
    
    validation to make sure the file put in is actually a text file.  Doesn't
    break things if it isn't but it looks nasty
    
"""
import binascii
from copy import deepcopy
import dictionaries
import tiFile
import common
from metadata import createMeta


def init():    
    print("TI BASIC file encoder.  Compiles text to TIBASIC.\n")
    print("Nate Levesque <public@thenaterhood.com>.")
    print("Visit www.thenaterhood.com/projects for more software\n")
    
def readFile(filename):
    """
    Reads a file into an array as chunks separated by spaces.
    
    Arguments:
        filename (string): the name of the file to open
    Returns:
        fileContents (list): byte values from the file
        
    """
    fileContents = []
    
    # Opens the file and reads it one line at a time into an array
    for line in open(filename, "r"):
        fileContents.append(line)
        fileContents.append(b'?')
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
    #translation = deepcopy(content)
    translation = []

    # Iterate through each index of the copy of the content
    for item in content:
        # If there is no escape character set, check if the item
        # exists in the dictionary and replace it with its value if it does
        if ( not escapeCharExists) and (item in dictionary):
            translation.append(dictionary[item])
                
        # If an escape character is set and the character at the current
        # iteration was found in the dictionary, switch out the item for
        # its compiled byte value and insert the escape character into
        # the preceding index.
        if (escapeCharExists and item in dictionary):
            translation.append(dictionary[item])
            translation.insert(-1, escapeChar)
                    
        elif (item not in dictionary):
            translation.append(item)
                
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
    
    # Grab the dictionary with values for ascii uppercase and numbers
    # and reverse the key/value pairs since the dictionary is written
    # for decompiling
    ascii_dict = dictionaries.standardASCII(True)
    
    # Call translate with the uppercase dictionary, the file contents
    # and no escape code set.
    ascii_parsed = translate(ascii_dict, ascii_parsed, False, '')
      
    # Grab the dictionary with values for the lowercase letters
    # and reverse the key/value pairs since the dictionary is written
    # for decompiling
    ascii_lower_dict = dictionaries.lowercaseASCII(True)    
    
    # Call translate with the lowercase dictionary, the file contents,
    # and the escape character b'\xbb' set
    ascii_parsed = translate(ascii_lower_dict, ascii_parsed, True, b'\xbb')
    
    # Grab the dictionary mapping symbols to their plaintext values and
    # reverse the key/values since the dictionary is written for decompiling.    
    ascii_symbol_dict = dictionaries.symbolsASCII(True)
    
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
    
    parsedFile = []
    """
    try:
        for i in range(0, len(fileContents)):
            if (fileContents[i][0] == ":"):
                parsedFile.append(b'?')
                parsedFile.append(fileContents[i][1:])
                            
            if (fileContents[i][0] != ":"):
                parsedFile.append(fileContents[i])
    except:
        pass
    """
    # Commented, because doing this doesn't actually hold any benefit
    # with how the file is currently dealt with
    
    whitespace_dict = dictionaries.whitespace(True)
    return translate(whitespace_dict, fileContents, False, '')
    #return parsedFile
    
def parseLine(line):
    """
    Parses a line of TI-Basic code from plaintext -> tiBasic.
    Observes text and comments, so such things are now safe to compile.
    Runs through and parses comments and text, followed by newlines,
    followed by TI-Basic tokens.
    
    Arguments:
        line (str): a line of plaintext tibasic code
    Returns:
        parsedLine (list): a list of bytes from the parsed line
    """
    unParsed = deepcopy(line)[1:]
    
    # Parse any comments in the line, denoted by '"', as 
    # they should be in tibasic.  This section works as expected.

    if (len(unParsed) == 0):
        return ''
      
    for i in range(0, len(unParsed)):
        if (unParsed[i] == '"'):
            parsed = [ unParsed[:i] ] + parseWhitespace( parseASCII(unParsed[i:]) )
            return parsed
        
    """   
    # Checks to see if the line starts with a function definition,
    # and if it does converts it to the appropriate token then
    # calls the function again for the continuation of the line
    unParsedLineStart = unParsed.split()[0]
    
    try:
        function = dictionaries.tibasicFunctions(True)[unParsedLineStart]
    except:
        function = dictionaries.tibasicFunctions(True)[unParsedLineStart + " "]
    
    if ( function in dictionaries.tibasicFunctions(True)):
        textLength = len(unParsed.split()[0])
        nextSection = parseLine(unParsed[textLength:])
        print(nextSection)
        
        if (not isinstance(nextSection, list)):
            nextSection = [nextSection]
        parsed = [dictionaries.tibasicFunctions(True)[unParsed.split()[0]] ] + nextSection
        #parsed = parseASCII(parsed)
        #parsed = parseWhitespace(parsed)
        return parsed
        
    else:
        return parseASCII(line)
    """
    return [line]
            

def parseFunction(fileContents):
    """
    Converts the TI83 byte values for TI-BASIC functions to plaintext
    
    Arguments:
        fileContents (list): a list of byte values read from the file
    Returns:
        a list with the byte values for functions replaced with their
        plaintext equivalents
    """
    
    # Grab the dictionary mapping function hex codes to their plaintext 
    # values and reverse the key/values since the dictionary is written
    # for decompiling.
    function_dict = dictionaries.tibasicFunctions(True)

    # calls the translate function with the function dictionary,
    # contents of the file, and no escape character set
    parsed = translate(function_dict, fileContents, False, '')
    # Because of issues with spaces, now stripping spaces from the
    # code and trying again.
    stripped_dict = dict()
    for key in function_dict:
        stripped_dict[key.strip()] = function_dict[key]
    
    parsed = translate(stripped_dict, parsed, False, '')
    
    return parsed

def splitBytes(contents):
    """
    Splits a list of items up into byte-sized chunks.  They'd probably
    taste nice on salad.
    
    Arguments:
        contents (list): a list of strings
    Returns:
        splitBytes (list): a list of bytes
    """
    splitBytes = []
    
    for item in contents:
        if (isinstance(item, str)):
            for byte in item:
                splitBytes.append(byte)
        if (not isinstance(item, str)):
            splitBytes.append(item)
    
    
    return splitBytes

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
    tiData = tiFile.tiFile()
    
    # Read the file
    fileContents = readFile(filename)
    
    # Parses any code comments
    parsed = []
    for line in fileContents:
        if ( isinstance(line, list) or isinstance(line, str) ):
            parsed = parsed + parseLine(line)

        else:
            parsed = parsed + [line]
                    
    
    # Splits the remainder into pieces and parses it like before.        
    split = []
    for i in range(0,len(parsed)):
        if (isinstance(parsed[i], str)):
            split = split + parsed[i].strip(':').split() 
        else:
            split.append(parsed[i])
   
    parsed = split

    # Parse the file.  Again, order matters here
    #tiData.prgmdata = parseWhitespace(parsed)
    tiData.prgmdata = parseFunction(parsed)
    tiData.prgmdata = splitBytes(tiData.prgmdata)
    tiData.prgmdata = parseASCII(tiData.prgmdata)
    #tiData.prgmdata = parseWhitespace(tiData.prgmdata)

    
    # Break the name of the program off the filename
    name = (filename.split('.')[0])
    
    # Add the metadata and a footer of null bytes to the tidata object
    tiData.metadata = createMeta(tiData.prgmdata, name)
    tiData.footer = [b'\x00', b'\x00']
    
    # Write the tile to disk
    tiFile.write(name, tiData)
    

# Call the main method
main()
