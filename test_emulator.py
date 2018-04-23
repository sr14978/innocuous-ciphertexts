#!/usr/bin/python2

"""
You can test that the emulated ciphertexts are like the adversary reference distrobution  and is that the encoding invertable using this program.
```bash
./test_emulator.py --mode <binning_method>
eg ./test_emulator.py --mode char
```
"""

import argparse
import random
from Crypto import Random

import emulator
import measure

from bins import modes

def test(mode=modes['CHARACTER_DISTROBUTION']):

	size = 1000

	if mode == modes['URL_LENGTH']:
		message_length = 238
		encode,decode = emulator.init(mode=mode)
		def randchar():
			return chr(random.randrange(33, 127))
		messages = ["".join([randchar() for _ in range(message_length)]) for _ in range(size)]
		urls = encode(messages)
		message_decodings = decode(urls)

	else:
		message_length = 238
		Random.get_random_bytes(5)
		messages = [Random.get_random_bytes(message_length) for _ in range(size)]

		encode,decode = emulator.init(mode=modes['CHARACTER_DISTROBUTION'], message_length=message_length)

		urls = [encode(m) for m in messages]
		message_decodings = [decode(u) for u in urls]

	is_inverted_correctly = all([a==b for a,b in zip(messages, message_decodings)])
	print("Invertable" if is_inverted_correctly else "Not Invertable")

	result = measure.test_raw(urls, size, mode=mode)
	print("Fake" if result else "Normal")


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('-m', '--mode',
		choices=modes.values(), default=modes['CHARACTER_DISTROBUTION'])
	args = vars(parser.parse_args())
	test(args["mode"])
