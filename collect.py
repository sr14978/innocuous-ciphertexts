#!/usr/bin/python2

"""
This program allows you to collect some url paths from unencrypted http requests in the following way
./collect.py --output <output_filepath> --size <number_of_urls>
eg ./collect.py --output 100/fakes/1 --size 100

There are already examples stored in

- 100/fakes/
- 100/normals/
- 100/emulated/

and a reference list to test against at
- 100/reference_urls
"""

import pyshark
import pickle
from scipy.stats import chisquare
import argparse

def main(output_file, sample_size=100, continue_flag=False):

	if type(sample_size) == str:
		sample_size = int(sample_size)

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
	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('-c', '--continue', action='store_true')
	parser.add_argument('-o', '--output', default="test_urls")
	parser.add_argument('-s', '--size', default=100)
	args = vars(parser.parse_args())

	main(args["output"], args["size"], args["continue"])
