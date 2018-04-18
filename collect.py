#!/usr/bin/python2

"""
This program allows you to collect some url paths from unencrypted http requests in the following way
```bash
./collect.py --output <output_filepath> --size <number_of_urls>
eg ./collect.py --output 1000/fakes/1 --size 1000
```

There are already examples stored in

- 1000/fakes/
- 1000/normals/
- 1000/emulated/

and a reference list to test against at
- 1000/reference_urls
"""

import pyshark
import pickle
from scipy.stats import chisquare
import argparse
from sys import stdout as out


def main(output_file, sample_size=1000, continue_flag=False):

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

	with open(output_file, "rb") as f:
		urls = pickle.load(f)

	out.write("read %i samples"%(len(urls))); out.flush()

	for packet in capture.sniff_continuously(packet_count=sample_size):
		if len(urls) > sample_size: break
		urls.append(packet.http.get_field_value("request_uri")[1:])
		with open(output_file, "wb") as f:
			pickle.dump(urls, f)
		out.write("\rread %i samples"%(len(urls))); out.flush()

	print "\rread all %i samples"%(len(urls))

	capture.close()


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('-c', '--continue', action='store_true')
	parser.add_argument('-o', '--output', default="test_urls")
	parser.add_argument('-s', '--size', default=1000)
	args = vars(parser.parse_args())

	main(args["output"], args["size"], args["continue"])
