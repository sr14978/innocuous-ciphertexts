#!/usr/bin/python3

import argparse
import pickle

def sort(filename_in):

	bins = [0] * 256

	with open(filename_in, "rb") as f:
		lines = pickle.load(f)

	for line in lines:
		for chr in line:
			bins[ord(chr)] += 1

	return bins	

if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--in', default="reference_urls")
	parser.add_argument('-o', '--out', default="reference_bins")
	args = vars(parser.parse_args())

	with open(args["out"], "wb") as f:
		pickle.dump(sort(args["in"]), f)
	
