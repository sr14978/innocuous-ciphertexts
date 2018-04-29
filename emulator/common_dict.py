
import numpy as np
from collections import deque

def _create_cumlative_splits(bins):
	"""Calculate the boundaries of each bin in the cumlative distrobution"""
	prev_bound = 0
	cumlative_splits = {}
	for key,diff in sorted(bins.items()):
		new_bound = prev_bound+diff
		cumlative_splits[key] = (prev_bound, new_bound)
		prev_bound = new_bound
	return cumlative_splits

def _create_digit_splits(bins, base, cumlative_splits):
	"""Calculate the boundaries if the distrobution is split `base` ways - adjusting for cumlative bins overflowing from one split to the next"""
	bins_total = sum(bins.values())
	digit_splits_width = float(bins_total) / base
	digit_splits = []
	running_total = 0.0
	for i in range(base):
		# round lower digit_split to the max of the cumlative_splits bin in which it resides
		_,lower = cumlative_splits[_lies_at_index_range(running_total)]
		running_total += digit_splits_width
		assert lower < running_total
		digit_splits.append((lower, running_total))

	# ensure the last max is rounded up
	low,_ = digit_splits[-1]
	digit_splits[-1] = low,bins_total

	return digit_splits

def _set_dist(d):
	global dist
	global keys
	dist = d
	keys = dist.keys()
	keys.sort()

def _lies_at_index_range(value):
	"""Invert the lookup table"""
	a = 0; b = len(keys)-1;
	while a != b:
		c = (a+b)/2
		if value < dist[keys[c]][0]:
			b = c-1
		elif value > dist[keys[c]][1]:
			a = c+1
		else:
			return keys[c]
	return keys[a]
