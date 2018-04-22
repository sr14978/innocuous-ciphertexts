
"""This is a progam for creating an invertable encoding that produces ciphertexts that look like they come from a given distrobution"""

import numpy as np
from collections import deque
import random

import common as com

def init_emulator(bins, base=10, message_length=256):
	"""Returns (encode, decode) functions that emulate the character distrobution defined by `bins`."""
	message_max = (message_length+1)*8
	cumlative_splits = com._create_cumlative_splits(bins)
	digit_splits = com._create_digit_splits(bins, base, cumlative_splits)
	base_powers = com._calculate_powers_of_base(base, message_max)

	def encode(message):
		message = '\xFF'+message
		input_value = 0
		for char in message:
			input_value <<= 8
			input_value += ord(char)
		if input_value > (1<<message_max):
			raise Exception("Message too long")
		digits = deque()
		for mod in base_powers:
			digit = input_value/mod
			digits.appendleft(digit)
			input_value -= digit*mod
		characters = []
		for digit in digits:
			low_split, high_split = digit_splits[digit]
			value = low_split + random.random()*(high_split-low_split)
			index = com._lies_at_index_range(cumlative_splits, value)
			char = chr(index + 30)	# bin offset
			characters.append(char)

		print "encoding", message, ':'.join(x.encode('hex') for x in message) , "".join(characters)[:10], "..."
		return "".join(characters)


	def decode(url):
		digits = deque()
		for char in url:
			index = ord(char) - 30
			value,_ = cumlative_splits[index]
			digit = com._lies_at_index_range(digit_splits, value)
			digits.appendleft(digit)
		output_value = 0
		for digit,mod in zip(digits, base_powers):
			output_value += digit*mod
		message = deque()
		while output_value != 0xFF:
			message.appendleft(chr(output_value & 0xFF))
			output_value >>= 8
		# while len(message) < message_length:
		# 	message.appendleft('\x00')

		print "decoding", url[:10], "...", "".join(message), ':'.join(x.encode('hex') for x in message)
		return "".join(message)

	return encode, decode
