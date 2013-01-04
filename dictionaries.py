"""
file: dictionaries.py
language: python3
author: Nate Levesque <public@thenaterhood.com>
description: Contains functions that return the dictionaries
    required to decompile and compile TI-Basic
    
TODO:
    add functionality to return the reversed dictionary for compiling
"""
def standardASCII():
    """
    Maps binary ascii values to plaintext.
    
    Arguments:
        none
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
    (b'*', '"'),
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
    
    return dictionary
    
def lowercaseASCII():
    """
    Maps TI-Basic binary values for lowercase letters to plaintext.  Does
    not include the escape characters that TI-Basic files use to denote
    lowercase letters in the compiled files.
    
    Arguments:
        none
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
    
    return dictionary
    
def symbolsASCII():
    """
    Maps TI-Basic binary codes for ascii symbols and operators to plaintext
    
    Arguments:
        none
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
    (b'\xf0', '^')
    ])
    
    return dictionary
    
def whitespace():
    """
    Returns a dictionary mapping TI-Basic binary codes for whitespace
    to their plaintext equivalent.  Works with spaces and newlines.
    
    Arguments:
        none
    Returns:
        dictionary (dict): a dictionary mapping TI-Basic whitespace to 
            plaintext
    """
    dictionary = dict([
    (b'?', '\n:'),
    (b')', ' ')
    ])
    
    return dictionary
    
def tibasicFunctions():
    """
    Returns a dictionary mapping TI-Basic tokens for functions to their
    plaintext equivalents.
    
    Arguments:
        none
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
    
    return dictionary
