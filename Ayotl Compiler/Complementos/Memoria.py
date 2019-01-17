from .SegmentoMemoria import SegmentoMemoria

class Memoria():

	def __init__(self):
		self.memoriaGlobal = SegmentoMemoria('Global',0,4000)
		self.memoriaLocal = SegmentoMemoria('Local',5000,4000)
		self.memoriaTemp = SegmentoMemoria('Temp',10000,4000)
		self.memoriaConst = SegmentoMemoria('Const',15000,4000)


	def getGlobalAddress(self,TipoVar,Valor):
		return self.memoriaGlobal.CreateAddress('global',TipoVar,Valor)

	def getLocalAddress(self,TipoVar,Valor):
		return self.memoriaLocal.CreateAddress('local',TipoVar,Valor)

	def getTemporalAddress(self,TipoVar,Valor):
		return self.memoriaTemp.CreateAddress('temp',TipoVar,Valor)

	def getConstantAddress(self,TipoVar,Valor):
		return self.memoriaConst.CreateAddress('const',TipoVar,Valor)