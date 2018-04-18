
import argparse
import pickle

import random

from bins import modes
from bins import default_mode


def get_emulations(messages=None, number=1000, mode=modes['CHARACTER_DISTROBUTION'], reference_file=None):
	"""Produce example encodings"""

	if mode == modes['URL_LENGTH']:
		message_length = 238
		encode,decode = init_emulator(mode=mode)
		def randchar():
			return chr(random.randrange(33, 127))

		if messages == None:
			messages = ["".join([randchar() for _ in range(message_length)]) for _ in range(number)]
		return encode(messages)

	else:
		message_length = 238*8
		encode,decode = init_emulator(mode=modes['CHARACTER_DISTROBUTION'], message_length=message_length)

		if messages == None:
			messages = [random.getrandbits(message_length) for _ in range(number)]
		return [encode(m) for m in messages]

def init_emulator(mode=modes['CHARACTER_DISTROBUTION'], message_length=64*8, reference_file=None):
	"""construct encode and decode fuctions that emulate the `bins` distrobution"""
	if reference_file == None:
		reference_file = "1000/reference_" + mode + "_bins"

	with open(reference_file, "rb") as f:
		bins = pickle.load(f)

	if mode == modes['CHARACTER_DISTROBUTION'] or mode == modes['INTER_SLASH_DIST'] or mode == modes['FIRST_LETTER'] or mode == modes['RANDOM_LETTER']:

		# base = number of distrobution divisions
		base = 10
		import emulate_char
		return emulate_char.init_emulator(bins, base, message_length)

	elif mode == modes['URL_LENGTH']:
		import emulate_length
		return emulate_length.init_emulator(bins)

	else:
		print "mode not supported"


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('-o', '--out', default="1000/emulated/char/1")
	parser.add_argument('-m', '--mode',
		choices=modes.values(), default=modes['CHARACTER_DISTROBUTION'])
	parser.add_argument('-nu', '--no_use', action='store_true')
	args = vars(parser.parse_args())

	if args["no_use"]:
		init_emulator(mode=args["mode"])
	else:
		urls = get_emulations(mode=args["mode"])
		with open(args["out"], "wb") as f:
			pickle.dump(urls, f)
