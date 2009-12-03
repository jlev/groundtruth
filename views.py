from django.http import HttpResponse
import urllib2

def proxy(request,theURL):
	"""This is a blind proxy that we use to get around browser
	restrictions that prevent the Javascript from loading pages not on the
	same server as the Javascript.  This has several problems: it's less
	efficient, it might break some sites, and it's a security risk because
	people can use this proxy to browse the web and possibly do bad stuff
	with it.  It only loads pages via http and https, but it can load any
	content type. It supports GET requests."""
	
	# Designed to prevent Open Proxy type stuff.
	allowedHosts = ['www.openlayers.org', 'openlayers.org', 
					'labs.metacarta.com', 'world.freemap.in', 
					'prototype.openmnnd.org', 'geo.openplans.org',
					'sigma.openplans.org', 'demo.opengeo.org',
					'www.openstreetmap.org','www.example.com',
	#mine
					'virtualgaza.media.mit.edu:8080',
					'groundtruth.media.mit.edu:8080',
	]
	
	response = HttpResponse()

	#fix URL percent encoding
	url = theURL.replace('%2F','/')
	url.replace('%3A',':')

	if url == "":
		url = "http://www.example.com"

	try:		
		host = url.split("/")[2]
		if allowedHosts and not host in allowedHosts:
			response.write("Status: 502 Bad Gateway\n")
			response.write("Content-Type: text/plain\n")
			response.write("This proxy does not allow you to access the location (%s).\n" % (host,))

		elif url.startswith("http://") or url.startswith("https://"):
#			if request.method == "POST":
#				length = int(request.META["CONTENT_LENGTH"])
#				headers = {"Content-Type": request.META["CONTENT_TYPE"]}
#				body = sys.stdin.read(length)
#				##fix
#				r = urllib2.Request(url, body, headers)
#				y = urllib2.urlopen(r)
#			else:
			y = urllib2.urlopen(url)
			
			i = y.info()
			if i.has_key("Content-Type"):
				response.write("Content-Type: %s" % (i["Content-Type"]))
			else:
				response.write("Content-Type: text/plain\n")
			response.write(y.read())
			y.close()
		else:
			response.write("Content-Type: text/plain\n")
			response.write("Illegal request.\n")
	
	except Exception, E:
		response.write("Status: 500 Unexpected Error\n")
		response.write("Content-Type: text/plain\n")
		response.write("Some unexpected error occurred. Error text was:\n")
		response.write(str(E))
		
	return response
