#coding:utf-8

def pasteInInterval(string,length=1,replaceChar='')
	replaceChar.join(splitText(string,length)

def splitText(string,length=1):
	return [sym for sym in TextCutter(string,length)]
 
class TextCutter:
	def __init__(self,string,step=1):
		self.fullLen=len(string)
		self.currentStep=0
		self.string=string
		self.step=step
	def __iter__(self):
		return self
	def next(self):
		current=self.fullLen-self.currentStep
		if current:
			cr=self.currentStep
			if current<=self.step :
				self.currentStep=self.fullLen
			else:
				self.currentStep+=self.step
			return self.string[cr:self.currentStep]
		else:
			raise StopIteration 
