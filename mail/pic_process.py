import requests
import re
import unicodedata
import urllib
import urllib2

def CheckUrl(url):
	try:
		while(True):
			res = requests.post(url)
			if res.url != url:
				return url
			else:
				if url[len(url)-1] == "/":
					raise NameError
				url = url[:-1]
	except NameError:
		print("Wrong URL")
	except Exception as e:
		print e

def short2full(url_short):
	# If i pass the shorten url, it returns full url
	url_full = requests.post(url_short).url
	# The variable url_full's type is unicode, but the each of letter is unicode.
	# So i can't use just in time. So i need to change it to ascii first for using. And then decode it as 'utf8'
	url_full_enc = urllib.unquote(url_full.encode('ascii', 'ignore')).decode('utf8')
	# noramlize string because of spliting korean.
	url_fin = unicodedata.normalize('NFC', unicode(url_full_enc))
	# shorten_url to full_url
	return url_fin

def DownPic(url_full, dirname):
	FileName = url_full[url_full.rfind("/")+1:]

	with open(dirname + "/" + FileName, "wb") as f:
		for chunk in res.iter_content(chunk_size=128):
			f.write(chunk)
	return FileName

def DownPic2(dirname, url_short, url_full):
	FileName = url_full[url_full.rfind("/")+1:]
	with open(dirname + "/" + FileName, "wb") as f:
		try:
			f.write(urllib2.urlopen(url_full).read())
		# There is some encoding error that i can't handle. So temporary use exception.	
		except:
			f.write(urllib2.urlopen(requests.post(url_short).url).read())
	return FileName