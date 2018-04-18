#!/usr/bin/python2

"""
A distrobution historgram of the urls can be computed with this bin program. You can choose one of the following methods:
  - CHARACTER_DISTROBUTION:'char'
  - SLASHES_FREQUENCY:'slash'
  - INTER_SLASH_DIST:'length'
  - FIRST_LETTER:'first'
  - RANDOM_LETTER:'rand'

```bash
./bins.py --in 100/reference_urls --out 100/reference_<method>_bins --mode <method>
eg ./bins.py --in 100/reference_urls --out 100/reference_char_bins --mode char
```
"""

import argparse
import pickle
import random
import numpy as np
import matplotlib.pyplot as plt

modes = {
	'CHARACTER_DISTROBUTION':'char',
	'SLASHES_FREQUENCY':'slash',
	'INTER_SLASH_DIST':'dist',
	'FIRST_LETTER':'first',
	'RANDOM_LETTER':'rand',
    'URL_LENGTH':'length'
}

default_mode = modes['CHARACTER_DISTROBUTION']

def sort_file(filename_in, mode, smoothed=True, graph=False):
	"""calculates freuqency bins from urls in `filename`"""
	with open(filename_in, "rb") as f:
		urls = pickle.load(f)

	return sort(urls, mode, smoothed, graph)

def sort(urls, mode=default_mode, smoothed=True, graph=False):
	"""calculates freuqency bins from `urls`"""
	if mode == modes['CHARACTER_DISTROBUTION']:

		bins = [0] * 256
		for url in urls:
			for chr in url:
				bins[ord(chr)] += 1
		bins = bins[30:130]

	elif mode == modes['SLASHES_FREQUENCY']:

		bins = [0] * 2
		for url in urls:
			for chr in url:
				bins[1 if chr == '/' else 0] += 1

	elif mode == modes['INTER_SLASH_DIST']:

		bins = [0] * 100
		for url in urls:
			length = 0
			for chr in url:
				if chr == '/':
					if length < len(bins):
						bins[length] += 1
					length = 0
				else:
					length += 1

	elif mode == modes['FIRST_LETTER']:

		bins = [0] * 256
		for url in urls:
			bins[ord(url[0])] += 1

		bins = bins[30:130]

	elif mode == modes['RANDOM_LETTER']:

		bins = [0] * 256
		for url in urls:
			bins[ord(url[random.randrange(len(url))])] += 1

		bins = bins[30:130]

	elif mode == modes['URL_LENGTH']:

		bins = [0] * 500
		for url in urls:
			if len(url) < 500: # ignore the old outliers
				bins[len(url)] += 1

	total = sum(bins)

	if smoothed and any([i==0 for i in bins]):
		smoothing_proportion = 1e-2
		smoothed_total = total / (1 - smoothing_proportion)
		smoothing_value = smoothing_proportion/len(bins)
		bins = [smoothing_value + float(i)/smoothed_total for i in bins]
	else:
		bins = [float(i)/total for i in bins]

	if graph:
		plt.plot(np.cumsum(bins))
		plt.show()

	return bins


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('-i', '--in', default="100/reference_urls")
	parser.add_argument('-o', '--out')
	parser.add_argument('-m', '--mode',
		choices=modes.values(), default=modes['CHARACTER_DISTROBUTION'])
	parser.add_argument('-ns', '--nosmooth', action='store_true')
	parser.add_argument('-g', '--graph', action='store_true')
	args = vars(parser.parse_args())

	bins = sort_file(args["in"], args["mode"], not args["nosmooth"], args["graph"])
	if args["out"] == None:
		print bins
	else:
		with open(args["out"], "wb") as f:
			pickle.dump(bins, f)
