import numpy as np
import math
import calculate as calc

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

def go():
	fake_paths = [ "100/fakes/" + str(x) for x in range(1,4) ]
	normal_paths = [ "100/normals/" + str(x) for x in range(1,4) ]
	fakes = [calc.test(p) for p in fake_paths]
	normals = [calc.test(p) for p in normal_paths]
	fakes_dist = distrobution(np.mean(fakes), np.var(fakes))
	normals_dist = distrobution(np.mean(normals), np.var(normals))
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
	print(go())
