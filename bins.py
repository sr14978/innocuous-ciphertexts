import arguments as args
import pickle

args.setup_argument(0, "in", "reference_urls")
args.setup_argument(1, "out", "reference_bins")

bins = [0] * 256

with open(args.args["in"] , "rb") as f:
  lines = pickle.load(f)

# with open(args.args["in"] , "r") as f:
#   lines = f.readlines()

for line in lines:
  for chr in line:
    bins[ord(chr)] += 1

print(bins)

with open(args.args["out"] , "wb") as f:
  pickle.dump(bins, f)
