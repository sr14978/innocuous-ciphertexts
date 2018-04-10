#!/usr/bin/python3

description = """
Program to create a distrobution historgram from a list of paths
"""

import argparse
import pickle
import random

modes = {
	'CHARACTER_DISTROBUTION':'char',
	'SLASHES_FREQUENCY':'slash',
	'INTER_SLASH_DIST':'length',
	'FIRST_LETTER':'first',
	'RANDOM_LETTER':'rand',
}

default_mode = modes['CHARACTER_DISTROBUTION']

def sort_smoothed(filename_in, mode):
	bins = sort(filename_in, mode)
	if any([i==0 for i in bins]):
		bins = [i+1 for i in bins]
	return bins

def sort(filename_in, mode=default_mode):
	if mode == modes['CHARACTER_DISTROBUTION']:

		bins = [0] * 256
		with open(filename_in, "rb") as f:
			lines = pickle.load(f)

		for line in lines:
			for chr in line:
				bins[ord(chr)] += 1
		return bins[30:130]

	elif mode == modes['SLASHES_FREQUENCY']:

		bins = [0] * 2
		with open(filename_in, "rb") as f:
			lines = pickle.load(f)

		for line in lines:
			for chr in line:
				bins[1 if chr == '/' else 0] += 1
		return bins
		
	elif mode == modes['INTER_SLASH_DIST']:

		bins = [0] * 256
		with open(filename_in, "rb") as f:
			lines = pickle.load(f)
		
		for line in lines:
			length = 0
			for chr in line:
				if chr == '/':
					bins[length] += 1
					length = 0
				else:
					length += 1

		return bins
		
	elif mode == modes['FIRST_LETTER']:

		bins = [0] * 256
		with open(filename_in, "rb") as f:
			lines = pickle.load(f)
		
		for line in lines:
			bins[ord(line[0])] += 1
		
		return bins[30:130]

	elif mode == modes['RANDOM_LETTER']:

		bins = [0] * 256
		with open(filename_in, "rb") as f:
			lines = pickle.load(f)
		
		for line in lines:
			bins[ord(line[random.randrange(len(line))])] += 1
		
		return bins[30:130]


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description=description)
	parser.add_argument('-i', '--in', default="100/reference_urls")
	parser.add_argument('-o', '--out', default="100/reference_char_bins")
	parser.add_argument('-m', '--mode',
		choices=modes.values(), default=modes['CHARACTER_DISTROBUTION'])
	parser.add_argument('-ns', '--nosmooth', action='store_true')
	args = vars(parser.parse_args())
	
	if args["nosmooth"]:
		go = sort
	else: 
		go = sort_smoothed
		
	with open(args["out"], "wb") as f:
		pickle.dump(go(args["in"], args["mode"]), f)

