#!/usr/bin/python2

"""
A distrobution historgram of the urls can be computed with this bin program. You can choose one of the following methods:
  - CHARACTER_DISTROBUTION:'char'
  - SLASHES_FREQUENCY:'slash'
  - INTER_SLASH_DIST:'length'
  - FIRST_LETTER:'first'
  - RANDOM_LETTER:'rand'

./bins.py --in 100/reference_urls --out 100/reference_<method>_bins --mode <method>
eg ./bins.py --in 100/reference_urls --out 100/reference_char_bins --mode char
"""

import argparse
import pickle
import random

modes = {
	'CHARACTER_DISTROBUTION':'char',
	'SLASHES_FREQUENCY':'slash',
	'INTER_SLASH_DIST':'dist',
	'FIRST_LETTER':'first',
	'RANDOM_LETTER':'rand',
    'URL_LENGTH':'length'
}

default_mode = modes['CHARACTER_DISTROBUTION']

def sort_file(filename_in, mode, smoothed=True):
	"""calculates freuqency bins from urls in `filename`"""
	with open(filename_in, "rb") as f:
		urls = pickle.load(f)

	return sort(urls, mode, smoothed)

def sort(urls, mode=default_mode, smoothed=True):
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

		bins = [0] * 2000
		for url in urls:
			if len(url) < 2000:
				bins[len(url)] += 1

	if smoothed:
		if any([i==0 for i in bins]):
			bins = [i+1 for i in bins]

	return bins

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('-i', '--in', default="100/reference_urls")
	parser.add_argument('-o', '--out')
	parser.add_argument('-m', '--mode',
		choices=modes.values(), default=modes['CHARACTER_DISTROBUTION'])
	parser.add_argument('-ns', '--nosmooth', action='store_true')
	args = vars(parser.parse_args())

	bins = sort_file(args["in"], args["mode"], not args["nosmooth"])
	if args["out"] == None:
		print bins
	else:
		with open(args["out"], "wb") as f:
			pickle.dump(bins, f)
