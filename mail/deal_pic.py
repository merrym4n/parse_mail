import requests
import re
import unicodedata
import urllib

def CheckUrl(url):
	try:
		while(True):
			res = requests.post(url)
			if res.url != url:
				csv = []
				url_full = res.url
				# The type of res.url is unicode. So if i wanna use it as a unicode, i have to change type as ascii by using encode('ascii', 'ignore').
				dec = urllib.unquote(url_full.encode('ascii', 'ignore'))
				print dec
				csv.append(url)
				csv.append(dec)
				csv.append(dec[dec.rfind("/")+1:])
				print csv
				return dec
			else:
				#print str(len(url)-1) + " " + url[len(url)-1],
				if url[len(url)-1] == "/":
					raise NameError
				#print("pass")
				url = url[:-1]
	except NameError:
		print("Wrong URL")
	except Exception as e:
		print e


'''
			print "==============================="
				url_short = url
				print "Shorten URL\t: " + url_short
				url_full = res.url
				print "Full URL\t: " + url_full
				#FileName = unicodedata.normalize('NFC', unicode(res.url[url_full.rfind("/")+1:]))
				#FileName = urllib.unquote(url.encode(res.url[url_full.rfind("/")+1:]))
				#FileName = res.url[url_full.rfind("/")+1:].encode("UTF-8")
				FileName = res.url[url_full.rfind("/")+1:]
				print "FileName\t: " + FileName
				
				with open(FileName, "wb") as f:
					for chunk in res.iter_content(chunk_size=128):
						f.write(chunk)
				
				print "==============================="
				'''