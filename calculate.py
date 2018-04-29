#!/usr/bin/python2

"""
You can calculate the distance between given urls and a reference distrobution with this program.
```bash
./calculate.py <url_test_file> <reference_bins>
eg ./calculate.py 1000/fakes/1 1000/censor/reference_char_bins
```
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

	test = bins.sort(urls, mode, smoothed=False)

	with open(reference_file, "rb") as f:
		reference = pickle.load(f)

	# paired = zip(test, reference)
	# filtered = [(a,b) for a,b in paired if b != 0]
	# test, reference = zip(*filtered)

	# Fisher's exact test

	if type(test) == dict:
		print "one"
		assert type(reference) == dict
		for k in test:
			if k not in reference:
				reference[k] = 0
		for k in reference:
			if k not in test:
				test[k] = 0
		# smoothing
		total = sum(reference.values())
		smoothing_proportion = 1e-2
		smoothed_total = total / (1 - smoothing_proportion)
		smoothing_value = smoothing_proportion/len(reference)
		reference = {key:smoothing_value + float(value)/smoothed_total for (key,value) in reference.items()}

		test_l = []
		ref_l = []
		for key in reference.keys():
			test_l.append(test[key])
			ref_l.append(reference[key])
		test = test_l
		reference = ref_l

	v = chisquare(test, reference).statistic
	return v

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('test', default="test_urls")
	parser.add_argument('reference', default="1000/censor/reference_char_bins")
	parser.add_argument('-m', '--mode',
		choices=bins.modes.values(), default=bins.default_mode)
	args = vars(parser.parse_args())
	print(test_file(args["test"], args["reference"], args["mode"]))
