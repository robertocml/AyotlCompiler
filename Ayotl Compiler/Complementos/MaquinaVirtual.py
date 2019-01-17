from Complementos.DirFunciones import DirFunciones

class MaquinaVirtual():

	def __init__(self,quadsP,lisConstInt,lisConstFloat,sizeIntGl,sizeFlGl,sizeIntLoc,sizeFlLoc,sizeIntTemp,sizeFlTemp):		
		global dirFunciones
		self.memGlobalInt=[0]*sizeIntGl
		self.memGlobalFloat=[0]*sizeFlGl
		
		self.memLocalInt=[0]*sizeIntLoc
		self.memLocalFloat=[0]*sizeFlLoc
		
		self.memTempInt=[0]*sizeIntTemp
		self.memTempFloat=[0]*sizeFlTemp
		
		self.memConstInt=lisConstInt
		self.memConstFloat=lisConstFloat

		self.quads=quadsP



		self.pBaseLocalInt=[]
		self.pBaseLocalFloat=[]
		self.pBaseTempInt=[]
		self.pBaseTempFloat=[]
		self.pBaseLocalInt.append(0)
		self.pBaseLocalFloat.append(0)
		self.pBaseTempInt.append(0)
		self.pBaseTempFloat.append(0)


		self.pLimLocalInt=[]
		self.pLimLocalFloat=[]
		self.pLimTempInt=[]
		self.pLimTempFloat=[]
		self.pLimLocalInt.append(sizeIntLoc-1)
		self.pLimLocalFloat.append(sizeFlLoc-1)
		self.pLimTempInt.append(sizeIntTemp-1)
		self.pLimTempFloat.append(sizeFlTemp-1)


		



		#self.dirFunciones=dirFunciones


	def getValue(self,dir):

		if(type(dir)==list):
			if(dir[0]>=10000 and dir[0]<=12000):
				return(getValue(self.memTempInt[self.pBaseTempInt[len(self.pBaseTempInt)-1]+dir-10000])) 
			elif(dir[0]>=12001 and dir[0]<=14000):
				return(getValue(self.memTempFloat[pBaseTempFloat[len(pBaseTempFloat)-1]+dir-12001])) 


		if(dir<=2000):
			return(self.memGlobalInt[dir-2000]) 
		elif(dir>=2001 and dir<=4000):
			return(self.memGlobalFloat[dir-2001]) 
		elif(dir>=5000 and dir<=7000):
			return(self.memLocalInt[pBaseLocalInt[len(pBaseLocalInt)-1] +dir-5000]) 
		elif(dir>=7001 and dir<=9000):
			return(self.memLocalFloat[pBaseLocalFloat[len(pBaseLocalFloat)-1]+dir-7001]) 
		elif(dir>=10000 and dir<=12000):
			return(self.memTempInt[self.pBaseTempInt[len(self.pBaseTempInt)-1]+dir-10000]) 
		elif(dir>=12001 and dir<=14000):
			return(self.memTempFloat[pBaseTempFloat[len(pBaseTempFloat)-1]+dir-12001]) 
		elif(dir>=15000 and dir<=17000):
			return(self.memConstInt[dir-15000]) 
		elif(dir>=17001 and dir<=19000):
			return(self.memConstFloat[dir-17001]) 
		else:
			print('ERROR EJECUCION EN DIRECCION' + dir)


	def setValue(self,dir,val):
		if(type(dir)==list):
			if(dir[0]>=10000 and dir[0]<=12000):
				setValue(getValue(self.memTempInt[self.pBaseTempInt[len(self.pBaseTempInt)-1]+dir-10000]),val) 
			elif(dir[0]>=12001 and dir[0]<=14000):
				setValue(getValue(self.memTempFloat[pBaseTempFloat[len(pBaseTempFloat)-1]+dir-12001]),val) 


		if(dir<=2000):
			self.memGlobalInt[dir]=val 
		elif(dir>=2001 and dir<=4000):
			self.memGlobalFloat[dir-2001]=val 
		elif(dir>=5000 and dir<=7000):
			self.memLocalInt[pBaseLocalInt[len(pBaseLocalInt)-1] +dir-5000]=val 
		elif(dir>=7001 and dir<=9000):
			self.memLocalFloat[pBaseLocalFloat[len(pBaseLocalFloat)-1]+dir-7001]=val 
		elif(dir>=10000 and dir<=12000):
			self.memTempInt[self.pBaseTempInt[len(self.pBaseTempInt)-1]+dir-10000]=val 
		elif(dir>=12001 and dir<=14000):
			self.memTempFloat[pBaseTempFloat[len(pBaseTempFloat)-1]+dir-12001]=val 
		elif(dir>=15000 and dir<=17000):
			self.memConstInt[dir-15000]=val 
		elif(dir>=17001 and dir<=19000):
			self.memConstFloat[dir-17001]=val 
		else:
			print('ERROR EJECUCION EN DIRECCION' + dir)



	def run(self):
		insPointer=0
		pilaPointers=[]
		nameFuncAux=''
		baseTempPointer=0
		while(self.quads[insPointer]!=('end',1)):
			if(self.quads[insPointer][0]=='+'):
				val = self.getValue(self.quads[insPointer][1]) + self.getValue(self.quads[insPointer][2])
				self.setValue(self.quads[insPointer][3],val)
			
			elif(self.quads[insPointer][0]=='-'):
				val = self.getValue(self.quads[insPointer][1]) - self.getValue(self.quads[insPointer][2])
				self.setValue(self.quads[insPointer][3],val)
			
			elif(self.quads[insPointer][0]=='*'):
				val = self.getValue(self.quads[insPointer][1]) * self.getValue(self.quads[insPointer][2])
				self.setValue(self.quads[insPointer][3],val)
			
			elif(self.quads[insPointer][0]=='/'):
				val = self.getValue(self.quads[insPointer][1]) / self.getValue(self.quads[insPointer][2])
				self.setValue(self.quads[insPointer][3],val)
			
			elif(self.quads[insPointer][0]=='>'):
				if(self.getValue(self.quads[insPointer][1]) > self.getValue(self.quads[insPointer][2])):
					self.setValue(self.quads[insPointer][3],1)
				else:
					self.setValue(self.quads[insPointer][3],0)
			
			elif(self.quads[insPointer][0]=='<'):
				if(self.getValue(self.quads[insPointer][1]) < self.getValue(self.quads[insPointer][2])):
					self.setValue(self.quads[insPointer][3],1)
				else:
					self.setValue(self.quads[insPointer][3],0)
			
			elif(self.quads[insPointer][0]=='=='):
				if(self.getValue(self.quads[insPointer][1]) == self.getValue(self.quads[insPointer][2])):
					self.setValue(self.quads[insPointer][3],1)
				else:
					self.setValue(self.quads[insPointer][3],0)
			
			elif(self.quads[insPointer][0]=='!='):
				if(self.getValue(self.quads[insPointer][1]) > self.getValue(self.quads[insPointer][2])):
					self.setValue(self.quads[insPointer][3],1)
				else:
					self.setValue(self.quads[insPointer][3],0)
			elif(self.quads[insPointer][0]=='&&'):
				if(self.getValue(self.quads[insPointer][1]) and self.getValue(self.quads[insPointer][2])):
					self.setValue(self.quads[insPointer][3],1)
				else:
					self.setValue(self.quads[insPointer][3],0)

			elif(self.quads[insPointer][0]=='||'):
				if(self.getValue(self.quads[insPointer][1]) or self.getValue(self.quads[insPointer][2])):
					self.setValue(self.quads[insPointer][3],1)
				else:
					self.setValue(self.quads[insPointer][3],0)
			
			elif(self.quads[insPointer][0]=='='):
				self.setValue(self.quads[insPointer][2], self.getValue(self.quads[insPointer][1]))
			
			elif(self.quads[insPointer][0]=='goto'):
				insPointer = self.quads[insPointer][1] - 1
			
			elif(self.quads[insPointer][0]=='gotoF'):
				if(self.quads[insPointer][1] == 0):
					insPointer = self.quads[insPointer][3] - 1
			
			elif(self.quads[insPointer][0]=='endproc'):
				if(self.quads[insPointer][1]=='void'):
					del(self.memLocalInt[self.pBaseLocalInt.pop():len(memLocalInt)])
					del(self.memLocalFloat[self.pBaseLocalFloat.pop():len()])
					
					del(self.memTempInt[self.pBaseTempInt.pop():len()])
					del(self.memTempFloat[self.pBaseTempFloat.pop():len()])


					self.pLimLocalInt.pop()
					self.pLimLocalFloat.pop()
					self.pLimTempInt.pop()
					self.pLimTempFloat.pop()

					insPointer=pilaPointers.pop()
					insPointer=insPointer-1

				else:
					val=self.getValue(self.quads[insPointer][1])
					del(self.memLocalInt[self.pBaseLocalInt.pop():len(memLocalInt)])
					del(self.memLocalFloat[self.pBaseLocalFloat.pop():len()])
					
					del(self.memTempInt[self.pBaseTempInt.pop():len()])
					del(self.memTempFloat[self.pBaseTempFloat.pop():len()])

					self.pLimLocalInt.pop()
					self.pLimLocalFloat.pop()
					self.pLimTempInt.pop()
					self.pLimTempFloat.pop()

					insPointer=pilaPointers.pop()
					insPointer+=1
					self.setValue(self.quads[insPointer][2],val)



			elif(self.quads[insPointer][0]=='era'):
				nameFuncAux=self.quads[insPointer][1]
				auxSLI=dirFunciones.getSizeLocalsINT(self.quads[insPointer][1])
				auxSLF=dirFunciones.getSizeLocalsFLOAT(self.quads[insPointer][1])
				auxSTI=dirFunciones.getSizeTempsINT(self.quads[insPointer][1])
				auxSTF=dirFunciones.getSizeTempsFLOAT(self.quads[insPointer][1])

				self.memLocalInt+=[0]*auxSLI
				self.memLocalFloat+=[0]*auxSLF
				
				self.memTempInt+=[0]*auxSTI
				self.memTempFloat+=[0]*auxSTF
				#Creo la nueva memoria 


				self.pBaseLocalInt.append(pLimLocalInt[len(pLimLocalInt)-1]+1)
				self.pBaseLocalFloat.append(pLimLocalFloat[len(pLimLocalInt)-1]+1)
				self.pBaseTempInt.append(pLimTempInt[len(pLimLocalInt)-1]+1)
				self.pBaseTempFloat.append(pLimTempFloat[len(pLimLocalInt)-1]+1)

				self.pLimLocalInt.append(pLimLocalInt[len(pLimLocalInt)-1]+auxSLI)
				self.pLimLocalFloat.append(pLimLocalFloat[len(pLimLocalInt)-1]+auxSLF)
				self.pLimTempInt.append(pLimTempInt[len(pLimLocalInt)-1]+auxSTI)
				self.pLimTempFloat.append(pLimTempFloat[len(pLimLocalInt)-1]+auxSTF)
				#inicialice nuevos apuntadores de limites

			elif(self.quads[insPointer][0]=='param'):#siempre tiene 3 parametros				
				bli=self.pBaseLocalInt.pop()
				blf=self.pBaseLocalFloat.pop()
				bti=self.pBaseTempInt.pop()
				btf=self.pBaseTempFloat.pop()

				val=self.getValue(self.quads[insPointer][1])

				self.pBaseLocalInt.append(bli)
				self.pBaseLocalFloat.append(blf)
				self.pBaseTempInt.append(bti)
				self.pBaseTempFloat.append(btf)

				lisParam=dirFunciones.getParametersAddresses(nameFuncAux)
				self.setValue(lisParam[self.quads[insPointer][2]],val)

			elif(self.quads[insPointer][0]=='gosub'):
				pilaPointers.append(insPointer)
				insPointer=self.quads[insPointer][1]-1

			elif(self.quads[insPointer][0]=='ver'):
				if(not (self.getValue(self.quads[insPointer][1])>=self.quads[insPointer][2] and self.getValue(self.quads[insPointer][1])<=self.quads[insPointer][3])):
					print('Error pusiste un indice fuera de rango')

			elif(self.quads[insPointer][0]=='print'):
				print(self.getValue(self.quads[insPointer][1]))
			elif(self.quads[insPointer][0]=='read'):
				val=input('')
				self.setValue(self.getValue(self.quads[insPointer][1]),val)



			insPointer+=1


	

