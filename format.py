import pickle
import sys

if False:
	with open(sys.argv[1], 'rb') as f:
		urls = pickle.load(f)

	with open(sys.argv[1], 'w') as f:
		for url in urls:
			f.write(url + '\n')

else:
	with open(sys.argv[1], 'r') as f:
		urls = [l[:-1] for l in f.readlines()]
		
	with open(sys.argv[1], 'wb') as f:
		pickle.dump(urls, f)

