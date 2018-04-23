#!/usr/bin/python2

"""
Program to run all functions with default paths. -c enables collecting all new packets. -g displays the graphs as it goes along. -e enables emulation calculations.
```bash
./run_all.py -c -g -e
```
"""

import argparse, pickle
import collect, bins, find_threshold, emulator

def main(collect_new, enable_graphs, enable_emulations):

	if collect_new:
		print "Press enter to collect reference urls"
		raw_input()
		collect.main('1000/censor/reference_urls')

		print "Press enter to collect fakes."
		raw_input()
		for i in range(10):
			collect.main('1000/fakes/'+str(i))

		print "Press enter to collect normal packets."
		raw_input()
		for i in range(10):
			collect.main('1000/normals/'+str(i))

	for mode in bins.modes.values():
		print "Creating " + mode + " histogram."
		hist = bins.sort_file("1000/censor/reference_urls", mode)
		with open("1000/censor/reference_" + mode + "_bins", 'wb') as f:
			print str(hist)[:100], "...", str(hist)[-100:]
			pickle.dump(hist, f)

	for mode in bins.modes.values():
		print "Calculating " + mode + " threshold"
		results = find_threshold.calculate(mode=mode, enable_graphs=enable_graphs)
		with open("1000/censor/threshold_" + mode, "w") as f:
			print str(results)
			f.write(str(results))

	if enable_emulations:
		for mode in bins.modes.values():
			if mode != bins.modes["INTER_SLASH_DIST"]:
				print "Testing emulation in " + mode + " mode."
				emulator.test(mode)

		for mode in bins.modes.values():
			if mode != bins.modes["INTER_SLASH_DIST"]:
				print "Emulating example ciphertexts in " + mode + " mode."
				for i in range(10):
					urls = emulator.get_emulations(mode=mode)
					with open("1000/emulated/" + mode + "/" + str(i), "wb") as f:
						pickle.dump(urls, f)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('-c', '--collect_new', action='store_true')
	parser.add_argument('-e', '--enable_emulations', action='store_true')
	parser.add_argument('-g', '--enable_graphs', action='store_true')
	args = vars(parser.parse_args())
	main(args["collect_new"], args["enable_graphs"], args["enable_emulations"])
