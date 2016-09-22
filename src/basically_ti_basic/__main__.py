from basically_ti_basic.compiler import PrgmCompiler
from basically_ti_basic.files import TIPrgmFile
import argparse

def compile_file(inputfile, outputfile):

    file_lines = []
    with open(inputfile, 'r') as f:
        for line in f:
            file_lines.append(line)

    compiler = PrgmCompiler()
    compiled_file = compiler.compile(file_lines)
    if outputfile == "stdout":
        print("".join(compiled_file.prgmdata))
    else:
        compiled_file.writeOut(outputfile)

def decompile_file(inputfile, outputfile):
    tifile = TIPrgmFile(inputfile)

    compiler = PrgmCompiler()
    decompiled = compiler.decompile(tifile)
    if outputfile == 'stdout':
        print("\n".join(decompiled))
    else:
        with open(outputfile, 'w') as out:
            for line in decompiled:
                out.write(line+"\n")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d',
        required=False,
        action="store_true",
        default=False,
        help="Decompile the passed file."
        )
    parser.add_argument(
        '-c',
        required=False,
        action="store_true",
        default=False,
        help="Compile the passed file."
        )
    parser.add_argument(
        '-o',
        required=False,
        default='stdout',
        help="Optional output file to write to. Defaults to standard out."
        )
    parser.add_argument(
        '-i',
        required=True,
        help="Input file."
        )

    args = parser.parse_args()

    if args.c:
        compile_file(args.i, args.o)

    elif args.d:
        decompile_file(args.i, args.o)

if __name__ == "__main__":
    main()
