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
    
    # Opens the file and reads it one word at a time into an array
    for line in open(filename, "r"):
        fileContents.append(line)
        
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
    try:
        for i in range(0, len(fileContents)):
            if (fileContents[i][0] == ":"):
                parsedFile.append(b'?')
                parsedFile.append(fileContents[i][1:])
                            
            if (fileContents[i][0] != ":"):
                parsedFile.append(fileContents[i])
    except:
        pass
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
        
    if (unParsed[0] == '"'):
        parsed = parseASCII(unParsed)
        return parseWhitespace(parsed)
        
    # Checks to see if the line starts with a function definition,
    # and if it does converts it to the appropriate token then
    # calls the function again for the continuation of the line
    """
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
    return line
            

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
        stripped_dict[key.strip(' ,\n')] = function_dict[key]
    
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
    
def getSize(size):
    """
    Determines the size value to use for the compile TI-Basic header
    
    Arguments:
        size (int): the size in bytes of the data
    Returns:
        sizebytes (list): the size value and its following byte
    """
    # The absolute largest possible size that the TI-Basic file is
    # allowed to be, based on current knowledge of the metadata.
    absoluteLimit = 255*255
    
    headerSize = []
    
    if (size <= 255):
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
        raise RuntimeError("File is beyond the allowed size for compiled TI-Basic files: yours: " +str(size) +", limit:" +str(absoluteLimit))

    return headerSize
    
def createHeader(content, name):
    header = []
    # Appends the TI83 filetype header to the header file, followed
    # by its newline.  In ascii, header is **TI83F*[SUB][NEWLINE]
    filetype = dictionaries.mimetype()
    
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
    # 2 since in comparison with known files, there always seems to be 2
    # bytes short, possibly because the file has no footer.
    
    size = (len(content)+2)
    
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
    
    # Create the series of bytes that holds the name.  Splits the name
    # that's known into bytes and adds 9 null bytes after it to make sure
    # it is the right length.  Then takes the first 9 bytes of the resulting
    nameAppend = []
    name = name[0:9] 
       
    for char in name:
        nameAppend.append(char.encode('ascii', 'strict'))
    
    while len(nameAppend) < 8:
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
        try:
            parsed = parsed + parseLine(line)
        except:
            parsed = parsed + [parseLine(line)]
    
    # Splits the remainder into pieces and parses it like before.        
    split = []
    for i in range(0,len(parsed)):
        if (isinstance(parsed[i], str)):
            split = split + parsed[i].strip(':').split() 
        else:
            split.append(parsed[i])
   
    parsed = split

    # Parse the file.  Again, order matters here
    tiData.prgmdata = parseWhitespace(parsed)
    tiData.prgmdata = parseFunction(tiData.prgmdata)
    tiData.prgmdata = splitBytes(tiData.prgmdata)
    tiData.prgmdata = parseASCII(tiData.prgmdata)
    tiData.prgmdata = parseWhitespace(tiData.prgmdata)

    
    # Break the name of the program off the filename
    name = (filename.split('.')[0])
    
    # Add the metadata and a footer of null bytes to the tidata object
    tiData.metadata = createHeader(tiData.prgmdata, name)
    tiData.footer = [b'\x00', b'\x00']
    
    # Write the tile to disk
    tiFile.write(name, tiData)
    

# Call the main method
main()
