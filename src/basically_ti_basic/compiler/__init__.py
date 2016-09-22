from basically_ti_basic.tokens import get_tokens, get_inverse_tokens
from basically_ti_basic.files import TIPrgmFile

class PrgmCompiler(object):

    """
    Handles compilation and decompilation of TIBasic .8Xp
    program files
    """

    def compile(self, raw_text=None):
        """
        Compiles to 8Xp format. This logic works, but the TIFile class is
        incomplete so the file may not work properly on the TI calculator.

        Parameters:
            Array[string]
        Returns:
            TIFile
        """
        # To be compatible with Python 2.7 without changing
        # the public class API, we do some gross magic. This
        # has a side effect that we can use this method either
        # as a static method or not.
        # FIXME
        if not isinstance(self, PrgmCompiler):
            raw_text = self

        tifile = TIPrgmFile()
        tifile.prgmdata = []
        tokens = get_inverse_tokens()
        prgm_string = "".join(raw_text)
        longest_prgm_string = max(len(k) for k in tokens.keys())

        current_char = 0
        while current_char < len(prgm_string):
            found = False
            chars_further = longest_prgm_string
            # Greedily start with the maximum size string we have and back
            # down until we get to something that we can create a token from.
            while not found and chars_further > 0:
                try:
                    token = tokens[prgm_string[current_char:current_char+chars_further]]
                    found = True
                    tifile.prgmdata.append(token)
                    current_char += chars_further
                except:
                    chars_further -= 1

                if chars_further <= 0:
                    raise Exception("Something went horribly wrong while compiling.")

        return tifile


    def decompile(self, tifile=None):
        """
        Decompiles to plaintext.

        Parameters:
            TIFile tifile: An open ti file to decompile
        Returns:
            Array[string]
        """

        # To be compatible with Python 2.7 without changing
        # the public class API, we do some gross magic. This
        # has a side effect that we can use this method either
        # as a static method or not.
        # FIXME
        if not isinstance(self, PrgmCompiler):
            tifile = self

        prgm_data = tifile.prgmdata
        plaintext = []
        tokens = get_tokens()

        byte_num = 0
        # Iterate until we hit the end of the program data
        while byte_num < len(prgm_data):

            curr_byte = prgm_data[byte_num]
            found_plaintext = ''

            # If the current byte exists in the tokens, see if we
            # can find a more specific one (2 bytes) that matches. If not, use
            # the first. We only need to worry about up to 2 bytes.
            if curr_byte in tokens.keys():
                try:
                    found_plaintext = tokens[curr_byte + prgm_data[byte_num+1]]
                    byte_num += 2
                except:
                    found_plaintext = tokens[curr_byte]
                    byte_num += 1

                plaintext.append(found_plaintext)
                continue

            # If the current byte is not in the tokens, see if we can add
            # on the next byte to make it work. If so, use that, otherwise
            # spit out an error but do the rest.
            if curr_byte not in tokens.keys():
                try:
                    found_plaintext = tokens[curr_byte + prgm_data[byte_num+1]]
                    plaintext.append(found_plaintext)
                    byte_num += 2
                except:
                    print("Could not decode " + str(curr_byte))
                    byte_num += 1

        return "".join(plaintext).split("\n")
