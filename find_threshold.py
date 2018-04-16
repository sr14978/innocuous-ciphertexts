#!/usr/bin/python2

"""
This program can calculate a decision threshold to differentiate the normal and fake distrobutions.
./find_threshold.py --mode <binning_method>
eg ./find_threshold.py --mode charq
"""

import numpy as np
import math
import calculate as calc
import bins
import argparse
import functools as ft
import os
import matplotlib.pyplot as plt

class _distrobution():
	mu = 0
	sig = 1
	def __init__(self, mean, var):
		self.mu = mean
		self.sig = var

def _get_func(d1, d2):
	"""Constructs a quadratic formula that constrains the position where the probility density is equal for both normal distrobutions."""
	return (d2.sig-d1.sig, 2*(d1.sig*d2.mu - d2.sig*d1.mu), d2.sig*d1.mu*d1.mu - d1.sig*d2.mu*d2.mu - d1.sig*d2.sig*math.log(d2.sig/d1.sig))

def _solve_for_x(a,b,c):
	"""Solves the quadratic defined by the given coeffients to find x using the quandratic formula."""
	test = b*b - 4*a*c
	if test < 0:
		return None
	elif test == 0:
		return ((-b) + math.sqrt(test) ) / 2*a
	else:
		return ( ((-b) + math.sqrt(test) ) / (2*a), ((-b) - math.sqrt(test) ) / (2*a) )

def calculate(size=100, mode=bins.default_mode):
	"""Calculates the point of equal probility density when the the two datasets are modelled as normal distrobutions"""
	base_path = os.path.dirname(os.path.abspath(__file__))
	fake_path = base_path + "/" + str(size) + "/fakes/"
	normal_path = base_path + "/" + str(size) + "/normals/"
	fake_paths = [fake_path + p for p in os.listdir(fake_path) if p != "results"]
	normal_paths = [
		normal_path + p for p in os.listdir(normal_path) if p != "results"]
	test = ft.partial(
		calc.test_file,
		reference_file=size + "/reference_" + mode + "_bins",
		mode=mode
	)

	fakes = [test(p) for p in fake_paths]
	normals = [test(p) for p in normal_paths]
	plt.plot(fakes, 'ro', normals, 'go')
	plt.show()

	fakes_dist = _distrobution(np.mean(fakes), np.var(fakes, ddof=1))
	normals_dist = _distrobution(np.mean(normals), np.var(normals, ddof=1))
	coeffs = _get_func(fakes_dist, normals_dist)
	solutions = _solve_for_x(*coeffs)
	if solutions == None:
		return None
	if type(solutions) == float:
		return solutions
	if type(solutions) == tuple:
		x,y = solutions
		if (lambda a,b: a < x and x < b)(normals_dist.mu, fakes_dist.mu):
			return x
		elif (lambda a,b: a < y and y < b)(normals_dist.mu, fakes_dist.mu):
			return y
		else:
			return None

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('-s', '--size', default="100")
	parser.add_argument('-m', '--mode',
		choices=bins.modes.values(), default=bins.default_mode)
	args = vars(parser.parse_args())

	with open(args["size"] + "/threshold_" + args["mode"], "w") as f:
		results = calculate(args["size"], args["mode"])
		f.write(str(results))
