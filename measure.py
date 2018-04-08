#!/usr/bin/python3

import collect as col
import calculate as calc
import argparse
import os

def test(size, folder, index=None):
	
	path = size + "/" + folder + "/"

	if index == None:
		index = 1
		while os.path.exists(path + str(index)):
			index += 1

		col.main(True, path + str(index))

	with open(size + "/threshold", "r") as f:
		threshold = float(f.readline())

	val = calc.test(
		path + str(index),
		size + "/reference_bins"
	)

	return val > threshold


if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument('-s', '--size', default="100")
	parser.add_argument('-f', '--folder', default="fakes")
	parser.add_argument('-i', '--index', default=None)
	args = vars(parser.parse_args())
	result = test(args["size"], args["folder"], args["index"])
	print("Fake" if result else "Normal")
