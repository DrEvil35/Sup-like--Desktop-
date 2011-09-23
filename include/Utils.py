#coding: utf-8
from __future__ import with_statement
from Exceptions import ErrorRead,ErrorWrite,ErrorCreatePath
from PyQt4.QtGui import QMovie
from PyQt4.QtCore import QFile,QDir,QTextStream,QIODevice
from Mutex import Mutex
import re
import random
import os


URL_ESCAPE_PATTERN=re.compile(r'[svn|http|https|ftp]+\:\/\/[^\s<]{1,}',re.UNICODE)

URL_STR_PATTERN=u'<a href="%(url)s"> %(url)s </a>'

HTML_ESC_MAP = (
	("&gt;", u">"),
	("&lt;", u"<"),
	("&apos;", u"'"),
	("&quot;", u"\""),
	("&nbsp;", u" "),
	("&mdash;", u"—"),
	("&middot;", u"·")
)

XML_ESC_MAP = (
	("&gt;", ">"),
	("&lt;", "<"),
	("&apos;", "'"),
	("&quot;", "\""),
)

getFilePath             = os.path.join
smph                    = Mutex(1)

def getPathUserDir(*args):
	return getFilePath(os.path.expanduser("~"),'.suplike',*args)

def unescapeXML(xml):
	for esc, char in XML_ESC_MAP:
		xml = xml.replace(esc, char)
	xml = xml.replace("&amp;", "&")
	return xml

def escapeXML(xml):
	xml = xml.replace("&", "&amp;")
	xml = xml.replace("\x0C", "")
	xml = xml.replace("\x1B", "")
	for esc, char in XML_ESC_MAP:
		xml = xml.replace(char, esc)
	return xml

def getEntityChar(char):
	return unichr(int(char.group(1)))

def unescapeHTML(html):
	for esc, char in HTML_ESC_MAP:
		html = html.replace(esc, char)
	html = html.replace("&amp;", "&")
	return re.sub("&#(\d+);", getEntityChar, html)

def readFile(path, default=None, encoding=None):
	if not os.path.supports_unicode_filenames:
		path = path.encode("utf-8")
	if QFile.exists(path):
		f = QFile(path,parent)
		if f.open(QIODevice.ReadOnly):
			data=f.readAll().__str__()
		else:
			raise ErrorRead(u'Couldn\'t open file %s with code error %d'%path,f.error())
		f.close()
		if encoding:
			data = data.decode(encoding)
		return data
	else:
		dir = QDir(os.path.dirname(path))
		if not dir.exists():
			if not dir.mkpath(dir.path()):
				raise ErrorCreatePath(u'impossible to create a path!')
		writeFile(path, default)
		return default

def writeFile(path, data,mode=QIODevice.WriteOnly):
	with smph:
		if not os.path.supports_unicode_filenames:
			path = path.encode("utf-8")
		f=QFile(path)
		if f.open(mode):
			if type(data)==unicode:
				data=data.encode('utf-8')
			QTextStream(f) << data
			f.close()
		else:
			raise ErrorWrite('Couldn\'t write to file %s with code error %d'%path,f.error())

'''Replace url and wrapper in <a hreaf=> tags'''
def urlWrapper(body):
	for url in URL_ESCAPE_PATTERN.findall(body):
		body=body.replace(url,URL_STR_PATTERN%locals())
	return body
		
def setAni(label,path,parent=None):
	pix=QMovie(path,parent=parent)
	label.setMovie(pix)
	pix.start()

"""unpack incoming tuple for wrapper method"""
def unpackResponse(func):
	def unpack(self,args):
		func(self,*args)
	return unpack
	
"""Color utils"""
def encodeColorRGB(param):
	if not isinstance(param,int):
		param=int(param)
	return((param>>16)&255,(param>>8)&255,param&255)

"""int RGB to #hex"""
def encodeColorHEX(param):
	r,g,b=encodeColorRGB(param)
	return RGBtoHEX(r,g,b)

'''r,g,b into #hex'''
def RGBtoHEX(r,g,b):
	hexchars = "0123456789ABCDEF"
	return "#" + hexchars[r / 16] + hexchars[r % 16] + hexchars[g / 16] + hexchars[g % 16] + hexchars[b / 16] + hexchars[b % 16]

"""Function for color print debug info in stdout,deprecated"""
def cprintf(color,text):
	text=unicode(text)
	if color=="yellow":
		return "\033[1;33m"+text+" \033[0m"
	elif color=="white":
		return "\033[37;1m"+text+" \033[0m"
	elif color=="red":
		return "\033[0;31m"+text+" \033[0m"
	elif color=="green":
		return "\033[0;32m"+text+" \033[0m"
	elif color=="blue":
		return "\033[34m"+text+" \033[0m"
	elif color=="lightblue":
		return "\033[1;34m"+text+" \033[0m"
	elif color=="lightgray":
		return "\033[0;37m"+text+" \033[0m"
	elif color=="lightcyan":
		return "\033[1;36m"+text+" \033[0m"
	elif color=="lightred":
		return "\033[31;1m"+text+" \033[0m"
	else:
		return text