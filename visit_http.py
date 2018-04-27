#!/usr/bin/python2

"""
This simple web crawler program will follow links on webpages to create normal looking traffic.
```bash
./visit_http
```
"""

from collections import deque
from HTMLParser import HTMLParser
import urllib2, urlparse

class MyHTMLParser(HTMLParser):
	def handle_starttag(self, tag, attrs):
		attrs = dict(attrs)
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
		if attr not in attrs:
			return
		link = attrs[attr]
		if link == "":
			return

		if link.startswith("https"):
			return
		elif "javascript:void(0)" in link:
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
			path = obj.path[:-1] if obj.path[-1] == '/' else obj.path
			base_url = "http://" + obj.hostname + path
			link = base_url + '/' + link
		if link not in visited:
			queue.appendleft(link)
			visited.append(link)


if __name__ == "__main__":
	seed_sites = ["exeter", "dur", "manchester", "cam", "ox", "bath", "imperial", "ucl", "bristol", "uwe"]

	visited = ["http://www.%s.ac.uk/"%(uni) for uni in seed_sites]
	queue = deque(visited)
	parser = MyHTMLParser()

	while len(queue) > 0:
		url = queue.pop()
		print url, len(queue)
		try:
			request = urllib2.urlopen(url)
			if request.getcode() != 200:
				continue
			if len(queue) > 10000:
				continue
			if 'text/html' in request.headers.getheader('content-type'):
				contents = request.read()
				parser.url = url
				parser.feed(contents)

		except:
			continue
