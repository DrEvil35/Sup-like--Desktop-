#coding:utf-8
from PyQt4.QtCore import QSemaphore

class Mutex(QSemaphore):
	def __init__(self,n=0):
		QSemaphore.__init__(self,n)
	def __enter__(self):
		self.acquire()
	def __exit__(self,*args):
		self.release()

