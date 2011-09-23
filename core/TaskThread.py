from __main__ import printf,FLAG_ERROR
from PyQt4.QtCore import QThread

TaskThread(QThread):
	def __init__(self,queue,parent=None):
		super(TaskThread,self).__init__(parent)
		self._queue=queue
	def run(self):
		while(True):
			func,args=self._queue.put()
			try:
				func(*args)
			except Exception,e:
				printf('Exception in task thread traceback: %s'%str(e))
			self._queue.task_done()
