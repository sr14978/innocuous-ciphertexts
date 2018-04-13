#!/usr/bin/python2

description = """
Program produce ciphertexts that enumale the normal distrobutions
"""

import argparse
import pickle
import random
from collections import deque

import matplotlib.pyplot as plt

from bins import modes
from bins import default_mode

def main(mode=modes['CHARACTER_DISTROBUTION']):
	
	if mode == modes['CHARACTER_DISTROBUTION']:
		
		with open("100/reference_" + mode + "_bins", "rb") as f:
			bins = pickle.load(f)
			
		# bins = [0 if b == 1 else b for b in bins]
		bins_total = sum(bins)
		# base = number of distrobution divisions 
		base = 10
		division_width = float(bins_total) / base
		distrobution_division_split_values = []
		running_total = 0.0
		for i in range(base):
			distrobution_division_split_values.append(int(running_total))
			running_total += division_width
		distrobution_division_split_values.append(bins_total)
				
		message_length = 64*8
		message_max = 1 << message_length
			
		i = 1
		base_powers = [1]
		while i < message_max:
			i *= base
			base_powers.append(i)
		
		base_powers = base_powers[:-1]
				
		running_total = 0
		cumlative = [0]
		for bin in bins:
			running_total += bin
			cumlative.append(running_total)
					
		# plt.plot(cumlative)
		# plt.show()
		
		# print distrobution_division_split_values
		# print cumlative
		
		def encode(message):
			digits = deque()
			message_tmp = message
			for mod in reversed(base_powers):
				digit = message_tmp/mod
				digits.appendleft(digit)
				message_tmp -= digit*mod
				
			characters = []
			for digit in digits:
				lower_split_value = distrobution_division_split_values[digit]
				higher_split_value = distrobution_division_split_values[digit+1]
				value = random.randrange(lower_split_value, higher_split_value)
				index = lies_at_index_range(cumlative, value)
				char = chr(index + 30)	
				characters.append(char)
			
			return "".join(characters)
			
		return encode
			
	else:
		print "mode not supported"

def lies_at_index_range(dist, value):
	for i in range(len(dist)-1):
		lower_bound = dist[i]
		higher_bound = dist[i+1]
		if lower_bound <= value and value < higher_bound:
			return i
			
	raise Exception("Value %i not from distrobution: %s"%(value, str(dist)))

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description=description)
	parser.add_argument('-o', '--out', default="100/emulated/1")
	parser.add_argument('-m', '--mode',
		choices=modes.values(), default=modes['CHARACTER_DISTROBUTION'])
	parser.add_argument('-nu', '--nouse', action='store_true')
	args = vars(parser.parse_args())
	
	func = main(args["mode"])
	
	if not args["nouse"]:
		urls = []
		for _ in range(100):
			urls.append(func(random.getrandbits(64*8)))

		with open(args["out"], "wb") as f:
			pickle.dump(urls, f)
	
	
	
