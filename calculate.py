from scipy.stats import chisquare
import arguments as args
import pickle


def test(test_file=None, reference_file=None):

	args.setup_argument(0, "test", "test_urls")
	args.setup_argument(1, "reference", "100/reference_bins")

	if test_file == None:
		test_file = args.args["test"]
	if reference_file == None:
		reference_file = args.args["reference"]

	with open(test_file, "rb") as f:
	  urls = pickle.load(f)

	test = [0] * 256

	for url in urls:
	  for chr in url:
	    test[ord(chr)] += 1

	with open(reference_file, "rb") as f:
	  reference = pickle.load(f)

	paired = zip(test, reference)
	filtered = [(a,b) for a,b in paired if b != 0]
	test, reference = zip(*filtered)

	return chisquare(test, reference).statistic

if __name__ == "__main__":
	print(test())
