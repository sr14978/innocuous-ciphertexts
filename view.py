#!/usr/bin/python2

"""
There are already examples stored in
 - 100/fakes/
 - 100/normals/
 - 100/emulated/
  
and a reference list to test against at
 - 100/reference_urls
  
These can be viewed using the print program
./print.py <filepath>
eg ./print.py 100/reference_urls
"""

import pickle
import sys
with open(sys.argv[1], "rb") as f:
  print(pickle.load(f))
