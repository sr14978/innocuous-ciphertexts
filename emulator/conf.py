
import math
from fte.encrypter import Encrypter

def inv_char_calc(output):
    return

size_of_char = 0x100
URI_length = 500
pattern_length = 48
divisions = 50
# divisions = lambda: int(0x100**((float(pattern_length)/8) * (256.0/1500)))

wrapped_length = URI_length + 18

frag_ciphertext_length = lambda: int(URI_length*math.log(divisions)/math.log(size_of_char)/(pattern_length >> 3)) -1
frag_plaintext_padded_length = lambda: frag_ciphertext_length() - Encrypter._CTXT_EXPANSION
frag_plaintext_length = lambda: frag_plaintext_padded_length() - 1 # leave at least one byte to pad
