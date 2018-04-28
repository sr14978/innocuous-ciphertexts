
"""This is a progam for creating an invertable encoding that produces ciphertexts that look like they come from a given distrobution"""

import numpy as np
from collections import deque
import random
import itertools

import common as com
import common_dict as comd

def init_emulator(bins, base=100, message_length=256, pattern_length=32):
	"""Returns (encode, decode) functions that emulate the character distrobution defined by `bins`."""
	message_max = (message_length+1)*8
	cumlative_splits = comd._create_cumlative_splits(bins)
	comd._set_dist(cumlative_splits)
	digit_splits = comd._create_digit_splits(bins, base, cumlative_splits)
	base_powers = com._calculate_powers_of_base(base, message_max)
	pattern_length_rng = range(pattern_length)
	def encode(message):
		message = '\xFF'+message
		input_value = 0
		for char in message:
			input_value = (input_value << 8) | ord(char)
		if input_value > (1<<message_max):
			raise Exception("Message too long")
		digits = deque()
		non_zero_digit_not_found = True
		for mod in base_powers:
			digit = input_value/mod
			if non_zero_digit_not_found:
				if digit == 0:
					continue
				else:
					non_zero_digit_not_found = False
			digits.appendleft(digit)
			input_value -= digit*mod
		bit_stream = [0] * (pattern_length * len(digits))
		i = 0
		for digit in digits:
			low_split, high_split = digit_splits[digit]
			value = low_split + random.random()*(high_split-low_split)
			index = comd._lies_at_index_range(value)
			value = index
			# value = index + int(0.2e7)	# bin offset
			# value = (index + 30)	# bin offset
			for j in pattern_length_rng:
				bit_stream[i] = ((value>>j)&1)
				i += 1
		return "".join(chr(evaluate8(chunk)) for chunk in group(bit_stream, 8))

	def group(xs, n): return itertools.izip(*(itertools.islice(xs, i, None, n) for i in xrange(n)))

	def evaluate8(bits):
		a, b, c, d, e, f, g, h = bits
		return (h << 7 | g << 6 | f << 5 | e << 4 | d << 3 | c << 2 | b << 1 | a)

	def evaluate(bits):
			sum = 0
			for bit in reversed(bits): sum = (sum << 1) | bit
			return sum

	def to_char_bits(value):
		return [(value>>i)&1 for i in xrange(8)]


	def decode(url):

		bit_stream = [b for c in url for b in to_char_bits(ord(c))]
		digits = [evaluate(chunk) for chunk in group(bit_stream, pattern_length)]
		l = len(digits)
		i = 0
		while i < l:
			# digits[i] = com._lies_at_index_range(digit_splits, cumlative_splits[digits[i] - 30][0])
			digits[i] = com._lies_at_index_range(digit_splits, cumlative_splits[digits[i]][0])
			i+=1
		output_value = 0
		for digit,mod in zip(digits, base_powers[::-1]):
			output_value += digit*mod
		message = deque()
		while output_value != 0xFF:
			message.appendleft(chr(output_value & 0xFF))
			output_value >>= 8
		return "".join(message)

	return encode, decode
