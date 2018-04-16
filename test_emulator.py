#!/usr/bin/python2

"""
You can test that the emulated ciphertexts are like the reference distrobution  and is that the encoding invertable using this program.
./test_emulator.py --mode <binning_method>
eg ./test_emulator.py --mode char
"""

import random
import argparse

import emulate
import measure

from bins import modes

def test(mode=modes['CHARACTER_DISTROBUTION']):

	size = 100
	message_length = 256*8
	messages = [random.getrandbits(message_length) for _ in range(size)]

	encode,decode = emulate.init_emulator(mode=mode, message_length=message_length)

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
