#!/usr/bin/python2

description = """
Program to collect a list of paths from clear http requests
"""

import pyshark
import pickle
from scipy.stats import chisquare
import argparse

def main(output_file, sample_size=100, continue_flag=False):
		
	if not continue_flag:
		with open(output_file, "wb") as f:
			pickle.dump([], f)

	capture = pyshark.LiveCapture(
		interface="ens33",
		display_filter='http && http.request.method == \
						"GET" && http.request.uri != "/"'
	)

	steps = 20
	jump = sample_size/steps
	for i in range(steps):
		print("read %i samples"%(i*jump))
		capture.sniff(packet_count=jump)
		urls = [p.http.get_field_value("request_uri")[1:] for p in capture]
		with open(output_file, "rb") as f:
			current_urls = pickle.load(f)
		with open(output_file, "wb") as f:
			pickle.dump(current_urls + urls, f)

	print("read %i samples"%(sample_size))

	capture.close()


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description=description)
	parser.add_argument('-c', '--continue', action='store_true')
	parser.add_argument('-o', '--output', default="test_urls")
	parser.add_argument('-s', '--size', default=100)
	args = vars(parser.parse_args())

	main(args["output"], args["size"], args["continue"])
