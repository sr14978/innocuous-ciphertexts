#!/usr/bin/python3

import argparse
import pickle

def go():

	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--in', default="reference_urls")
	parser.add_argument('-o', '--out', default="reference_bins")
	args = vars(parser.parse_args())

	bins = [0] * 256

	with open(args["in"] , "rb") as f:
		lines = pickle.load(f)

	for line in lines:
		for chr in line:
			bins[ord(chr)] += 1

	print(bins)

	with open(args["out"] , "wb") as f:
		pickle.dump(bins, f)

if __name__ == "__main__":
	print(go())
