#coding:utf-8
from TextCutter import pasteInInterval,splitText,TextCutter

class string(str):
	def __init__(self,_str):
		super(string,self).__init__(_str)
		self.splitLength = splitText
		self.pasteInterval = pasteInInterval
	def splitIter(self,interval):
		return TextCutter(self,interval).__iter__()
	