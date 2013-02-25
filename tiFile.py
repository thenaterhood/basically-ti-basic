"""
file: ti_file.py
language: python3
author: Nate Levesque <public@thenaterhood.com>
description: Reads and writes TI-Basic .8Xp files and returns
    structures relevant to the file if appropriate.
    
TODO:
    add additional validation to the validate function
    
    figure out why when reading the file, the first byte
    goes missing
"""
import dictionaries
from metadata import mimetype

class tiFile():
    """
    Defines a data object to hold sections of a TI-Basic
    program file
    """
    __slots__=('metadata', 'prgmdata', 'footer')
    
    def __init__(self, fname = False ):
        """
        Initializes the fields of the struct
        to empty fields if called without arguments or reads
        in a tiBasic file if a filename is given.
        
        Arguments:
            fname (str, optional): a 8xp filename to read
        """
        
        if ( fname ):
            self.read( fname )
        else:
            
            self.metadata = False
            self.prgmdata = False
            self.footer = False
        
    def read(self, filename):
        """
        Reads a TI-Basic .8xp file byte by byte
        and populates the fields of the data object that
        represents it
        
        Arguments:
            filename (str): the filename of a .8xp file to open, inc extension
            
        Returns:
            fileData (tiFile): a tiFile object
            
        """
        
        # Reads the file into an array of bytes
        fileData = tiFile()
        fileContents = []
        with open(filename, "rb") as inStream:
            byte = inStream.read(1)
            while byte:
                byte = inStream.read(1)
                fileContents.append(byte)
        
        # Attempts to extract the metadata and raises an error
        # if the array is too short to contain any
        try:
            self.metadata = fileContents[:73]
        except:
            raise RuntimeError("File is too short to be a .8xp file.")
        
        # raises a warning if the array is too short to contain program 
        # data and a footer    
        if (len(fileContents) < 74):
            print("WARNING: File is only long enough to contain metadata.")
            self.prgmdata = False
            self.footer = False
            
        else:
            self.prgmdata = fileContents[73:len(fileContents)-3]
            self.footer = fileContents[len(fileContents)-3:len(fileContents)]
            
    def write(self, filename):
        """
        Writes a .8xp TI-Basic file to disk as bytes
         
        Arguments:
           filename (str): the name of the file to write
            
        Returns:
            fileWritten (boolean): a boolean value of whether or not the file
                has been written
        """
        
        # Add the .8xp extension to the filename
        filename = (filename.split('.')[0] + ".8Xp")
        
        # Opens the file to write binary
        outFile = open(filename, "wb")
        
        # Writes the program file to disk
        self.writeBytes(outFile, self.metadata)
        self.writeBytes(outFile, self.prgmdata)
        self.writeBytes(outFile, self.footer)
        
        # Returns true for now, will later possibly perform some check to
        # make sure it wrote what it intended.  For now needs to just
        # write the whole thing or fail, makes it easier to debug the encode
        # function if a big problem pops up        
        return True
        
    def validate(self):
        """
        Validates that a .8Xp file is actually a .8Xp file.
        Currently only checks sections of the metadata.  For now
        is primarily so the decode program doesn't try decoding things
        that are not TI-Basic files.
        
        Arguments:
			self
                
        Returns:
            valid (boolean): a boolean value indicating if the file is valid
        """    
        fileType = self.metadata[:9]
        # Validating against bytes 1-9 of the mimetype.
        # for some reason the first byte of the file doesn't get read
        # which will need to be looked into

        if (fileType != mimetype()[1:]):
            return False
        
        return True
        
    def writeBytes(self, openFile, data):
        """
        Iterates through a list of bytes and writes them to a file.
        Arguments:
            openFile (file): an open file
            data (list): a list of bytes to write
        """
        for byte in data:
            if (isinstance(byte, bytes)):
                openFile.write(byte)
            else:
                print("Error writing byte to file.  Was '"+str(byte)+"'.  Compiled file might have problems.")
                    
    def __str__(self):
        """
        Returns a string representation of the TI data object
        """
        string = "TI File Data Object"
        if ( self.metadata ):
            string += "\n Contains metadata"
        if ( self.prgmdata ):
            string += "\n Contains program data"
        if ( self.footer ):
            string += "\n Contains footer data" 
            
        return string    




