#cofing:utf-8
from PyQt4.QtGui import (QStyledItemDelegate,QStyleOptionButton,QStyleOption,QRect)
from PyQt4.QtCore import Qt

class Delegate(QStyledItemDelegate):
	def __init__(self,parent):
		super(Delegate,self).__init__(parent)
		self._parent=parent
	def paint(self,painter,option,index):
		model=index.model()
		option.state &= QStyle.State_Enabled ^ QStyle.State_Selected
		if model.parent(index).isValid():
			option.rect.setLeft(0)
			super(Delegate,self).paint(painter,option,index)
		else:
			i=9
			RECT = option.rect
			button = QStyleOptionButton()
			button.rect = RECT
			button.state = option.state
			button.state &= QStyle.State_HasFocus
			button.state |= QStyle.State_Raised
			button.features = QStyleOptionButton.None
			self._parent.style().drawControl(QStyle.CE_PushButton,button,painter,self._parent)
			branch = QStyleOption()
			branch.rect = QRect(RECT.left() + i/2, RECT.top() + (RECT.height() - i)/2, i, i)
			branch.palette = option.palette
			branch.state = QStyle.State_Children
			if self._parent.isExpanded(index):
				branch.state |= QStyle.State_Open
			self._parent.style().drawPrimitive(QStyle.PE_IndicatorBranch, branch, painter,self._parent);
			textrect = QRect(RECT.left() + i * 2, RECT.top(), RECT.width() - ((5*i)/2), RECT.height());
			#text = elidedText(option.fontMetrics, textrect.width(), Qt.ElideMiddle, model.data(index, Qt.DisplayRole).toString())
			text = model.data(index, Qt.DisplayRole).toString()
			self._parent.style().drawItemText(painter,textrect,Qt.AlignCenter,option.palette,self._parent.isEnabled(),text)