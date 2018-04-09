#!/usr/bin/python3

import argparse
import pickle

modes = {
	'CHARACTER_DISTROBUTION':'char',
	'SLASHES_FREQUENCY':'slash'
}

def sort(filename_in, mode=modes['CHARACTER_DISTROBUTION']):

	if mode == modes['CHARACTER_DISTROBUTION']:

		bins = [0] * 256
		with open(filename_in, "rb") as f:
			lines = pickle.load(f)

		for line in lines:
			for chr in line:
				bins[ord(chr)] += 1
		return bins

	elif mode == modes['SLASHES_FREQUENCY']:

		bins = [0] * 2
		with open(filename_in, "rb") as f:
			lines = pickle.load(f)

		for line in lines:
			for chr in line:
				bins[1 if chr == '/' else 0] += 1
		return bins

if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--in', default="reference_urls")
	parser.add_argument('-o', '--out', default="reference_bins")
	parser.add_argument('-m', '--mode',
		choices=modes.values(), default=modes['CHARACTER_DISTROBUTION'])
	args = vars(parser.parse_args())

	with open(args["out"], "wb") as f:
		pickle.dump(sort(args["in"], args["mode"]), f)

