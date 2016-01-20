Basically, TI-Basic
========

Software to make working with TI-Basic files much easier on the PC by decompiling
and recompiling the .8Xp files from the TI-83/TI-84 calculators. For more
information about the 8Xp file format, see the site listed in the credits and
the 8XP_Format.md file, which contains additional reverse-engineered
information.

Installation
------------
basically_ti_basic can be installed like any other typical Python package.
Once Python (3+) is installed on the target system, simply clone the repository
and navigate to the cloned repository in the command line. Once there, run
`python setup.py install`. You should be good to go.

Usage
------------
basically_ti_basic provides a command line utility and a few libraries.

The command line utility should be available in your shell as the command
`basically-ti-basic`. The utility allows for compilation and decompilation of
TI-83+ .8Xp files. It provides the option to write the result to a file or
print it to the console. Some usage examples:

Open the file FIBO.8Xp, decompile it, and save the result to FIBO.txt

`$ basically-ti-basic -d -i FIBO.8Xp -o FIBO.txt`

Open the file FIBO.txt, compile it, and save the result to FIBO.8Xp

`$ basically-ti-basic -c -i FIBO.txt -o FIBO.8Xp`

Open the file FIBO.8Xp, decompile it, and print the result to the console

`$ basically-ti-basic -d -i FIBO.8Xp`

basically_ti_basic can also be imported into other applications. The libraries
that may interest you the most are:

* `basically_ti_basic.tokens`: Contains a dictionary of tokens to strings, and two functions for manipulating it (mainly, a flip so that the same dictionary can be used for compilation and decompilation).

* `basically_ti_basic.compiler.PrgmCompiler`: Provides compilation and decompilation functionality.

* `basically_ti_basic.files.TIPrgmFile`: Structure that represents a TI Program file and provides methods for generating the file headers.

**Heads Up! The TI file creation (compilation) functionality is incomplete and
may produce malformed files. Use it with caution and make sure to back up your
calculator before loading any compiled files onto it.**


LICENSE
------------
basically_ti_basic is licensed under the MIT license. The full license text
can be found in the LICENSE file.

If you find basically_ti_basic useful, use it regularly, or build something cool
around it, please consider contributing, providing feedback or simply dropping a
line to say that basically_ti_basic is useful to you. Feedback from users is
what keeps open source projects strong.

Credits
------------
Special thanks to [http://merthsoft.com/](http://merthsoft.com/) for their [TI-83+/TI-84+ Link Protocol Guide](http://merthsoft.com/linkguide/ti83+/index.html), which was a big help in writing sections of this software.
