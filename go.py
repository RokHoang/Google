#!/usr/bin/python
# -*- coding: utf8 -*-

# Dev: Vu Ngoc Minh Hoang  
# Public: 19-08-2015
# Version: 1.0
# Example: google Vu Ngoc Minh Hoang
from urllib2 import urlopen
from urllib2 import HTTPError
import urllib2
import sys
import re
import string
import codecs
import os
import admin
#set admin
#if not admin.isUserAdmin():
#	admin.runAsAdmin()

sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
sys.stdin = codecs.getreader('utf_8')(sys.stdin)

def setPath():
    old_path = os.path.dirname(os.path.abspath("__file__")) 
    if not old_path in os.environ['path']:
        path = old_path + ';%PATH%'
        os.system('setx PATH "%s" /M' % path)
def mergerURL():
	url = 'https://www.google.com/search?q='
	for i in range(1,len(sys.argv)):
		url = url + str(sys.argv[i]) + '+'
	return url

if __name__ ==  '__main__':
	#set path
	if (len(sys.argv)==2 and sys.argv[1]=='setup'):
		setPath()
		sys.exit()
	
	#fake the mozilla headers
	header = {'User-Agent' : 'Mozilla/5.0 (X11; U; Linux i686; en-US)AppleWebKit/533.2(KHTML, like Gecko) Chrome/5.0.342.7 Safari/533.2'}

	#merger url
	url = mergerURL()

	#make request
	req = urllib2.Request(url, headers=header)

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
		#print lnk
		if not lnk:
			break
		else:
			rtitle = ftitle.findall(lnk)
			rlink = flink.findall(lnk)
			rcontent = fcontent.findall(lnk)
			if rtitle:
				for i in range(len(rtitle)):
					try:
						sys.stdout.write("[*]" + rtitle[i] + '\n|' + rlink[i] + '\n|' + fix.sub('',rcontent[i]) + '\n')
					except Exception, e:
						pass

	fpage.close()	
