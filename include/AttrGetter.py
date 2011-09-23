#coding:utf-8
class unpackAttrs:
	def __init__(self,attr):
		self.__attrs=attr
	def __getitem__(self,item):
		if item in self.__attrs:
			return self.__attrs[item]
		return None 
