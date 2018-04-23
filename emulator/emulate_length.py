
"""This is a progam for creating an invertable encoding that produces ciphertexts that look like they come from a given distrobution"""

import numpy as np
from collections import deque
import random
import conf

import common as com

def init_emulator(bins):
	"""Returns (encode, decode) functions that emulate the length distrobution defined by `bins`."""
	cumlative_splits = com._create_cumlative_splits(bins)

	def encode(messages):

		# put in to a continous stream
		data_stream = ""
		for text in messages:
			if len(text) >= 0xFFFF: raise Exception("Too long")
			data_stream += "%04X"%(len(text))
			data_stream += text

		# slice up following the distrobution
		distributed_texts = []
		while len(data_stream) > 0:
			length = conf.inv_char_calc(sample(cumlative_splits))
			if len(data_stream) >= length:
				out = data_stream[:length]
				distributed_texts.append(out)
				data_stream = data_stream[length:]
			else:
				padding_length = length-len(data_stream)
				padding = get_padding(padding_length)
				distributed_texts.append(data_stream+padding)
				data_stream = ""

		print "length encoder", messages, " => ", distributed_texts
		return distributed_texts

	def decode(data_stream):

		original_messages = []
		while len(data_stream) > 0:
			if len(data_stream) < 4:
				break
			length = int(data_stream[:4], 16)
			if length == 0xFFFF:
				data_stream = ''
				break
			if len(data_stream) < length + 4:
				break
			data_stream = data_stream[4:]
			message = data_stream[:length]
			data_stream = data_stream[length:]
			original_messages.append(message)

		print "length decoder", data_stream, " => ", original_messages
		return original_messages, data_stream

	return encode, decode

def sample(dist):
	return com._lies_at_index_range(dist, random.random())

def randchar():
	return chr(random.randrange(256))

def get_padding(padding_length):
	if padding_length >= 4:
		return "%04X"%(0xFFFF) + "".join([randchar() for _ in range(padding_length-4)])
	else:
		return "".join([randchar() for _ in range(padding_length)])
