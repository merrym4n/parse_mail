#-*- coding: utf-8 -*-
import os
import sys
import gmail
import csv

sys.path.insert(0, "./mail")
import secret_login
import parse_mail
import pic_process
import csv_process

try:
	g = gmail.login(secret_login.id, secret_login.pw)
	if g.logged_in:
		print('[*] Mail log in success')
		unread = g.inbox().mail(unread=True, sender='fl0ckfl0ck@hotmail.com')
		i = 0
		number = 0
		for new in unread:
			# If not fetch, can not read email
			new.fetch()

			# If Dir doesmn't exist, make Dir
			dirname = "./Downloads/" + str(new.sent_at)[:10]
			if not os.path.isdir(dirname):
				os.makedirs(dirname)
				with open(dirname + "/result.csv", "w") as f:
					wr = csv.writer(f)
					wr.writerow(['Number', 'Date', 'Shorten URL', 'Full URL', 'FileName', 'Latitude', 'Longitude', 'MD5', 'SHA1'])
					print("[*] make csv")
					number = 1

			i+=1
			title = new.subject.encode("UTF-8")
			print('New #' + str(i) + '//' + str(number))# + ' Title : ' + title)
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
					number += 1
			print
			#new.read()
	g.logout
except gmail.AuthenticationError:
	print('log in failed')