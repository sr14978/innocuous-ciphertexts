#!/usr/bin/python2

"""
You can use the emulator program to produce url messages that emulate the reference distrobution
```bash
./run_emulator.py --out <output_filepath> --mode <binning_method>
eg ./run_emulator.py --out 100/emulated/char/1 --mode char
```
"""

import argparse
import pickle
import random

from bins import modes
from bins import default_mode

import emulator

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('-o', '--out', default="100/emulated/char/1")
	parser.add_argument('-m', '--mode',
		choices=modes.values(), default=modes['CHARACTER_DISTROBUTION'])
	parser.add_argument('-nu', '--no_use', action='store_true')
	args = vars(parser.parse_args())

	if args["no_use"]:
		emulator.init(mode=args["mode"])
	else:
		urls = emulator.get_emulations(mode=args["mode"])
		with open(args["out"], "wb") as f:
			pickle.dump(urls, f)
