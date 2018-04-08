#!/usr/bin/python3

import pyshark
import pickle
from scipy.stats import chisquare
import argparse

def main(reset, output_file):

	if reset:
		with open(output_file, "wb") as f:
			pickle.dump([], f)

	capture = pyshark.LiveCapture(
		interface="ens33",
		display_filter='http && http.request.method == \
						"GET" && http.request.uri != "/"'
	)

	sample_size = 100
	steps = 20
	jump = sample_size/steps
	for i in range(steps):
		print("read %i samples"%(i*jump), flush=True)
		capture.sniff(packet_count=jump)
		urls = [p.http.get_field_value("request_uri")[1:] for p in capture]
		with open(output_file, "rb") as f:
			current_urls = pickle.load(f)
		with open(output_file, "wb") as f:
			pickle.dump(current_urls + urls, f)

	print("read %i samples"%(sample_size))

	capture.close()


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('reset', nargs='?', default=False)
	parser.add_argument('-o', '--output', default="test_urls")
	args = vars(parser.parse_args())

	main(args["reset"], args["output"])
