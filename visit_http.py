#!/usr/bin/python2

from collections import deque
from HTMLParser import HTMLParser
import urllib2, urlparse

class MyHTMLParser(HTMLParser):
	def handle_starttag(self, tag, attrs):
		if tag != 'a':
			return
		attrs = dict(attrs)
		if "href" not in attrs:
			return
		link = dict(attrs)["href"]
		if link.startswith("https"):
			return
		elif link.startswith("http"):
			pass
		elif link.startswith("/"):
			obj = urlparse.urlparse(self.url)
			base_url = obj.scheme + "://" + obj.hostname
			link = base_url + link
		else:
			obj = urlparse.urlparse(self.url)
			base_url = obj.scheme + "://" + obj.hostname + obj.path
			link = base_url + '/' + link
		if link not in visited:
			queue.appendleft(link)
			visited.append(link)

visited = ["http://www.ucl.ac.uk/"]
queue = deque(visited)
parser = MyHTMLParser()

while len(queue) > 0:
	url = queue.pop()
	print url, len(queue)
	try:
		request = urllib2.urlopen(url)
		if request.getcode() != 200:
			continue
		if 'text/html' in request.headers.getheader('content-type'):
			contents = request.read()
			parser.url = url
			parser.feed(contents)

	except:
		continue
