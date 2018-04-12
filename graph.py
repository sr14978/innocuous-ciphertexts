
import numpy as np
import math
import calculate as calc
import bins
import functools as ft
import os
import matplotlib.pyplot as plt

size=100
mode=bins.default_mode

base_path = os.path.dirname(os.path.abspath(__file__))

fake_path = base_path + "/" + str(size) + "/fakes/"
normal_path = base_path + "/" + str(size) + "/normals/"
emulated_path = base_path + "/" + str(size) + "/emulated/"


fake_paths = [fake_path + p for p in os.listdir(fake_path) if p != "results"]
normal_paths = [normal_path + p for p in os.listdir(normal_path) if p != "results"]
emulated_paths = [emulated_path + p for p in os.listdir(emulated_path) if p != "results"]

test = ft.partial(
	calc.test_file,
	reference_file= str(size) + "/reference_" + mode + "_bins",
	mode=mode
)

fakes = [test(p) for p in fake_paths]
normals = [test(p) for p in normal_paths]
emulateds = [test(p) for p in emulated_paths]

plt.plot(fakes, 'ro', normals, 'go', emulateds, 'bo')
plt.show()
