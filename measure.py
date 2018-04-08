import collect as col
import calculate as calc
import argparse
import os

def test():
	parser = argparse.ArgumentParser()
	parser.add_argument('-s', '--size', default="100")
	parser.add_argument('-f', '--folder', default="fakes")
	args = vars(parser.parse_args())

	path = args["size"] + "/" + args["folder"] + "/"

	index = 1
	while os.path.exists(path + str(index)):
		index += 1

	col.main(True, path + str(index))

	with open(args["size"] + "/threshold", "r") as f:
		threshold = float(f.readline())

	val = calc.test(
		path + str(index),
		args["size"] + "/reference_bins"
	)

	return val > threshold


if __name__ == "__main__":
  print("Fake" if test() else "Normal")
