"""
file: common.py
language: python3
author: Nate Levesque <public@thenaterhood.com>
description: Contains generic functions for reading, writing, and
    retrieving files.
    
TODO:
    
"""
def getFName():
    """
    Requests the name of a file from the user and verifies
    that the file actually exists before returning it.
    
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

def saveFile(contents, filename):
    """
    Saves a file to disk from a list of lines in the file
    
    Arguments:
        contents (list): a list of lines to store into the file
        filename (string): the filename to save the file into
    Returns:
        nothing
    """
    # Adds a txt extension to the filename
    filename = (filename + ".txt")
    
    with open(filename, "w") as output:
        for item in contents:
            output.write(item)
        print("Saved file as " + filename)
