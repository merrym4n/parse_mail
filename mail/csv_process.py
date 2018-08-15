import csv
import requests

from PIL import Image
from PIL.ExifTags import TAGS

import hashlib

def write(dirname, data):
	with open(dirname + "/result.csv", "a") as f:
		wr = csv.writer(f)
		#wr.writerow(['Number', 'Date', 'Shorten URL', 'Full URL', 'FileName', 'Latitude', 'Longitude', 'MD5', 'SHA1'])
		lat, lon = latitude_longtitude(dirname + "/" + data[4])
		data.append(lat)
		data.append(lon)
		cont = file_as_bytes(open(dirname + "/" + data[4], 'rb'))
		md5 = hashlib.md5(cont).hexdigest()
		sha1 = hashlib.sha1(cont).hexdigest()
		data.append(md5)
		data.append(sha1)
		try:
			wr.writerow(data)
		except:
			nonascii = []
			nonascii.append(data[0])
			nonascii.append(data[1])
			nonascii.append(data[2])
			url_full = str(requests.post(data[2]).url)
			nonascii.append(url_full)
			FileName = url_full[url_full.rfind("/")+1:]
			nonascii.append(FileName)
			nonascii.append(data[5])
			nonascii.append(data[6])
			nonascii.append(data[7])
			nonascii.append(data[8])
			wr.writerow(nonascii)
			#nonascii.append()
		print "[*] Check result.csv"

def latitude_longtitude(FileName):
	try:
		img = Image.open(FileName)
		info = img._getexif()
		exif = {}
		for tag, value in info.items():
			decoded = TAGS.get(tag, tag)
			exif[decoded] = value
		exifGPS = exif['GPSInfo']
		latData = exifGPS[2]
		lonData = exifGPS[4]
		latDeg = latData[0][0] / float(latData[0][1])
		latMin = latData[1][0] / float(latData[1][1])
		latSec = latData[2][0] / float(latData[2][1])
		lonDeg = lonData[0][0] / float(lonData[0][1])
		lonMin = lonData[1][0] / float(lonData[1][1])
		lonSec = lonData[2][0] / float(lonData[2][1])
		Lat = (latDeg + (latMin + latSec / 60.0) / 60.0)
		if exifGPS[1] == 'S': Lat = Lat * -1
		Lon = (lonDeg + (lonMin + lonSec / 60.0) / 60.0)
		if exifGPS[3] == 'W': Lon = Lon * -1
		msg = "There is GPS info in this picture located at " + str(Lat) + "," + str(Lon)
		print msg
		return Lat, Lon
	except:
		return "None", "None"

def file_as_bytes(FileName):
	with FileName:
		return FileName.read()