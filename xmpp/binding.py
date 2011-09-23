#coding:utf-8

__all__=('bind_Objects','bindOutgoingStream','bindIncomincStream','binding_up','IN','OUT')

IN=0x1
OUT=0x2

BINDINGS={IN:[],OUT:[]}
BIND_OBJ={}


def _searhBindInstance(instance):
	for ins1,ins2 in BIND_OBJ.items():
		if ins1.__dict__[instance.__class__.__name__]==instance:
			return ins2
	return None

def _callBind(self,type,rawdata):
	instance=_searhBindInstance(self)
	if instance:
		for x in BINDINGS[type]:
			x(instance,rawdata)

def bindObjects(instance1,instance2):
	BIND_OBJ.update({instance1:instance2})
	
def unbindObjects(inst):
	if inst in BIND_OBJ:
		del BIND_OBJ[inst]
	
def bindIncomincStream(func):
	BINDINGS[0x1].append(func)
	return func
def bindOutgoingStream(func):
	BINDINGS[0x2].append(func)

def bindingUp(type):
	def wrapper(func):
		if type==IN:
			def receive(self):
				data=func(self)
				_callBind(self,type,data)
				return data
			return receive
		elif type==OUT:
			def send(self,rawdata):
				func(self,rawdata)
				_callBind(self,type,rawdata)
			return send
		else:
			return func
	return wrapper
				
		
