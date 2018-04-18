#!/usr/bin/python2

"""
This program can be used to view data such as urls and distrobution historgram bins as follows
```bash
./view.py <filepath>
eg ./view.py 100/reference_urls
```
"""

import pickle
import sys

if __name__ == "__main__":
    with open(sys.argv[1], "rb") as f:
      print(pickle.load(f))
