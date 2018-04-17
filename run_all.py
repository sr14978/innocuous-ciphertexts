#!/usr/bin/python2

"""
Program to run all function with default paths
"""

import argparse, pickle
import collect, bins, find_threshold, emulator

def main(collect_new_flag):

	if collect_new_flag:
		print "Press enter to collect fakes."
		raw_input()
		for i in range(10):
			collect.main('100/fakes/'+str(i), size=100)

		print "Press enter to collect normal packets."
		raw_input()
		for i in range(10):
			collect.main('100/normals/'+str(i), size=100)

	for mode in bins.modes.values():
		print "Creating " + mode + " histogram."
		hist = bins.sort_file("100/reference_urls", mode)
		with open("100/reference_" + mode + "_bins", 'wb') as f:
			pickle.dump(hist, f)

	for mode in bins.modes.values():
		print "Calculating " + mode + " threshold"
		results = find_threshold.calculate(mode=mode)
		with open("100/threshold_" + mode, "w") as f:
			f.write(str(results))

	for mode in bins.modes.values():
		print "Emulating ciphertexts in " + mode + " mode."
		emulator.test(mode)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('-c', '--collect_new', action='store_true')
	args = vars(parser.parse_args())
	main(args["collect_new"])
