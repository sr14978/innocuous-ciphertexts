#!/usr/bin/python2

"""
You can use this program to compare visually how the url distrobutions compare.
```bash
./visualise -m <binning_mode>
eg ./visualise -m char
```
"""

import pickle
import numpy as np
import matplotlib.pyplot as plt
from itertools import repeat
from itertools import chain
import argparse

import bins

def main(mode=bins.modes['CHARACTER_DISTROBUTION']):

	def get(folder):
		for i in range(10):
			with open("100/"+folder+"/"+str(i), 'rb') as f:
				yield bins.sort(pickle.load(f), mode=mode, smoothed=False)

	with open("100/reference_"+mode+"_bins", "rb") as f:
		reference = pickle.load(f)

	fakes = get("fakes")
	normals = get("normals")

	pairs = [(fakes,'m'), (normals,'g')]
	args = list(chain(*[colour(*t) for t in pairs])) + [reference, 'k']

	plt.plot(*args)
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
