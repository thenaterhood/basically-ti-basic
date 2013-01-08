Basically, TI-Basic
========

Software to make working with TI-Basic files much easier on the PC by decompiling
and recompiling the .8Xp files from the TI-83/TI-84 calculators.

Contents
------------

    ti_decode.py    a decompiler for TI-Basic files (TI-Basic -> text)
    ti_encode.py    a compiler for TI-Basic files (text -> TI-Basic)
    dictionaries.py the dictionaries required to compile and decompile
    tiFile.py       contains structures and functions for reading/writing/validating TI-Basic files
    common.py       contains common code for getting filenames, reading, and writing text files
    FIBO.8Xp        a compiled test program.  Calculates the Fibonacci sequence.
    
ti_decode.py
------------
ti_decode.py is a non-graphical program that pulls from TI .8Xp files and converts
the data to text.  It's rough around the edges and isn't quite finished, but 
it works in a pinch.  It will convert ASCII text and symbols (lowercase letters as well!),
whitespace, and a collection of TI-Basic functions to plaintext.  At the time of writing
this script, I did not have a full collection of functions to figure out, but it's easy
enough to add those.  I'll be finishing that off over the next while.

Note that the script does not parse lists that are called in the code at all.

Anything that isn't parsed will give back garbage, as python converts
the bytes to strings directly so they show up as b'\x00' (null character there, but
that's what they look like).  The software supports saving the output to a file so removing
any garbage with the text editor of your choice is easy.

ti_encode.py
------------
ti_encode.py is still a work in progress but it compiles files to TI-Basic.  Documentation is coming soon,
as there are still things that are a little shaky in terms of building the file metadata, although
that seems to work fairly well for small programs.  Larger programs may be a problem as some
of the hex values in the metadata change for larger programs and I haven't figured them out yet.

The main problems right now with compiling the files is a little trouble with whitespace, ascii, and
the metadata.  With that said, I'm able to successfully compile some small programs and get back
something recognizable.  The biggest problem is the metadata because without that, nothing will
accept the compiled file at all.  Keep reading for more on that.

8Xp Files
------------
The 8Xp files are fairly easy to decompile since they're basically only byte-compiled and fairly simple.
The program works with them by running through and matching up bytes to what they represent in plaintext.
After that, it cuts 72 bytes off the top of the file, which appears to be metadata and doesn't need
to be decoded to plaintext (it holds no benefit) and cuts 3 bytes off the bottom of the file.  Those
3 bytes don't appear to hold much importance because the file is still recognized without them.

The metadata is a little bit more interesting and the Internet doesn't hold much information about it.
The first 9 bytes are the same for every program and declare the type of file.  Easy enough, it's:

    **TI83F*[SUB][NEWLINE]
    
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

Disclaimer
------------
Be careful, don't be dumb, back up your stuff.  The software isn't currently aware of when it might
overwrite a file, so watch what you do with it.  It also doesn't do custom filenames (it will soon enough)
so watch out.

Installation, or How to Git
------------

To download and use the repository, you must check out the repository
from github into the directory of your choice using:

	git clone --recursive https://github.com/thenaterhood/basically-ti-basic.git ~/basically-ti-basic
	
This command clones the repository to the basically-ti-basic folder in your user directory.  If
you happened to put it somewhere other than the ~/basically-ti-basic folder, which is perfectly
acceptable, remember to adjust the following instructions accordingly.

After cloning the repository, you'll want to run
	
	cd ~/basically-ti-basic
	git submodule update --init --recursive
	
The --init flag initizlizes the submodule repositories and the --recursive flag
makes sure that nested submodules are initialized and updated as well.
	
You may want to learn more github commands in order to update specific files.


LICENSE
------------

thenaterhood/basically-ti-basic repository (c) 2012-2013 Nate Levesque (TheNaterhood)

[![Creative Commons License](http://i.creativecommons.org/l/by-sa/3.0/88x31.png)](http://creativecommons.org/licenses/by-sa/3.0/)

TL;DR: You can use, copy and modify this SO LONG AS you credit me and distribute your remixes with the same license.

This work is licensed under the [Creative Commons Attribution-ShareAlike 3.0 Unported License](http://creativecommons.org/licenses/by-sa/3.0/).

You should have received a copy of the license along with this
work. To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/3.0/ or send
a letter to Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.
