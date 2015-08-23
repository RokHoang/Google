#!/usr/bin/python
# -*- coding: utf8 -*-

# Dev: Vu Ngoc Minh Hoang  
# Public: 19-08-2015
# Version: 1.0
# Example: google Vu Ngoc Minh Hoang
from urllib2 import urlopen
from urllib2 import HTTPError
from urlparse import urlparse
import urllib2
import urllib
import sys
import re
import string
import codecs
import os
import argparse
#from bs4 import BeautifulSoup

#set admin
import admin
if not admin.isUserAdmin():
	admin.runAsAdmin()

#set default encoding utf-8
reload(sys).setdefaultencoding('utf8')

def setPath():
    old_path = os.path.dirname(os.path.abspath("__file__")) 
    if not old_path in os.environ['path']:
        path = old_path + ';%PATH%'
        os.system('setx PATH "%s" /M' % path)
def mergerQuery(string):
	query =''
	for i in range(0,len(string)):
		print str(string[i])
		query = query + str(string[i]) + '+'
	return query

if __name__ ==  '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-s","--setup", help="Setup", action="store_true")
	parser.add_argument("-vi","--vietnamese", help="Vietnamese", action="store_true")
	parser.add_argument("-t","--translate", help="Translate to Vietnamese", action="store_true")
	parser.add_argument("-m","--more", help="Display more results", action="store_true")
	parser.add_argument("string", type=str, nargs='+', help="Keyword")
	args = parser.parse_args()
	
	#set path
	if args.setup:
		setPath()
		sys.exit()
	
	#fake the mozilla headers
	header = {'User-Agent' : 'Mozilla/5.0 (X11; U; Linux i686; en-US)AppleWebKit/533.2(KHTML, like Gecko) Chrome/5.0.342.7 Safari/533.2'}

	#languages searching
	if args.vietnamese:
		lang = "lang_vi"
	else:
		lang = "lang_en"

	#merger url
	query = mergerQuery(args.string)

	#make request
	url = 'https://www.google.com/search?'
	values = {'start':'1','num':str((args.more+1)*10),'q':query,'lr':lang}
	data = urllib.urlencode(values)
	req = urllib2.Request(url + data, headers=header)

	
	#creat streamreader
	try:
		fpage = urlopen(req);
	except HTTPError, e:
		print "Error: ", e.code, e.reason

	print "Read data complete"
	#regex
	ftitle = re.compile(r'<!--m-->.*?\)">(.*?)</a></h3>.*?<!--n-->')
	flink = re.compile(r'<h3 class="r"><a href="(.*?)"')
	fcontent = re.compile(r'<span class="st">(.*?)</span><')
	###ftitle = re.compile(r'<!--m-->(.*?)<!--n-->')
	
	#fix content
	fix = re.compile('(<em>)|(</em>)|(&nbsp)|(</span>)|(<span class="f">)|(<wbr>)')

	while True:
		lnk = fpage.readline();
		#print link and content
		if not lnk:
			break
		else:
			rtitle = ftitle.findall(lnk)
			rlink = flink.findall(lnk)
			rcontent = fcontent.findall(lnk)
			if rtitle:
				for i in range(len(rtitle)):
					try:
						sys.stdout.write("[*]" + rtitle[i] + '\n|' + rlink[i] + '\n|' + fix.sub('',rcontent[i]) + '\n\n' )
					except Exception, e:
						pass
	fpage.close()	
