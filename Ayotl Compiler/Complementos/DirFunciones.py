class DirFunciones():

	def __init__(self):
			self.dirFunciones = {}
			self.contINT = 0
			self.contFLOAT = 0
			self.tamINTLocales = 0
			self.tamFLOATLocales = 0
			self.sizeIntTemp = 0
			self.sizeFloatTemp = 0
			self.dirActualINT = 5000
			self.dirActualFLOAT = 7001

	def addFn(self,TipoFn,NombreFn):
		self.dirFunciones[NombreFn] = {

			'nombre' : NombreFn,
			'tipo' : TipoFn,
			'direccionDeInicio' : 0,
			'CantdeVar' : {
				'int' : 0,
				'float' : 0
			}, 
			'parametrosAdresses' : [],
			'parametrosTypes' : [],
			 'localSizeINT' : 0,
			 'localSizeFLOAT' : 0,
			 'tempSizeINT' : 0,
			 'tempSizeFLOAT' : 0
		}

	def existFn(self,NombreFun):
		if NombreFun in self.dirFunciones.keys():
			return True
		else:
			return False

	def getNameFn(self,nombreFun):
		if existeFun(nombreFun):
			return self.dirFunciones[nombreFun]
		else:
			print("Error: No existe la función con ese nombre")
			return None

	def addParamFn(self, nombreFn,Tipo):
		if  Tipo == 'int':
			self.contINT = self.contINT + 1
			self.dirFunciones[nombreFn]['CantdeVar']['int'] = self.contINT
			self.dirFunciones[nombreFn]['parametrosAdresses'] = self.dirFunciones[nombreFn]['parametrosAdresses'] + [self.dirActualINT]
			self.dirFunciones[nombreFn]['parametrosTypes'] = self.dirFunciones[nombreFn]['parametrosTypes'] + ["INT"]
			self.dirActualINT = self.dirActualINT + 1
		else:
			self.contFLOAT = self.contFLOAT + 1
			self.dirFunciones[nombreFn]['CantdeVar']['int'] = self.contFLOAT
			self.dirFunciones[nombreFn]['parametrosAdresses'] = self.dirFunciones[nombreFn]['parametrosAdresses'] + [self.dirActualFLOAT]
			self.dirFunciones[nombreFn]['parametrosTypes'] = self.dirFunciones[nombreFn]['parametrosTypes'] + ["FLOAT"]
			self.dirActualFLOAT = self.dirActualFLOAT + 1

	def setDireccionInicio(self,nombreFn,DirInicio):
		self.dirFunciones[nombreFn]['direccionDeInicio'] = DirInicio

	def getDireccionInicio(self, nombreFn):
		return self.dirFunciones[nombreFn]['direccionDeInicio']

	def verificaParam(self,nombreFn,ListaPar):
		if set(self.dirFunciones[nombreFn]['parametrosTypes']) == set(ListaPar):
			return True
		else:
			return False

	def setSizeLocalsINT(self,nombreFn,Size):
		self.dirFunciones[nombreFn]['localSizeINT'] = Size

	def setSizeLocalsFLOAT(self,nombreFn,Size):
		self.dirFunciones[nombreFn]['localSizeFLOAT'] = Size
	
	def setSizeTempsINT(self,nombreFn,Size):
		self.dirFunciones[nombreFn]['tempSizeINT'] = Size

	def setSizeTempsFLOAT(self,nombreFn,Size):
		self.dirFunciones[nombreFn]['tempSizeINT'] = Size

	def getSizeLocalsINT(self,nombreFn):
		return self.dirFunciones[nombreFn]['localSizeINT']

	def getSizeLocalsFLOAT(self,nombreFn):
		return self.dirFunciones[nombreFn]['localSizeFLOAT']

	def getSizeTempsINT(self,nombreFn):
		return self.dirFunciones[nombreFn]['tempSizeINT']

	def getSizeTempsFLOAT(self,nombreFn):
		return self.dirFunciones[nombreFn]['tempSizeFLOAT']

	def getParametersAddresses(self,nombreFn):
		return self.dirFunciones[nombreFn]['parametrosAdresses']

	def getParametersTypes(self,nombreFn):
		return self.dirFunciones[nombreFn]['parametrosTypes']

	def getFnType(self,nombreFn):
		return self.dirFunciones[nombreFn]['tipo']