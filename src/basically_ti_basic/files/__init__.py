"""
author: Nate Levesque <public@thenaterhood.com>
description: Reads and writes TI-Basic .8Xp files and returns
    structures relevant to the file if appropriate.

TODO:
    add additional validation to the validate function

    figure out why when reading the file, the first byte
    goes missing
"""

class TIPrgmFile(object):
    """
    Defines a data object to hold sections of a TI-Basic
    program file
    """
    __slots__=('metadata', 'prgmdata', 'footer')

    def __init__(self, fname=None):
        """
        Initializes the fields of the struct
        to empty fields if called without arguments or reads
        in a tiBasic file if a filename is given.

        Arguments:
            fname (str, optional): a 8xp filename to read
        """

        if fname is not None:
            self.read(fname)
        else:
            self.metadata = None
            self.prgmdata = None
            self.footer = None

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
            self.prgmdata = None
            self.footer = None

        else:
            self.prgmdata = fileContents[73:len(fileContents)-3]
            self.footer = fileContents[len(fileContents)-3:len(fileContents)]

    def writeOut(self, filename):
        """
        Writes a .8xp TI-Basic file to disk as bytes

        Arguments:
           filename (str): the name of the file to write

        Returns:
            fileWritten (boolean): a boolean value of whether or not the file
                has been written
        """

        # Add the .8xp extension to the filename
        name = filename.split(".")[0].upper()
        self._createMetadata(name)

        with open(filename, "wb") as outFile:
            # Writes the program file to disk
            self._writeBytes(outFile, self.metadata)
            self._writeBytes(outFile, self.prgmdata)
            if self.footer is not None:
                self._writeBytes(outFile, self.footer)
            else:
                print("WARNING: No file footer data was generated.")

    def getMimetype():
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

        if (fileType != TIPrgmFile.getMimetype()[1:]):
            return False

        return True

    def _writeBytes(self, openFile, data):
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

    def _convertSizeForHeader(self, size):
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

        if (size >= absoluteLimit):
            # Raise an error, since the file size can't be beyond the
            # size defined in the absoluteLimit variable
            raise RuntimeError("File is beyond the allowed size for compiled TI-Basic files: yours: " +str(size) +", limit:" +str(absoluteLimit))

        headerSize = []

        carrybyte = bytes([size//255])
        sizebyte = bytes([ size - (255 * (size // 255)) ])
        headerSize.append(sizebyte)
        headerSize.append(carrybyte)

        # If the program is beyond the size that the file will allow,
        # an error needs to be raised because the file metadata doesn't
        # seem to make it possible for it to be larger.  Current limit
        # appears to be 255*255 providing I can math tonight.

        return headerSize

    def _createMetadata(self, name):
        header = []
        # Appends the TI83 filetype header to the header file, followed
        # by its newline.  In ascii, header is **TI83F*[SUB][NEWLINE]
        filetype = TIPrgmFile.getMimetype()

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

        size = (len(self.prgmdata)+2)

        header = header + self._convertSizeForHeader(size)

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
        header = header + self._convertSizeForHeader(size)

        # Adding the next value, which appears to be the number of bytes in the
        # file excluding the header -2.  Consistent between different
        # program sizes
        header = header + self._convertSizeForHeader(size-2)

        self.metadata = header
