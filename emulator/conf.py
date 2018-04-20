
import math
from fte.encrypter import Encrypter

size_of_char = 0x100
divisions = 10
URI_length = 256

wrapped_length = URI_length + 18

frag_ciphertext_length = int(URI_length*math.log(divisions)/math.log(size_of_char)) -1
frag_plaintext_padded_length = frag_ciphertext_length - Encrypter._CTXT_EXPANSION
frag_plaintext_length = frag_plaintext_padded_length - 1 # leave at least one byte to pad
