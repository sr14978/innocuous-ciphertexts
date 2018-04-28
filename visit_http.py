#!/usr/bin/python2

"""
This simple web crawler program will follow links on webpages to create normal looking traffic.
```bash
./visit_http
```
"""

from collections import deque
from HTMLParser import HTMLParser
import urlparse
import traceback, sys
import urllib2

class MyHTMLParser(HTMLParser):
	def handle_starttag(self, tag, attrs):
		if tag == 'a':
			attr = "href"
		elif tag == "img":
			attr = "src"
		elif tag == "script":
			attr = "src"
		elif tag == "link":
			attr = "href"
		else:
			return
		if self.count > 5:
                        return
                self.count += 1
		attrs = dict(attrs)
		if attr not in attrs:
			return
		link = attrs[attr]
		if link == "":
			return

		if link.startswith("https"):
			return
		elif link.startswith("#"):
			return
		elif "javascript" in link:
			return
		elif link.startswith("http"):
			pass
		elif link.startswith("//"):
			link = "http:" + link
		elif link.startswith("/"):
			obj = urlparse.urlparse(self.url)
			base_url = obj.scheme + "://" + obj.hostname
			link = base_url + link
		else:
			obj = urlparse.urlparse(self.url)
			path = obj.path if len(obj.path) == 0 or obj.path[-1] != '/' else obj.path[:-1]
			base_url = "http://" + obj.hostname + path
			link = base_url + '/' + link
		if link not in visited:
			queue.appendleft(link)
			visited.append(link)
			print "ADDED", link

if __name__ == "__main__":

	seed_sites = ["exeter", "manchester", "cam", "ox", "bath",
			"imperial", "ucl", "bristol", "uwe"]
	visited = ["http://www.%s.ac.uk/"%(uni) for uni in seed_sites]

	# with open("good_urls", "r") as f:
	#	seed_sites = [l[:-1] for l in f.readlines()]
	# visited = ["http://" + site for site in seed_sites]

	queue = deque(visited)
	parser = MyHTMLParser()

	while len(queue) > 0:
		url = queue.pop()
		print "queue", len(queue)
		print "visiting", url
		try:
			request = urllib2.urlopen(url)
			if request.getcode() != 200:
				continue
			if request.geturl().startswith("https"):
				print "redirected to https"
				continue
			if len(queue) > 10000:
				continue
			if 'text/html' in request.headers.getheader('content-type'):
				contents = request.read()
				parser.count = 0
				parser.url = url
				parser.feed(contents)

		except:
			traceback.print_exc(file=sys.stdout)
