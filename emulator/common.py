
import numpy as np
from collections import deque

def _create_cumlative_splits(bins):
	"""Calculate the boundaries of each bin in the cumlative distrobution"""
	cumlative_splits_upper_bounds = np.cumsum(bins)
	prev_bound = 0
	cumlative_splits = []
	for bound in cumlative_splits_upper_bounds:
		cumlative_splits.append((prev_bound, bound))
		prev_bound = bound
	return cumlative_splits


def _create_digit_splits(bins, base, cumlative_splits):
	"""Calculate the boundaries if the distrobution is split `base` ways - adjusting for cumlative bins overflowing from one split to the next"""
	bins_total = sum(bins)
	digit_splits_width = float(bins_total) / base
	digit_splits = []
	running_total = 0.0
	for i in range(base):
		# round lower digit_split to the max of the cumlative_splits bin in which it resides
		_,lower = cumlative_splits[_lies_at_index_range(cumlative_splits,running_total)]
		running_total += digit_splits_width
		digit_splits.append((lower, running_total))

	# ensure the last max is rounded up
	low,_ = digit_splits[-1]
	digit_splits[-1] = low,bins_total

	return digit_splits

def _calculate_powers_of_base(base, message_length):
	"""Precalculate the needed powers of the base - reverse order"""
	message_max = 1 << message_length
	i = 1
	base_powers = deque()
	while i < message_max:
		base_powers.appendleft(i)
		i *= base
	return list(base_powers)


def _lies_at_index_range(dist, value):
	"""Invert the lookup table"""
	for i,(low,high) in enumerate(dist):
		if low <= value and value < high:
			return i

	raise Exception("Value %i not from distrobution: %s"%(value, dist))
