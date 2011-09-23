#coding:utf-8
from include.Utils import readFile,writeFile,getPathUserDir
from include.Locations import DIR_CONFIG

DEFAULT_DATA=u'{PASSWORD:'',USER:'',SERVER:\'localhost\',PORT:\'5222\'}'


class _container:
	def __init__(self,_args):
		self.__dict__ = _args

class Config:
	def __init__(self,path):	
		self._path      = path 
		self._container = container(eval(readFile(self._path)))
	@property
	def sets(self):
		return self._container
	def save(self):
		writeFile(self._path,str(self._container.__dict__))
