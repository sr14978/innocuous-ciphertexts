
"""This is a progam for creating an invertable encoding that produces ciphertexts that look like they come from a given distrobution"""

import numpy as np
from collections import deque
import random

import common as com

def init_emulator(bins, base=10, message_length=64*8):
	"""Returns (encode, decode) functions that emulate the character distrobution defined by `bins`."""
	cumlative_splits = com._create_cumlative_splits(bins)
	digit_splits = com._create_digit_splits(bins, base, cumlative_splits)
	base_powers = com._calculate_powers_of_base(base, message_length)

	def encode(message):
		digits = deque()
		for mod in base_powers:
			digit = message/mod
			digits.appendleft(digit)
			message -= digit*mod
		characters = []
		for digit in digits:
			low_split, high_split = digit_splits[digit]
			value = low_split + random.random()*(high_split-low_split)
			index = com._lies_at_index_range(cumlative_splits, value)
			char = chr(index + 30)	# bin offset
			characters.append(char)
		return "".join(characters)


	def decode(url):
		digits = deque()
		for char in url:
			index = ord(char) - 30
			value,_ = cumlative_splits[index]
			digit = com._lies_at_index_range(digit_splits, value)
			digits.appendleft(digit)
		message = 0
		for digit,mod in zip(digits, base_powers):
			message += digit*mod
		return message

	return encode, decode
