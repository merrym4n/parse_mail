import re

def print_content(data):
	print(data)

def content2url(data):
	regex = re.compile('https?://[a-zA-Z0-9]+.[a-zA-Z0-9]+/[a-zA-Z0-9]+')
	url = regex.findall(data)
	return list(set(url))