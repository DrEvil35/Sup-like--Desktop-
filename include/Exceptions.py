#coding:utf-8

'''Exceptions for utils-modules'''

class FileProcess(Exception):
	pass

class ErrorRead(FileProcess):
	pass

class ErrorWrite(FileProcess):
	pass

class ErrorCreatePath(FileProcess):
	pass
