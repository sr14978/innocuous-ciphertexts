#!/usr/bin/python2

"""
Program to test that the emulated ciphertexts are like the reference distrobution  and is that the encoding invertable using this program.
"""

import random

import emulate
import measure

from bins import modes

def test(mode=modes['CHARACTER_DISTROBUTION']):

	size = 100

	if mode == modes['URL_LENGTH']:
		message_length = 238
		encode,decode = emulate.init_emulator(mode=mode)
		def randchar():
			return chr(random.randrange(33, 127))
		messages = ["".join([randchar() for _ in range(message_length)]) for _ in range(size)]
		urls = encode(messages)
		message_decodings = decode(urls)
		
	else:
		message_length = 256*8
		messages = [random.getrandbits(message_length) for _ in range(size)]

		encode,decode = emulate.init_emulator(mode=modes['CHARACTER_DISTROBUTION'], message_length=message_length)

		urls = [encode(m) for m in messages]
		message_decodings = [decode(u) for u in urls]

	is_inverted_correctly = all([a==b for a,b in zip(messages, message_decodings)])
	print("Invertable" if is_inverted_correctly else "Not Invertable")

	result = measure.test_raw(urls, size, mode=mode)
	print("Fake" if result else "Normal")
