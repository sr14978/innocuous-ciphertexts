import calculate as calc
import argparse

def test():
	parser = argparse.ArgumentParser()
	parser.add_argument('-s', '--size', default="100")
	parser.add_argument('-f', '--folder', default="fakes")
	parser.add_argument('-i', '--index', default="1")
	args = vars(parser.parse_args())

	with open(args["size"] + "/threshold", "r") as f:
		threshold = float(f.readline())

	val = calc.test(
		args["size"] + "/" + args["folder"] + "/" + args["index"],
		args["size"] + "/reference_bins"
	)

	return val > threshold


if __name__ == "__main__":
  print(test())
