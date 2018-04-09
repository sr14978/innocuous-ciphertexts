#!/usr/bin/python3

from scipy.stats import chisquare
import argparse
import pickle
import bins

def test(test_file, reference_file):

	test = bins.sort(test_file)

	with open(reference_file, "rb") as f:
		reference = pickle.load(f)

	paired = zip(test, reference)
	filtered = [(a,b) for a,b in paired if b != 0]
	test, reference = zip(*filtered)

	return chisquare(test, reference).statistic

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('test', default="test_urls")
	parser.add_argument('reference', default="100/reference_bins")
	args = vars(parser.parse_args())
	print(test(args["test"], args["reference"]))
