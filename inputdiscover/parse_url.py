from urllib.parse import urlparse
from urllib.parse import parse_qs
import requests
from html.parser import HTMLParser
import json

# Takes a url and returns a dictionary containing key/value pairs
# representing the query string parameters provided in the url.
def parseURLForInput (url):
	# A tuple representing the url. Contains information such as:
	# urlparse("http://www.google.com/?a=b")
	# 	-> (scheme='http', netloc='www.google.com', path='/', params='',
	#		query='a=b', fragment='')
	parsed = urlparse(url)
	
	# The dictionary representing fuzzable inputs. Keys are the name
	# of the input in the query string, value is the value for the query param.
	inputs = parse_qs(parsed.query)

	return inputs
#end def

# Takes two urls and assesses if the two are the same page (ignores query
# string parameters and url parameters.)
def arePagesSame(url1, url2):
	parsed1 = urlparse(url1)
	parsed2 = urlparse(url2)
	same = False
	if ((parsed1.netloc + parsed1.path) == (parsed2.netloc + parsed2.path)):
		same = True

	return same
#end def

# Parses an HTML page and stores all input fields with associated actions as a result.
class FormHTMLParser(HTMLParser):
	# result will look like:
	#	[(actionPage<"loginPage.jsp">, method<"get"/"post">, inputs<["username","password"]>), ...]
	result = []
	inputs = []

	actionPage = None
	method = None
	lookingForInput = False

	def __init__(self):
		HTMLParser.__init__(self)
		

	def handle_starttag(self, tag, attrs):
		if (tag == "form"):
			self.lookingForInput = True
			# Check for actions and methods
			for item in attrs:
				if (isinstance(item, list) or isinstance(item, tuple)):
					if (item[0].strip() == "action"):
						self.actionPage = item[1]
					elif (item[0].strip() == "method"):
						self.method = item[1]
		elif (tag == "input" and self.lookingForInput):
			self.allowed = True
			for item in attrs:
				if (isinstance(item, list) or isinstance(item, tuple)):
					if (item[0].strip() == "type" and item[1].strip() == "submit"):
						self.allowed = False
					elif (item[0].strip() == "name" and self.allowed):
						self.inputs.append(item[1])

	def handle_endtag(self, tag):
		if (tag == "html"):
			# Finished scraping
			if (len(self.inputs) > 0):
				tup = (self.actionPage, self.method, self.inputs)
				self.result.append(tup)
			print(json.dumps(self.result, indent=2))
			# TODO: What do we want to do with the result?
		elif (tag == "form"):
			# Finished with our form
			self.lookingForInput = False
			if (len(self.inputs) > 0):
				tup = (self.actionPage, self.method, self.inputs)
				self.result.append(tup)
				self.actionPage = None
				self.method = None
				self.inputs = []
		#handle end form tag

def getFormFields(url):
	parse = FormHTMLParser()
	page = requests.get(url)
	parse.feed(page.text)


result = parseURLForInput("http://www.google.com/?b=thing&j=3")
print ("Fuzzable inputs: " + json.dumps(result, indent=2))


areSame = arePagesSame("http://www.google.com/?bitches=shit", "http://www.google.com/")
print ("Are the pages the same? " + ("Yes" if areSame else "No"))

getFormFields("http://127.0.0.1/dvwa/login.php")