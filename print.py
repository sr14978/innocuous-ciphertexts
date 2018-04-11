#!/usr/bin/python2

import pickle
import sys
with open(sys.argv[1], "rb") as f:
  print(pickle.load(f))
