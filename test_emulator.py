#!/usr/bin/python2

"""
You can test that the emulated ciphertexts are like the reference distrobution  and is that the encoding invertable using this program.
./test_emulator.py --mode <binning_method>
eg ./test_emulator.py --mode char
"""

import argparse

import emulator
from bins import modes

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('-m', '--mode',
		choices=modes.values(), default=modes['CHARACTER_DISTROBUTION'])
	args = vars(parser.parse_args())
	emulator.test(args["mode"])
