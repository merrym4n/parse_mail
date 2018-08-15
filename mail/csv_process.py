import csv
import requests

from PIL import Image
from PIL.ExifTags import TAGS

import hashlib

import folium


def write(dirname, data):
	with open(dirname + "/result.csv", "a") as f:
		wr = csv.writer(f)
		lat, lon = latitude_longtitude(dirname + "/" + data[4])
		data.append(lat)
		data.append(lon)
		cont = file_as_bytes(open(dirname + "/" + data[4], 'rb'))
		md5 = hashlib.md5(cont).hexdigest()
		sha1 = hashlib.sha1(cont).hexdigest()
		data.append(md5)
		data.append(sha1)
		# Try to write list to csv. 
		try:
			wr.writerow(data)
		# If there is encoding error, just split the income URL and use it.
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

# input : png => output : latitude & longtitude. If there is no gps information, then it return "None".
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
		return Lat, Lon
	except:
		return "None", "None"

# Read file as bytes.
def file_as_bytes(FileName):
	with FileName:
		return FileName.read()

# Marking the position on map.
def marking(FileName, gps, lat, lon):
	try:
		folium.Marker(location=[float(lat), float(lon)], popup=FileName).add_to(gps)
	except:
		pass
	return gps