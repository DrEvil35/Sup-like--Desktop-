#coding:utf-8
from PyQt4.QtGui import QStyledItemDelegate,QStyle
class Delegate(QStyledItemDelegate):
	def paint(self,painter,option,index):
		option.state &= QStyle.State_Enabled ^ QStyle.State_Selected
		super(Delegate,self).paint(painter,option,index)