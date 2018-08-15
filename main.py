#-*- coding: utf-8 -*-
import os
import sys
import gmail
import csv
import folium

# To import functions that i made.
sys.path.insert(0, "./mail")
import secret_login
import parse_mail
import pic_process
import csv_process

try:
	# login with secret_login. It just store my id & pw.
	g = gmail.login(secret_login.id, secret_login.pw)
	if g.logged_in:
		print('[*] Mail log in success')
		# Only select unread mail from fl0ckfl0ck@hotmail.com
		unread = g.inbox().mail(unread=True, sender='fl0ckfl0ck@hotmail.com')
		# This is for mail index.
		i = 0
		# This is for csv index.
		number = 0
		# This is for gps visualization of all received mail.
		gps_all = folium.Map(location=[22.9602, 119.2102], zoom_start=5)

		for new in unread:
			# If not fetch, can not read email
			new.fetch()

			# If Dir doesn't exist, make Dir
			dirname = "./Downloads/" + str(new.sent_at)[:10]
			if not os.path.isdir(dirname):
				os.makedirs(dirname)
				# This is for basic csv.
				with open(dirname + "/result.csv", "w") as f:
					wr = csv.writer(f)
					wr.writerow(['Number', 'Date', 'Shorten URL', 'Full URL', 'FileName', 'Latitude', 'Longitude', 'MD5', 'SHA1'])
					print("[*] make csv")
					number = 1
				# This is for gps visualization of selected day.
				gps = folium.Map(location=[22.9602, 119.2102], zoom_start=5)

			i+=1
			title = new.subject.encode("UTF-8")
			print('New #' + str(i))# + ' Title : ' + title)
			#parse_mail.print_content(new.body)
			urls = parse_mail.content2url(new.body)
			# To handle many urls
			for url in urls:
				data = []
				data.append(number)
				data.append(new.sent_at)
				url_short = pic_process.CheckUrl(url)
				# It only works, when the url is working.
				if url_short != None:
					data.append(url_short)
					print("===================================")
					print "Shorten URL is " + str(url_short)
					url_full = pic_process.short2full(url_short)
					data.append(url_full)
					print url_full
					FileName = pic_process.DownPic2(dirname, url_short, url_full)
					data.append(FileName)
					print("Successes to downloads %s" %(FileName))
					print("===================================")
					csv_process.write(dirname, data)
					lat, lon = csv_process.latitude_longtitude(dirname + "/" + FileName)
					gps = csv_process.marking(FileName, gps, lat, lon)
					gps_all = csv_process.marking(FileName, gps_all, lat, lon)
					number += 1
				if gps != "None":
					gps.save(dirname + "/gps.html")
			print
			#new.read()
	gps_all.save('gps.html')
	g.logout
except gmail.AuthenticationError:
	print('log in failed')