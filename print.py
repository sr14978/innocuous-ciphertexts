#!/usr/bin/python3
import pickle
import sys
with open("100/reference_" + sys.argv[1] + "_bins", "rb") as f:
  print(pickle.load(f))
