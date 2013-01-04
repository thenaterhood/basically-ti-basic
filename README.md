Basically, TI-Basic
========

Software to make working with TI-Basic files much easier on the PC by decompiling
and recompiling the .8Xp files from the TI-83/TI-84 calculators.

Contents
------------

    ti_decode.py    a decompiler for TI-Basic files
    
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

That's about all that works acceptably well right now, so I haven't uploaded it yet in the assumption
I did something stupid.  In summary, reversing what ti_decode.py does seems to almost work, but not
completely.

Once I get the ti_encode.py file online I'll try to write some more formal documentation about what
the file metadata seems to be and how it comes about.

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
