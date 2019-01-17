class Cuadruplos():

	def __init__(self):
		self.Cuadruplos = []
		self.ContCuads = 0
		

	def añadeCuadruplo(self,Oper,OperIzq,OperDer,Res):
		self.Cuadruplos = self.Cuadruplos + [(Oper,OperIzq,OperDer,Res)]
		#self.ContCuads = self.ContCuads+1

	def rellenaCuadruplo(self,temp,uno,dos,tres):
		self.Cuadruplos.insert(temp,(uno,dos,tres,""))
		#self.ContCuads = self.ContCuads+1
		

	def imprimeCuadruplos(self):
		for a,b,c,d in self.Cuadruplos:  # <-- this unpacks the tuple like a, b = (0, 1)
    			print(a,b,c,d)

	def Cuadruploslen(self):
		return len(self.Cuadruplos)

	def Cuadruplosdelete(self,temp):
		del self.Cuadruplos[temp]
    
	def Cuadruplosindex(self,temp,n):
		return self.Cuadruplos[temp][n]

"""	def enumeraCuadruplos(self):
		x=10
		for n in range(0,len(self.Cuadruplos)):
			t = tuple(str(x))
			tup = ''.join(t)
			tups = tuple(str(tup))
			self.Cuadruplos[n] = self.Cuadruplos[n] + tups
			#print(str(self.Cuadruplos[n]))
			#x = x+1;
			#print(tups)"""