from .Memoria import Memoria

class TablaVariables():

	def __init__(self,sc):
		self.tabla_variables = {}
		self.tabla_busqueda = {}
		self.lista_nombresINT = []
		self.lista_nombresFLOAT = []
		self.Scope = sc
		self.MemoriaRelativa = []
		self.cantINT=0
		self.cantFLOAT=0
		self.Gi = 0
		self.Gf = 2001
		self.Li = 5000
		self.Lf = 7001
		self.Ti = 10000
		self.Tf = 12001
		self.Ci = 15000
		self.Cf = 17001

	#   addVar(tipoVar,Nomvar,dim1,dim2)
	def addVar(self,TipoVar,NomVar,*dims):
		
		DirMemVar=0
		R=0
		S=0
		S1=0
		dim1=0
		dim2=0

		if not dims: #Si la lista esta vacia, es una var regular (no dimensionada)


			if self.Scope == 'global' and TipoVar == 'INT':
				DirMemVar += self.Gi
				self.Gi += 1
				self.cantINT += 1
			elif self.Scope == 'global' and TipoVar == 'FLOAT':
				DirMemVar = self.Gf
				self.Gf += 1
				self.cantFLOAT += 1
			elif self.Scope == 'local' and TipoVar == 'INT':
				DirMemVar = self.Li
				self.Li += 1
				self.cantINT += 1
			elif self.Scope == 'local' and TipoVar == 'FLOAT':
				DirMemVar = self.Lf
				self.Lf += 1
				self.cantFLOAT += 1			
			elif self.Scope == 'temp' and TipoVar == 'INT':
				DirMemVar = self.Ti
				self.cantINT += 1
				self.Ti += 1	
			elif self.Scope == 'temp' and TipoVar == 'FLOAT':
				DirMemVar = self.Tf
				self.Tf += 1	
				self.cantFLOAT += 1
			elif self.Scope == 'const' and TipoVar == 'INT':
				DirMemVar = self.Ci
				self.Ci += 1
				self.cantINT += 1
			else: 
				None
			  
			if self.Scope == 'const' and TipoVar == 'FLOAT':
				DirMemVar = self.Cf
				self.Cf += 1
				self.cantFLOAT += 1
		else:
			if len(dims) == 1: #Si la longitud de la dimension es 1, entonces es una lista
			 	if self.Scope == 'global' and TipoVar == 'INT':
						DirMemVar = self.Gi
						dim1 = dims[0]
						self.Gi += dims[0]
						self.cantINT += dims[0]
			 	if self.Scope == 'global' and TipoVar == 'FLOAT':
						DirMemVar = self.Gf
						dim1 = dims[0]
						self.Gf += dims[0]
						self.cantFLOAT += dims[0]
			 	if self.Scope == 'local' and TipoVar == 'INT':
						DirMemVar = self.Li
						dim1 = dims[0]
						self.Li += dims[0]
						self.cantINT += dims[0]
			 	if self.Scope == 'local' and TipoVar == 'FLOAT':
						DirMemVar = self.Lf
						dim1 = dims[0]
						self.Lf += dims[0]
						self.cantFLOAT += dims[0]
			 	if self.Scope == 'temp' and TipoVar == 'INT':
						DirMemVar = self.Ti
						dim1 = dims[0]
						self.Ti += dims[0]
						self.cantINT += dims[0]
			 	if self.Scope == 'temp' and TipoVar == 'FLOAT':
						DirMemVar = self.Tf
						dim1 = dims[0]
						self.Tf += dims[0]
						self.cantFLOAT += dims[0]
			 	if self.Scope == 'const' and TipoVar == 'INT':
						DirMemVar = self.Ci
						dim1 = dims[0]
						self.Ci += dims[0]
						self.cantINT += dims[0]
			 	if self.Scope == 'const' and TipoVar == 'FLOAT':
						DirMemVar = self.Cf
						dim1 = dims[0]
						self.Cf += dims[0]
						self.cantFLOAT += dims[0]
			if len(dims) == 2:
				if self.Scope == 'global' and TipoVar == 'INT':
						R = dims[0] * dims[1]
						S1 = (R / dims[0]) # osea dims[1]
						dim1 = dims[0]
						dim2 = dims[1]
						R = dims[0] * dims[1]
						S1 = (R / dims[0]) # osea dims[1]
						dim1 = dims[0]
						dim2 = dims[1]
						DirMemVar = self.Gi
						self.Gi += dims[0] * dims[1]
						self.cantINT += dims[0] * dims[1]					
				if self.Scope == 'global' and TipoVar == 'FLOAT':
						R = dims[0] * dims[1]
						S1 = (R / dims[0]) # osea dims[1]
						dim1 = dims[0]
						dim2 = dims[1]
						DirMemVar = self.Gf
						self.Gf += dims[0] * dims[1]
						self.cantFLOAT += dims[0] * dims[1]	
				if self.Scope == 'local' and TipoVar == 'INT':
						R = dims[0] * dims[1]
						S1 = (R / dims[0]) # osea dims[1]
						dim1 = dims[0]
						dim2 = dims[1]
						DirMemVar = self.Li
						self.Li += dims[0] * dims[1]
						self.cantINT += dims[0] * dims[1]	
				if self.Scope == 'local' and TipoVar == 'FLOAT':
						R = dims[0] * dims[1]
						S1 = (R / dims[0]) # osea dims[1]
						dim1 = dims[0]
						dim2 = dims[1]
						DirMemVar = self.Lf
						self.Lf += dims[0] * dims[1]
						self.cantFLOAT += dims[0] * dims[1]	
				if self.Scope == 'temp' and TipoVar == 'INT':
						R = dims[0] * dims[1]
						S1 = (R / dims[0]) # osea dims[1]
						dim1 = dims[0]
						dim2 = dims[1]
						DirMemVar = self.Ti
						self.Ti += dims[0] * dims[1]
						self.cantINT += dims[0] * dims[1]	
				if self.Scope == 'temp' and TipoVar == 'FLOAT':
						R = dims[0] * dims[1]
						S1 = (R / dims[0]) # osea dims[1]
						dim1 = dims[0]
						dim2 = dims[1]
						DirMemVar = self.Tf
						self.Tf += dims[0] * dims[1]
						self.cantFLOAT += dims[0] * dims[1]	
				if self.Scope == 'const' and TipoVar == 'INT':
						R = dims[0] * dims[1]
						S1 = (R / dims[0]) # osea dims[1]
						dim1 = dims[0]
						dim2 = dims[1]
						DirMemVar = self.Ci
						self.Ci += dims[0] * dims[1]
						self.cantINT += dims[0] * dims[1]	
				if self.Scope == 'const' and TipoVar == 'FLOAT':
						R = dims[0] * dims[1]
						S1 = (R / dims[0]) # osea dims[1]
						dim1 = dims[0]
						dim2 = dims[1]
						DirMemVar = self.Cf
						self.Cf += dims[0] * dims[1]
						self.cantFLOAT += dims[0] * dims[1]	

		self.tabla_variables[NomVar] = {
			'nombre' : NomVar,
			'tipo' : TipoVar,
			'dirMem' : DirMemVar,
			's1' : S1,	
			'lSdim1' : dim1,
			'lSdim2' : dim2

		}
		self.tabla_busqueda[DirMemVar] = {
			'nombre' : NomVar
		}
		
		if TipoVar == "INT":
			self.lista_nombresINT += [NomVar]
		else:
			self.lista_nombresFLOAT += [NomVar]

	def  eraseAll(self):
		self.tabla_variables.clear()
		self.MemoriaRelativa = []
		self.cantINT=0
		self.cantFLOAT=0
		self.Gi = 0
		self.Gf = 2001
		self.Li = 5000
		self.Lf = 7001
		self.Ti = 10000
		self.Tf = 12001
		self.Ci = 15000
		self.Cf = 17001

	
	def existsVar(self,NomVar):
		if NomVar in self.tabla_variables.keys():
			return True
		else:
			return False

	def getVar(self,NomVar):
		if existsVar(NomVar):
			return self.tabla_variables[NomVar]
		else:
			print("Error: No existe la variable")
			return None

	def getDireccionMem(self,NomVar):
		return self.tabla_variables[NomVar]['dirMem']

	def printTabladeVariables(self):
		print("*" * 20)
		for x in self.tabla_variables:
    			print (x)
    			for y in self.tabla_variables[x]:
        				print (y,':',self.tabla_variables[x][y])

	def getType(self,NomVar):
		if(self.existsVar(NomVar)):
			return self.tabla_variables[NomVar]['tipo']
		else:
			return False

	def getSizeInt(self):
		return self.cantINT

	def getSizeFloat(self):
		return self.cantFLOAT


	def getS1(self,Nomvar):
		return self.tabla_variables[Nomvar]['s1']

	def getNameVar(self,currentAddress):
		return self.tabla_busqueda[currentAddress]['nombre']

	def getLsDim1(self,Nomvar):
		return self.tabla_variables[Nomvar]['lSdim1']

	def getLsDim2(self,Nomvar):
		return self.tabla_variables[Nomvar]['lSdim2']


	def getNamesINT(self):
		return self.lista_nombresINT

	def getNamesFLOAT(self):
		return self.lista_nombresFLOAT



	

