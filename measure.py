#!/usr/bin/python2

description = """
Program to collect a list of paths from clear http requests and calculate the distance to reference distrobution.
"""

import collect as col
import calculate as calc
import bins
import argparse
import os
import pickle

def test(size, folder, index=None, mode=bins.default_mode):
	
	path = size + "/" + folder + "/"

	if index == None:
		index = 1
		while os.path.exists(path + str(index)):
			index += 1

		col.main(True, path + str(index))

	with open(path + str(index), "rb") as f:
		urls = pickle.load(f)

	return test_raw(urls, size, mode)

def test_raw(urls, size, mode=bins.default_mode):
	with open(size + "/threshold_" + mode, "r") as f:
		threshold = float(f.readline())
		
	val = calc.test(
		urls,
		size + "/reference_" + mode + "_bins",
		mode
	)
	
	return val > threshold

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description=description)
	parser.add_argument('-s', '--size', default="100")
	parser.add_argument('-f', '--folder', default="fakes")
	parser.add_argument('-i', '--index', default=None)
	parser.add_argument('-m', '--mode',
		choices=bins.modes.values(), default=bins.default_mode)
	args = vars(parser.parse_args())
	
	result = test(args["size"], args["folder"], args["index"])
	print("Fake" if result else "Normal")
