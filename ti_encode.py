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
    
    Find a better way to encode hex values into bytes so the program
    size isn't limited
    
"""
import binascii
from copy import deepcopy
import dictionaries


def init():    
    print("TI BASIC file encoder.  Compiles text to TIBASIC.\n")
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
        filename = input("Enter the name of the file to compile, including the .8Xp extension: ")

        try:
            file = open(filename, 'r')
            file.close()
            return filename
        except:
            print("File could not be found.")
    # Code below is for rapid debugging, should be commented
    #return "FIBO2.txt"
    
def readFile(filename):
    """
    Reads a file into an array as byte values
    
    Arguments:
        filename (string): the name of the file to open
    Returns:
        fileContents (list): byte values from the file
        
    """
    fileContents = []
    
    # Opens the file and reads it one word at a time into an array
    for line in open(filename, "r"):
        for word in line.split():
            fileContents.append(word)
        
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
    whitespace_dict = dictionaries.whitespace(True)
    
    parsedFile = []
    for i in range(0, len(fileContents)):
        if (fileContents[i][0] == ":"):
            parsedFile.append(b'?')
            parsedFile.append(fileContents[i][1:])
                        
        if (fileContents[i][0] != ":"):
            parsedFile.append(fileContents[i])
    
    #return translate(whitespace_dict, fileContents, False, '')
    return parsedFile

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
    return translate(function_dict, fileContents, False, '')

def splitBytes(contents):
    """
    Splits a list of items up into bytes.
    
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
    
def getSize(size):
    """
    Determines the size value to use for the compile TI-Basic header
    
    Arguments:
        size (int): the size in bytes of the data
    Returns:
        sizebytes (list): the size value and it's following byte
    """
    # The absolute largest possible size that the TI-Basic file is
    # allowed to be, based on current knowledge of the metadata.
    absoluteLimit = 255*255
    
    headerSize = []
    if (size < 256):
        sizebyte = bytes([size])
        headerSize.append(sizebyte)
        headerSize.append(b'\x00')
    if (size >= 255 and size < absoluteLimit):
        carrybyte = bytes([size//255])
        sizebyte = bytes([ size - (255 * (size // 255)) ])
        headerSize.append(sizebyte)
        headerSize.append(carrybyte)
        
    # If the program is beyond the size that the file will allow,
    # an error needs to be raised because the file metadata doesn't
    # seem to make it possible for it to be larger.  Current limit
    # appears to be 255*255 providing I can math tonight.
    
    if (size >= absoluteLimit):
        # Raise an error, since the file size can't be beyond the
        # size defined in the absoluteLimit variable
        raise ValueError("File is beyond the allowed size for compiled TI-Basic files: yours: " +str(size) +", limit:" +str(absoluteLimit))

    return headerSize
    
def createHeader(content, name):
    header = []
    # Appends the TI83 filetype header to the header file, followed
    # by its newline.  In ascii, header is **TI83F*[SUB][NEWLINE]
    filetype=[b'*',b'*',b'T',b'I',b'8',b'3',b'F',b'*',b'\x1a',b'\n']
    
    for item in filetype:
        header.append(item)
    
    # Appends a comment area of metadata to the header
    # Follows the form [NULL]40 characters[NULL]character[NULL][NULL][hex code][NEWLINE]
    # If the comment contains fewer than 40 characters, the unused 
    # characters are filled with null characters.  It appears that
    # more than 40 characters can be put here, but then the hex codes
    # at the end change. It doesn't seem to do anything,
    # but with over 40 characters it doesn't seem to be needed.
    # So, using the extra characters this section of the header becomes
    # [NULL]comment string, 42 chars[DC4][NULL][NEWLINE]
    
    # The comment appears to just be plain ASCII text, so not using
    # binary for it here.
    
    header.append(b'\x00')
    comment = "Encoding software from TheNaterhood....."
    for char in comment:
        header.append(char.encode('ascii', 'strict'))
        
    header.append(b'\x00')
    header.append(b'\x00')
    
    # This is the character that hasn't been figured out.  It doesn't
    # seem to matter what it is so using N for now.
    header.append(b'N')
    
    # This is the hex code that does change per program but hasn't
    # been figured out yet.  Using null for now to see if it makes
    # a difference
    header.append(b'\x00')
    header.append(b'\n')
    
    # This is a longer line.  It contains information about the file
    # such as the name of the program and the size of the program.
    # It starts with a null character.
    
    header.append(b'\x00')
    
    # Next is the size of the file in bytes, so we take the contents
    # of the parsed file and just check the length since each byte is
    # an entry in the list.  That gets added to the header.  Adding
    # 3 since in comparison with known files, there always seems to be 3
    # bytes short, possibly because the file has no footer.
    
    size = (len(content)+3)
    
    header = header + getSize(size)
    
    # Add the null character that comes after the size.  This is not
    # always a null character, but for now treating it as such to 
    # see if it works.  Will most likely work for smaller programs but
    # might be a problem for larger ones.  Previous line now
    # also adds this byte.  Worth noting: if there is an extra null
    # character at this point, the program is interpreted as a boxplot
    #header.append(b'\x00')
    
    # Adds the character that denotes the start of the name
    header.append(b'\x05')
    
    # Add the name of the file, which is limited to 8 characters and 
    # followed by 2 NULL characters.
    
    nameAppend = []
    name = name[0:9]
    for char in name:
        nameAppend.append(char.encode('ascii', 'strict'))
    
    while len(nameAppend) < 9:
        nameAppend.append(b'\x00')
        
    for char in nameAppend:
        header.append(char)
        
    header.append(b'\x00')
    header.append(b'\x00')
    
    # Adding the size a second time as it is repeated after the name
    header = header + getSize(size)
    
    # Adding the next value, which appears to be the number of bytes in the
    # file excluding the header -2.  Consistent between different
    # program sizes
    header = header + getSize(size-2)
    
    return header
    
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
    filename = (filename.split('.')[0] + ".8Xp")
    
    # Determins whether or not to save the file
    if (save == 'n'):
        print("Okay, done without saving")
        pass
    if (save == 'y'):
        # Opens the file for writing and saves the content into it
        file = open(filename, "wb")
        for item in contents:
            if (not isinstance(item, str)):
                file.write(item)
            if (isinstance(item, str)):
                print("Error writing byte to file.  Was string ("+item+").  Continuing, but compiled file might have problems.")
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
    parsedFile = parseWhitespace(fileContents)
    parsedFile = parseFunction(parsedFile)
    parsedFile = splitBytes(parsedFile)
    parsedFile = parseASCII(parsedFile)
    
    # Break the name of the program off the filename
    name = (filename.split('.')[0])

    # Create the file header/metadata
    header = createHeader(parsedFile, name)
     
    # Concatonate the metadata to the front of the list
    parsedFile = (header + parsedFile)
    
    # Create a string representation of the parsed file that can be
    # printed to the console
    #string = ""
    #for item in parsedFile:
    #    string += str(item)
    #print(string)

    save = input("\n Would you like to save this output?  y/n: ")
    # Call saveFile to determine whether to save the output and save it
    saveFile(parsedFile, save, filename)
    

# Call the main method
main()
