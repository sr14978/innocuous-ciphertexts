
import numpy as np
from collections import deque
import random

"""construct encode and decode fuctions that emulate the `bins` character distrobution"""
def init_emulator(bins, base=10, message_length=64*8):
		
	cumlative_splits = _create_cumlative_splits(bins)
	digit_splits = _create_digit_splits(bins, base, cumlative_splits)
	base_powers = _calculate_powers_of_base(base, message_length)
			
	def encode(message):
		digits = deque()
		for mod in base_powers:
			digit = message/mod
			digits.appendleft(digit)
			message -= digit*mod
		characters = []
		for digit in digits:
			low_split, high_split = digit_splits[digit]
			value = random.randrange(low_split, high_split)
			index = _lies_at_index_range(cumlative_splits, value)
			char = chr(index + 30)	# bin offset
			characters.append(char)
		return "".join(characters)

	
	def decode(url):
		digits = deque()
		for char in url:
			index = ord(char) - 30
			value,_ = cumlative_splits[index]
			digit = _lies_at_index_range(digit_splits, value)
			digits.appendleft(digit)
		message = 0
		for digit,mod in zip(digits, base_powers):
			message += digit*mod
		return message
				
	return encode, decode

"""Calculate the boundaries of each bin in the cumlative distrobution"""
def _create_cumlative_splits(bins):
	cumlative_splits_upper_bounds = np.cumsum(bins)
	prev_bound = 0
	cumlative_splits = []
	for bound in cumlative_splits_upper_bounds:
		cumlative_splits.append((prev_bound, bound))
		prev_bound = bound
	return cumlative_splits

"""Calculate the boundaries if the distrobution is split `base` ways - adjusting for cumlative bins overflowing from one split to the next"""
def _create_digit_splits(bins, base, cumlative_splits):
	bins_total = sum(bins)	
	digit_splits_width = float(bins_total) / base
	digit_splits = []
	running_total = 0.0
	for i in range(base):
		# round lower digit_split to the max of the cumlative_splits bin in which it resides
		_,lower = cumlative_splits[_lies_at_index_range(cumlative_splits,running_total)]
		running_total += digit_splits_width
		digit_splits.append((int(lower), int(running_total)))

	# ensure the last max is rounded up
	low,_ = digit_splits[-1]
	digit_splits[-1] = low,bins_total
	
	return digit_splits

"""Precalculate the needed powers of the base - reverse order"""
def _calculate_powers_of_base(base, message_length):
	message_max = 1 << message_length
	i = 1
	base_powers = deque()
	while i < message_max:
		base_powers.appendleft(i)
		i *= base
	return list(base_powers)

"""Invert the lookup table"""
def _lies_at_index_range(dist, value):
	for i,(low,high) in enumerate(dist):
		if low <= value and value < high:
			return i
			
	raise Exception("Value %i not from distrobution: %s"%(value, dist))

