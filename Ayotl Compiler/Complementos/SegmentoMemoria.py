class SegmentoMemoria():

	def __init(self,Scope,DirInicio,CantDir):
		base = 0	
		self.DirInicio = DirInicio
		self.Scope = Scope
		self.CantDir = CantDir 
		self.Memoria = []

		self.DirInicio_Int = DirInicio
		self.DirFinal_Int = DirInicio + CantDir/2
		
		self.DirInicio_Float = DirFinal_Int + 1
		self.DirFinal_Float = DirInicio_Float + CantDir/2



	def CreateAddress(self,Scope,TipoVar,Valor):
		if(Scope =='global'):
			if(TipoVar == 'Int'):
				dirMem = Memoria[DirInicio_Int] + base
				Memoria[dirMem] = Valor
				base += 1
			if(TipoVar == "Float"):
				dirMem = Memoria[DirInicio_Float] + base
				base += 1

		if(Scope =='local'):
			if(TipoVar == 'Int'):
				dirMem = Memoria[DirInicio_Int] + base
				Memoria[dirMem] = Valor
				base += 1
			if(TipoVar == "Float"):
				dirMem = Memoria[DirInicio_Float] + base
				base += 1

		if(Scope =='temp'):
			if(TipoVar == 'Int'):
				dirMem = Memoria[DirInicio_Int] + base
				Memoria[dirMem] = Valor
				base += 1
			if(TipoVar == "Float"):
				dirMem = Memoria[DirInicio_Float] + base
				base += 1
		if(Scope =='const'):
			if(TipoVar == 'Int'):
				dirMem = Memoria[DirInicio_Int] + base
				Memoria[dirMem] = Valor
				base += 1
			if(TipoVar == "Float"):
				dirMem = Memoria[DirInicio_Float] + base
				base += 1
		
		

		def getValue(self,dirMem):
			return self.Memoria[dirMem]