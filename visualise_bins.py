#!/usr/bin/python2

"""
You can use this program to compare visually how the url distrobutions compare.
```bash
./visualise_bins.py -m <binning_mode>
eg ./visualise_bins.py -m char
```
"""

import pickle
import numpy as np
import matplotlib.pyplot as plt
from itertools import repeat
from itertools import chain
import argparse
from matplotlib2tikz import save as save

import bins

def main(mode=bins.modes['CHARACTER_DISTROBUTION']):

	def get(folder):
		for i in range(10):
			with open("1000/"+folder+"/"+str(i), 'rb') as f:
				yield bins.sort(pickle.load(f), mode=mode, smoothed=False)

	with open("1000/censor/reference_"+mode+"_bins", "rb") as f:
		reference = pickle.load(f)

	fakes = get("fakes")
	normals = get("normals")

	pairs = [(normals,'g'),  (fakes, 'm')]
	args = list(chain(*[colour(*t) for t in pairs])) + [reference, 'k']

	# reference = np.cumsum(reference)
	# plt.bar(range(len(reference)),reference)
	plt.plot(*args)
	plt.xlabel("Bin Number")
	plt.ylabel("Proportion")
	# save('dist_bar.tex')
	plt.show()

def interleave(a,b):
	return (x for tup in zip(a,b) for x in tup)

def colour(dist, col):
	return interleave(dist,repeat(col, 10))

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('-m', '--mode',
		choices=bins.modes.values(), default=bins.modes['CHARACTER_DISTROBUTION'])
	args = vars(parser.parse_args())
	main(args["mode"])
