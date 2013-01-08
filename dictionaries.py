"""
file: dictionaries.py
language: python3
author: Nate Levesque <public@thenaterhood.com>
description: Contains functions that return the dictionaries
    required to decompile and compile TI-Basic.  Intended to be imported
    by another program.
    
TODO:
    Finish the dictionary defining TI-Basic functions
"""
def reverseDictionary(dictionary):
    """
    Reverses a dictionary so that the keys become the values.  Mainly
    so that the existing dictionaries for decompiling the TI-Basic files
    can be used here as well.
    
    Arguments:
        dictionary (dict): a dictionary to flip
    Returns:
        flipped (dict): a dictionary with the key/value pairs reversed
    """
    flipped = dict()
    for key in dictionary:
        flipped[dictionary[key].strip()] = key
     
    return flipped
    

def standardASCII(flip):
    """
    Maps binary ascii values to plaintext.
    
    Arguments:
        flip (boolean): whether to reverse the key/value pairs before
            returning the dictionary
    Returns:
        dictionary (dict): A dictionary mapping binary ascii codes to
            plaintext
    """
    dictionary = dict([
    (b'A', 'A'),
    (b'B', 'B'),
    (b'C', 'C'),
    (b'D', 'D'),
    (b'E', 'E'),
    (b'F', 'F'),
    (b'G', 'G'),
    (b'H', 'H'),
    (b'I', 'I'),
    (b'J', 'J'),
    (b'K', 'K'),
    (b'L', 'L'),
    (b'M', 'M'),
    (b'N', 'N'),
    (b'O', 'O'),
    (b'P', 'P'),
    (b'Q', 'Q'),
    (b'R', 'R'),
    (b'S', 'S'),
    (b'T', 'T'),
    (b'U', 'U'),
    (b'V', 'V'),
    (b'W', 'W'),
    (b'X', 'X'),
    (b'Y', 'Y'),
    (b'Z', 'Z'),
    (b'0', '0'),
    (b'1', '1'),
    (b'2', '2'),
    (b'3', '3'),
    (b'4', '4'),
    (b'5', '5'),
    (b'6', '6'),
    (b'7', '7'),
    (b'8', '8'),
    (b'9', '9')
    ])
    
    if (flip):
        return reverseDictionary(dictionary)
    else:
        return dictionary
        
def lowercaseASCII(flip):
    """
    Maps TI-Basic binary values for lowercase letters to plaintext.  Does
    not include the escape characters that TI-Basic files use to denote
    lowercase letters in the compiled files.
    
    Arguments:
        flip (boolean): whether to reverse the key/value pairs before
            returning the dictionary
    Returns:
        dictionary (dict): a dictionary mapping TI-Basic binary values
            for lowercase letters to plaintext
    """
    dictionary = dict([
    (b'\xb0', 'a'),
    (b'\xb1', 'b'),
    (b'\xb2', 'c'),
    (b'\xb3', 'd'),
    (b'\xb4', 'e'),
    (b'\xb5', 'f'),
    (b'\xb6', 'g'),
    (b'\xb7', 'h'),
    (b'\xb8', 'i'),
    (b'\xb9', 'j'),
    (b'\xba', 'k'),
    (b'\xbc', 'l'),
    (b'\xbd', 'm'),
    (b'\xbe', 'n'),
    (b'\xbf', 'o'),
    (b'\xc0', 'p'),
    (b'\xc1', 'q'),
    (b'\xc2', 'r'),
    (b'\xc3', 's'),
    (b'\xc4', 't'),
    (b'\xc5', 'u'),
    (b'\xc6', 'v'),
    (b'\xc7', 'w'),
    (b'\xc8', 'x'),
    (b'\xc9', 'y'),
    (b'\xca', 'z')
    ])
    
    if (flip):
        return reverseDictionary(dictionary)
    else:
        return dictionary
    
def symbolsASCII(flip):
    """
    Maps TI-Basic binary codes for ascii symbols and operators to plaintext
    
    Arguments:
        flip (boolean): whether to reverse the key/value pairs before
            returning the dictionary
    Returns:
        dictionary (dict): a dictionary mapping the TI-Basic values to
            plaintext.
    """
    dictionary = dict([
    (b'>', ':'),
    (b'\x83', '/'),
    (b'q', '-'),
    (b'j', '='),
    (b'+', ','),
    (b'\x10', '('),
    (b'\x11', ')'),
    (b'k', '<'),
    (b'l', '>'),
    (b'o', '!='),
    (b'p', '+'),
    (b':', '.'),
    (b'n', '>='),
    (b'm', '<='),
    (b'\xb0', '{-}'),
    (b'\n', '('),
    (b'\x06', '['),
    (b'\xaf', '?'),
    (b'\xf0', '^'),
    (b'*', '"')

    ])
    
    if (flip):
        return reverseDictionary(dictionary)
    else:
        return dictionary
    
def whitespace(flip):
    """
    Returns a dictionary mapping TI-Basic binary codes for whitespace
    to their plaintext equivalent.  Works with spaces and newlines.
    
    Arguments:
        flip (boolean): whether to reverse the key/value pairs before
            returning the dictionary
    Returns:
        dictionary (dict): a dictionary mapping TI-Basic whitespace to 
            plaintext
    """
    dictionary = dict([
    (b'?', '\n:'),
    (b')', ' ')
    ])
    
    if (flip):
        return reverseDictionary(dictionary)
    else:
        return dictionary
    
def tibasicFunctions(flip):
    """
    Returns a dictionary mapping TI-Basic tokens for functions to their
    plaintext equivalents.
    
    Arguments:
        flip (boolean): whether to reverse the key/value pairs before
            returning the dictionary
    Returns:
        dictionary (dict): a dictionary mapping the TI-Basic compiled
            tokens to their plaintext values.
            
    TODO:
        Add the remainder of TI-Basic functions to the dictionary
    """
    dictionary = dict([
    (b'\xde', 'Disp '),
    (b'\xdd', 'Prompt '),
    (b'\xce', 'If '),
    (b'\x04', ' -> '),
    (b'\xbb', 'randInt'),
    (b'\xd6', 'Lbl '),
    (b'\xe0', 'Output('),
    (b'\xd9', 'Stop'),
    (b'\xe1', 'ClrHome'),
    (b'\xd1', 'While '),
    (b'@', ' and '),
    (b'<', ' or '),
    (b'\xd4', 'End'),
    (b'\xad', 'getKey'),
    (b'r', 'Ans'),
    (b'\xd7', 'Goto ')
    ])
    
    if (flip):
        return reverseDictionary(dictionary)
    else:
        return dictionary
        
def mimetype():
    """
    Returns a list containing the bytes that define the mimetype
    of a TI-Basic .8Xp file
    
    Arguments:
        none
    Returns:
        (list): a list containing the bytes that define the mimetype
            of the TI 83 program files
    """
    return [b'*',b'*',b'T',b'I',b'8',b'3',b'F',b'*',b'\x1a',b'\n']
