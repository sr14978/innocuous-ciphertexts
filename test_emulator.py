#!/usr/bin/python2

description = """
Program to test that emulated ciphertexts are like the reference distrobution and is invertable
"""

import random
import argparse

import emulate
import measure

from bins import modes

def main(mode=modes['CHARACTER_DISTROBUTION']):

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
	parser = argparse.ArgumentParser(description=description)
	parser.add_argument('-m', '--mode',
		choices=modes.values(), default=modes['CHARACTER_DISTROBUTION'])
	args = vars(parser.parse_args())
	main(args["mode"])

