#!/usr/bin/python2

description = """
Program to calculate the decision threshold between two distrobtions
"""

import numpy as np
import math
import calculate as calc
import bins
import argparse
import functools as ft
import os
import matplotlib.pyplot as plt

class distrobution():
	mu = 0
	sig = 1
	def __init__(self, mean, var):
		self.mu = mean
		self.sig = var

def get_func(d1, d2):
	return (d2.sig-d1.sig, 2*(d1.sig*d2.mu - d2.sig*d1.mu), d2.sig*d1.mu*d1.mu - d1.sig*d2.mu*d2.mu - d1.sig*d2.sig*math.log(d2.sig/d1.sig))

def solve_for_x(a,b,c):
	test = b*b - 4*a*c
	if test < 0:
		return None
	elif test == 0:
		return ((-b) + math.sqrt(test) ) / 2*a
	else:
		return ( ((-b) + math.sqrt(test) ) / (2*a), ((-b) - math.sqrt(test) ) / (2*a) )

def go(size=100, mode=bins.default_mode):
	
	base_path = os.path.dirname(os.path.abspath(__file__))
	fake_path = base_path + "/" + str(size) + "/fakes/"
	normal_path = base_path + "/" + str(size) + "/normals/"
	fake_paths = [fake_path + p for p in os.listdir(fake_path) if p != "results"]
	normal_paths = [
		normal_path + p for p in os.listdir(normal_path) if p != "results"]
	test = ft.partial(
		calc.test,
		reference_file=size + "/reference_" + mode + "_bins",
		mode=mode
	)

	fakes = [test(p) for p in fake_paths]
	normals = [test(p) for p in normal_paths]
	plt.plot(fakes, 'ro', normals, 'go')
	plt.show()
	
	fakes_dist = distrobution(np.mean(fakes), np.var(fakes, ddof=1))
	normals_dist = distrobution(np.mean(normals), np.var(normals, ddof=1))
	coeffs = get_func(fakes_dist, normals_dist)
	solutions = solve_for_x(*coeffs)
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

	parser = argparse.ArgumentParser(description=description)
	parser.add_argument('-s', '--size', default="100")
	parser.add_argument('-m', '--mode',
		choices=bins.modes.values(), default=bins.default_mode)
	args = vars(parser.parse_args())

	with open(args["size"] + "/threshold_" + args["mode"], "w") as f:
		f.write(str(go(args["size"], args["mode"])))


