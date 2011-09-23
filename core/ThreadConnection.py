#coding: utf-8
from __main__ import printf,FLAG_ERROR,FLAG_INFO,FLAG_WARNING,FLAG_SUCESS
from PyQt4.QtCore import QThread,QRegExp,QObject,pyqtSignal,pyqtSlot
from xmpp import client
from xmpp import protocol
from xmpp.binding import bindIncomincStream,bindOutgoingStream
import traceback

__all__=['ThreadConnection','ERROR_STREAM']

ERROR_STREAM={
	0x1:'Error connection',
	0x2:'Authentification error',
	0x3:'Resources conflict',
	0x4:'System shutdown',
	0xF:'Exception in connection thread'
}

class ThreadConnection(QThread):
	disconnected     = pyqtSignal()
	connected        = pyqtSignal()
	stageConnection  = pyqtSignal(int)
	profileView      = pyqtSignal(str,dict)
	recivingMsgInTet = pyqtSignal(str,tuple,dict,'QString')
	streamOut        = pyqtSignal("QString")
	streamIn         = pyqtSignal("QString")
	streamError      = pyqtSignal(int)
	def __init__(self,config,parent=None):
		QThread.__init__(self,parent)
		self.XMPP = None
		self.setTerminationEnabled(True)
		self._config = config
		self.jid = self._config.user()+'@'+self.host
	@bindIncomincStream
	def __onStreamIN(self,data):
		self.streamIn.emit(self.trUtf8(data))
	@bindOutgoingStream
	def __onStreamOUT(self,data):
		self.streamOut.emit(self.trUtf8(data))
	def run(self):
		printf('Starting connertion thred of %s'%str(self))
		self.setPriority(self.HighestPriority)
		if self._connection():
			printf('Connection established',FLAG_SUCESS)
			self._RegisterHandlers()
			self.connected.emit()
			try:
				while self.XMPP.process(5):
					pass
				self.disconnected.emit()
				printf('Disconnected')
			except protocol.Conflict:
				self.streamError.emit(0x3)
				printf('Resources conflict',FLAG_WARNING)
			except protocol.SystemShutdown:
				printf('The remote server shutdown',FLAG_WARNING)
				self.streamError.emit(0x4)
			except protocol.StreamError,e:
				self.dropConnection()
				printf('Exception of stream %s'%str(e),FLAG_ERROR)
			except Exception:
				self.streamError.emit(0xF)
				printf('Exception in Thread: %s traceback : %s '%(str(self),traceback.format_exc()),FLAG_ERROR)
		printf('Thread is terminating')
	def _connection(self):
		self.stage.emit(1)
		printf('Connection established',FLAG_SUCESS)
		self.XMPP=client.Client(self._config.host(),self._config.port(),bind=self)
		if not self.XMPP.connect(self._config.ssl(),self._config.resolver()):
			self.streamError.emit(0x1)
			printf("Connection isn't possible",FLAG_WARNING)
			return False
		printf("Connection is established",FLAG_SUCESS)
		self.stage.emit(2)
		if not self.XMPP.auth(self._config.user(),self._config.password(),self._config.resource()):
			self.streamError.emit(0x2)
			printf("Authentification error",FLAG_WARNING)
			return False
		printf("Authentification is successful",FLAG_SUCESS)
		self.stage.emit(3)
		self.XMPP.setStatus(None, None,self._config.priority())
		printf('Set status and priority %d'%self._config.priority())
		return True
	def disconnect(self):
		if self.isConnected():
			self.XMPP.disconnected()
	def __RegisterHandlers(self):
		printf('Registry handlers')
		self.XMPP.registerHandler("iq",self.__Iq)
		self.XMPP.registerHandler("message",self.__Message)
		#self.XMPP.registerSendStreamHandler(self.printf)
		#self.XMPP.registerListenStreamHandler(self.printf)
	def __Iq(self,stanza):
		fulljid = stanza.getFrom()
		if fulljid is None : return
		if stanza.getType()==protocol.TYPE_GET:
			if stanza.getTags("ping", {}, protocol.NS_PING):
				iq = stanza.buildReply(protocol.TYPE_RESULT)
			else:
				iq = stanza.buildReply(protocol.TYPE_ERROR)
				error = iq.addChild("error", {"type": "cancel"})
				error.addChild("feature-not-implemented", {}, [], protocol.NS_STANZAS)
			self.send(iq)
	def __Message(self,stanza):
		if stanza.getTags("event",{},"askseelove:event:profileview") and stanza.getType() != protocol.TYPE_ERROR:
			attrs = stanza.getTag('event').getTag('User').getAttrs()
			if attrs:
				self.view.emit(stanza.getFrom().__str__(),attrs)
			reply=protocol.Message(stanza.getFrom())
			reply.setTag("event",namespace="askseelove:event:online")
			self.send(reply)
			return
		elif stanza.getTags("poke",{},"askseelove:event:poke"):
			poke=stanza.getTag("poke")
			msgAttrs=poke.getTag('User').getAttrs()
			if not msgAttrs :
				return
			msgFrom=stanza.getFrom().__str__()
			msgType=stanza.getType(),stanza.getErrorCode()
			msgBody=poke.getAttr("msg")
			self.tetMsg.emit(msgFrom,msgType,msgAttrs,self.trUtf8(msgBody))
	def sendMsgToTet(self,to,color,male,sid,name,body):
		msg=protocol.Message(to)
		poke=msg.setTag('poke',{'xmlns':'askseelove:event:poke','msg':body})
		poke.setTag('User',{'name':name,'color':color,'male':male,'id':sid})
		self.send(msg)
	def CallProfile(self,id,instance,args=[]):
		iq=protocol.Iq(protocol.TYPE_GET,to='profile1.%s'%self.host)
		query = iq.setTag('query',{'full':'1','xmlns':'askseelove:iq:profile'})
		query.setTag('User',{'id':(id.split('@')[0] if QRegExp('\w+@[\w+.]*\.\w+').exactMatch(id) else id)})
		self.sendAndCallForResponse(iq,instance,args)
	def SetProfileSettings(self,profileData,instance,args=[]):
		iq=protocol.Iq(protocol.TYPE_SET,to='profile1.%s'%self.host)
		query=iq.setTag('query',namespace='askseelove:iq:profile')
		query.setTag('User',profileData)
		self.sendAndCallForResponse(iq,instance,args)
	def Ping(self,jid,instance):
		iq = protocol.Iq(protocol.TYPE_GET,to=jid)
		iq.setTag('ping',namespace=protocol.NS_PING)
		self.sendAndCallForResponse(iq,instance)
	def sendAndCallForResponse(self,iq,instance,args=None):
		class SubSignal(QObject):
			response=pyqtSignal(tuple)
			def __init__(self):
				QObject.__init__(self,parent=None)
				self.response.connect(instance)
			def __call__(self,*args):
				self.response.emit(args)
				printf('Emit response iq of %s'%str(self))
		self.XMPP.sendAndCallForResponse(iq,SubSignal(),args)
	def send(self,node):
		self.XMPP.send(node)
	def isConnected(self):
		return self.XMPP.isConnected()
