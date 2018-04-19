
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

def get_emulations(messages=None, number=1000, mode=modes['CHARACTER_DISTROBUTION'], reference_file=None):
	"""Produce example encodings"""

	if mode == modes['URL_LENGTH']:
		message_length = 238
		encode,_ = init_emulator(mode=mode)
		def randchar():
			return chr(random.randrange(33, 127))

		if messages == None:
			messages = ["".join([randchar() for _ in range(message_length)]) for _ in range(number)]
		return encode(messages)

	else:
		message_length = 238*8
		encode,_ = init_emulator(mode=modes['CHARACTER_DISTROBUTION'], message_length=message_length)

		if messages == None:
			messages = [random.getrandbits(message_length) for _ in range(number)]
		return [encode(m) for m in messages]

def init_emulator(mode=modes['CHARACTER_DISTROBUTION'], message_length=64*8, reference_file=None, just_URI=True, key_enc=None, key_mac=None):
	"""construct encode and decode fuctions that emulate the `bins` distrobution"""
	if reference_file == None:
		import os.path as path
		dir_path = path.abspath(path.join(__file__ ,"../.."))
		reference_file = dir_path + "/1000/reference_" + mode + "_bins"

	with open(reference_file, "rb") as f:
		bins = pickle.load(f)

	if mode == modes['CHARACTER_DISTROBUTION'] or mode == modes['INTER_SLASH_DIST'] or mode == modes['FIRST_LETTER'] or mode == modes['RANDOM_LETTER']:

		# base = number of distrobution divisions
		base = 10
		import emulate_char
		enc,dec = emulate_char.init_emulator(bins, base, message_length)

	elif mode == modes['URL_LENGTH']:
		import emulate_length
		enc,dec = emulate_length.init_emulator(bins)

		if key_enc != None and key_mac != None:
			encrypter = encrypter.Encrypter(key_enc=key_enc, key_mac=key_mac)
			enc = lambda message: enc(encrypter.encrypt(message))
			dec = lambda message: encrypter.decrypt(dec(message))

	else:
		raise Exception("mode not supported")

	if just_URI:
		return enc, dec
	else:
		return encoder(enc), decoder(dec)

class encoder:
	def __init__(self, encode):
		self._encode = encode

	def encode(self, data):
		return "GET /" + self._encode(data) + " HTTP/1.1\r\n\r\n"

class decoder:
	def __init__(self, decode):
		self._decode = decode

	def decode(self, buffer):
		index = buffer.find("HTTP/1.1\r\n\r\n")
		if index == -1:
			return '', buffer
		else:
			packet = buffer[:index+12]
			buffer = buffer[index+12:]
			msg = self._decode(packet[5:-13])
			return msg, buffer
