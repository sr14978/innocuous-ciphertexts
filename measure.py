#!/usr/bin/python2

"""
You can use the measure program to decide if urls are fake or normal. Leaving off the index will collect new urls using the collect program
./measure.py --size <number_of_urls> --folder <folder> --index <#> --mode <binning_method>
eg ./measure.py --size 100 --folder fakes --index 1 --mode char
"""

import collect as col
import calculate as calc
import bins
import argparse
import os
import pickle

def test(size, folder, index=None, mode=bins.default_mode):
	"""Compares url's distance to the reference distrobtion with the threshold. If index is specified existing urls are used if not new requests are recorded.q"""
	path = size + "/" + folder + "/"

	if index == None:
		index = 1
		while os.path.exists(path + str(index)):
			index += 1

		col.main(path + str(index), size=size)

	with open(path + str(index), "rb") as f:
		urls = pickle.load(f)

	return test_raw(urls, size, mode)

def test_raw(urls, size=100, mode=bins.default_mode):
	"""Compares the given url's distance to the reference distrobtion with the threshold."""
	with open(str(size) + "/threshold_" + mode, "r") as f:
		threshold = float(f.readline())

	val = calc.test(
		urls,
		str(size) + "/reference_" + mode + "_bins",
		mode
	)

	return val > threshold

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('-s', '--size', default="100")
	parser.add_argument('-f', '--folder', default="fakes")
	parser.add_argument('-i', '--index', default=None)
	parser.add_argument('-m', '--mode',
		choices=bins.modes.values(), default=bins.default_mode)
	args = vars(parser.parse_args())

	result = test(args["size"], args["folder"], args["index"])
	print("Fake" if result else "Normal")
