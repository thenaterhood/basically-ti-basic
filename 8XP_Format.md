8Xp Files
==========
The 8Xp files are fairly easy to decompile since they're basically only byte-compiled and fairly simple.
The program works with them by running through and matching up bytes to what they represent in plaintext.
After that, it cuts 72 bytes off the top of the file, which appears to be metadata and doesn't need
to be decoded to plaintext (it holds no benefit) and cuts 3 bytes off the bottom of the file.  Those
3 bytes don't appear to hold much importance because the file is still recognized without them.

The metadata is a little bit more interesting and the Internet doesn't hold much information about it.
The first 9 bytes are the same for every program and declare the type of file.  Easy enough, it's:

    `**TI83F*[SUB][NEWLINE]`

The next line holds a comment.  The TI calculator uses this to datestamp the (creation?) of the file.  The comment is
40 characters (bytes) long, preceded by and ending with a NUL character.  Another NUL character follows then a hexadecimal
value.  The hexadecimal value doesn't seem to be extremely important as changing it arbitrarily in my test
programs doesn't seem to have any effect on their being decompiled (online software doing the decoding since
it's much pickier than mine).  The byte after it however is a little more important and changing it does some weird
things that I don't understand given my knowledge of the files.  It appears to denote something regarding
the size or length of the code since it stays the same for programs of the same relative size.  Given that, the line
looks something like:

    [NUL]40 character comment[NUL][NUL]hex value[NUL or STX looking at my program collection][NEWLINE]

The next and final line is a little more interesting and much more crucial to the file actually being usable.
It starts with a NUL character, followed by the size of the code (excluding the size of the metadata and footer).
If this value is invalid it causes some bigger problems, as the decompiler used to confirm results will stop
interpreting anything past the number of bytes the file claims to be.  This is followed by a byte that functions
as a carry bit.  Since the maximum value a single byte can hold is 255, if the size of the program is over 255 bytes
then the next byte is set.  The next section of the line is the name of the program, starting
with a [ENQ] character.  The name is limited to 8 bytes, and therein capital letters.  Any unused bytes are filled
with [NUL] characters.  The two bytes after this are [NUL] characters as well which might suggest that the file
itself could permit longer names although the 8 characters is all that fits on the calculator screen's place
for it.  This is followed by the size again and a carry byte, like the second two characters of the line.
After this is what appears to be the size - 2, and a carry byte for the size-2.  So, put together
the line ends up looking like this:

    [NUL]program size, carry byte[ENQ]prgmname[NUL][NUL]program size, carry byte, prgm size - 2, carry byte

Then the compiled code for the program follows
