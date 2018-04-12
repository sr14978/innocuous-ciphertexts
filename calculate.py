#!/usr/bin/python2

description = """
Program to calculate the distance between a test distrobution and a reference distrobution.
"""

from scipy.stats import chisquare
import argparse
import pickle
import bins

def test_file(test_file, reference_file, mode=bins.default_mode):
	with open(test_file, "rb") as f:
		urls = pickle.load(f)
	
	return test(urls, reference_file, mode)

def test(urls, reference_file, mode=bins.default_mode):

	test = bins.sort(urls, mode)

	with open(reference_file, "rb") as f:
		reference = pickle.load(f)

	# paired = zip(test, reference)
	# filtered = [(a,b) for a,b in paired if b != 0]
	# test, reference = zip(*filtered)
	
	# Fisher's exact test
	
	v = chisquare(test, reference).statistic
	return v

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description=description)
	parser.add_argument('test', default="test_urls")
	parser.add_argument('reference', default="100/reference_bins")
	parser.add_argument('-m', '--mode',
		choices=bins.modes.values(), default=bins.default_mode)
	args = vars(parser.parse_args())
	print(test_file(args["test"], args["reference"]))
