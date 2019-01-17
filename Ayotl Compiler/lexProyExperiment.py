import ply.lex as lex
import ply.yacc as yacc
import sys
import os
import codecs
import re
from ply import *


reservadas = (
	'PROGRAM',
	'INT', 
	'FLOAT', 
	'IF', 
	'ELSE',
	'READ',
	'PRINT',
	'VOID',
	'RETURN',
	'FOR',
	'WHILE'

)

tokens = reservadas + (

	# ; { } , = ( ) [ ] 
	'SEMICOLON','L_BRACE', 'R_BRACE', 
	'COMMA', 'ASSIGN', 'L_PARENTHESIS','R_PARENTHESIS',
	'L_BRACKET','R_BRACKET',
	
	#operators + - * /
	'PLUS',	'MINUS', 'MULTIP', 'DIVIDE', 
	
	#bool > < != == && ||
	'GREATER_THAN', 'LESS_THAN', 'DIFF_THAN',
	'EQUALS_TO', 'AND', 'OR',

	#Constants
	'CONST_ID', 'CONST_INT', 'CONST_FLOAT'
)





t_ignore = ' \t\n'


#bool > < != == && ||
t_GREATER_THAN= r'\>' 
t_LESS_THAN= r'\<' 
t_DIFF_THAN= r'\!=' 
t_ASSIGN= r'='
t_EQUALS_TO=r'=='
t_AND=r'&&'
t_OR=r'\|\|'
#Operators + - * /
t_PLUS	= r'\+'
t_MINUS = r'\-'
t_MULTIP= r'\*'
t_DIVIDE= r'/'

# ;  { } , = ( ) [ ] 
t_SEMICOLON= r';'
t_L_BRACE= r'\{' 
t_R_BRACE= r'\}' 
t_COMMA= r','

t_L_BRACKET=r'\['
t_R_BRACKET=r'\]'
t_L_PARENTHESIS= r'\('
t_R_PARENTHESIS= r'\)'




def t_CONST_FLOAT(t):
	r'\d\.\d+'
	t.value = float(t.value)
	return t


def t_CONST_INT(t):
	r'\d+'
	t.value = int(t.value)
	return t



def t_CONST_ID(t):
	#r'[a-zA-Z_][a-zA-z0-9_]*'
	r'[A-Za-z_][\w_]*'
	if t.value.upper() in reservadas:
		t.value = t.value.upper()
		t.type = t.value
	return t

def t_COMMENT(t):
	r'\#.*'
	pass

def t_error(t):
	print("caracter ilegal '%s'" % t.value[0])
	t.lexer.skip(1)


lexer = lex.lex()

#lexer.input("1+2+-*=1.23{}[] > < != == && || ; : { } , = ( ) [ ] float 1.23 as1")

#while True:
#	tok = lexer.token()
#	if not tok:
#		break
#	print(tok)

#spaces on : and on | are SUPER IMPORTANT

precedence = (
#	('right','IF','WHILE'),
	('left','ASSIGN'),
#	('left','AND','OR'),
#	('left','GREATER_THAN','LESS_THAN','EQUALS_TO','DIFF_THAN'),
	('left','PLUS','MINUS'),
	('left','MULTIP','DIVIDE'),
	('left','L_PARENTHESIS','R_PARENTHESIS')
)

#from .TablaVariables import TablaVariables
#from .DirFunciones import DirFunciones
#from .CuboSemantico import CuboSemantico  

#from .Memoria import Memoria




class CuboSemantico():

	def __init__(self):
		self.cubo = {			

			'INT' : {

						'INT' : {

							'+' : 'INT',
							'-' : 'INT',
							'*' : 'INT',
							'/' : 'FLOAT',
							'>' : 'INT',
							'<' : 'INT',
							'!=': 'INT',
							'==':'INT',
							'&&': 'INT',
							'||': 'INT'
							},

						'FLOAT' : {

							'+' : 'FLOAT',
							'-' : 'FLOAT',
							'*' : 'FLOAT',
							'/' : 'FLOAT',
							'>' : 'INT',
							'<' : 'INT',
							'!=': 'INT',
							'==': 'INT',
							'&&': 'INT',
							'||': 'INT'
						}
			},

			'FLOAT' : {


						'INT' : {

							'+' : 'FLOAT',
							'-' : 'FLOAT',
							'*' : 'FLOAT',
							'/' : 'FLOAT',
							'>' : 'INT',
							'<' : 'INT',
							'!=': 'INT',
							'==': 'INT',
							'&&': 'INT',
							'||': 'INT'
							},

						'FLOAT' : {

							'+' : 'FLOAT',
							'-' : 'FLOAT',
							'*' : 'FLOAT',
							'/' : 'FLOAT',
							'>' : 'INT',
							'<' : 'INT',
							'!=': 'INT',
							'==': 'INT',
							'&&': 'INT',
							'||': 'INT'
						}
			}
		}


	def checkType(self,OperIzq, OperDer, Oper):
		return self.cubo[OperIzq][OperDer][Oper]
			



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

	def getTypeFn(self,nombreFn):
		return self.dirFunciones[nombreFn]['tipo']



#from Complementos.DirFunciones import DirFunciones

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


				self.pBaseLocalInt.append(self.pLimLocalInt[len(self.pLimLocalInt)-1]+1)
				self.pBaseLocalFloat.append(self.pLimLocalFloat[len(self.pLimLocalInt)-1]+1)
				self.pBaseTempInt.append(self.pLimTempInt[len(self.pLimLocalInt)-1]+1)
				self.pBaseTempFloat.append(self.pLimTempFloat[len(self.pLimLocalInt)-1]+1)

				self.pLimLocalInt.append(self.pLimLocalInt[len(self.pLimLocalInt)-1]+auxSLI)
				self.pLimLocalFloat.append(self.pLimLocalFloat[len(self.pLimLocalInt)-1]+auxSLF)
				self.pLimTempInt.append(self.pLimTempInt[len(self.pLimLocalInt)-1]+auxSTI)
				self.pLimTempFloat.append(self.pLimTempFloat[len(self.pLimLocalInt)-1]+auxSTF)
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


#TablaVariables varTable
quads=[]
dictVar={}
temp=["t1","t2","t3","t4","t5","t6","t7","t8","t9","t10","t11","t12","t13","t14","t15"]
n=0
pSaltos=[]
varContext=0 #0 es global  #1 es local 
tablaGlobal = TablaVariables('global')

tablaConst=TablaVariables('const')
tablaLocal=TablaVariables('local')
tablaTemp=TablaVariables('temp')
cubo=CuboSemantico()
#1 es local 
#2+ es de funcion especifica 
flagType=''
dirFunciones=DirFunciones()

flagTypeVars=''
tempCont=0;

def getTypeUniversal(dir):

	while(type(dir)==list):
		dir=dir[0]

	if(dir<=2000):
		return('INT') 
	elif(dir>=2001 and dir<=4000):
		return('FLOAT')
	elif(dir>=5000 and dir<=7000):
		return('INT') 
	elif(dir>=7001 and dir<=9000):
		return('FLOAT')
	elif(dir>=10000 and dir<=12000):
		return('INT')
	elif(dir>=12001 and dir<=14000):
		return('FLOAT')
	elif(dir>=15000 and dir<=17000):
		return('INT')
	elif(dir>=17001 and dir<=19000):
		return('FLOAT')
	else:
		print('ERROR TOTAL EN DIRECCIONES DE TIPOS')


def getVarContext(dir):

	while(type(dir)==list):
		dir=dir[0]

	if(dir<=2000):
		return('global') 
	elif(dir>=2001 and dir<=4000):
		return('global')
	elif(dir>=5000 and dir<=7000):
		return('local') 
	elif(dir>=7001 and dir<=9000):
		return('local')
	


	elif(dir>=10000 and dir<=12000):
		return('Error de compilador: El contexto esta equivocado')
	elif(dir>=12001 and dir<=14000):
		return('Error de compilador: El contexto esta equivocado')
	elif(dir>=15000 and dir<=17000):
		return('Error de compilador: El contexto esta equivocado')
	elif(dir>=17001 and dir<=19000):
		return('Error de compilador: El contexto esta equivocado')
	else:
		print('ERROR TOTAL EN DIRECCIONES DE CONTEXTO')

def p_error(p):
	  # get formatted representation of stack
    stack_state_str = ' '.join([symbol.type for symbol in parser.symstack][1:])

    print('Syntax error in input! Parser State:{} {} . {}'
          .format(parser.state,
                  stack_state_str,
                  p))
   # print("Syntax error in input!")

def p_progr(p):
	'''
	progr : neurProStart PROGRAM CONST_ID SEMICOLON pro1 L_BRACE neurPro1 pro2 R_BRACE neurPro
	'''
	print(quads)
	
	lisConstInt=tablaConst.getNamesINT()
	lisConstFloat=tablaConst.getNamesFLOAT()

	sizeIntGl=tablaGlobal.getSizeInt()
	sizeFlGl=tablaGlobal.getSizeFloat()

	sizeIntLoc=tablaLocal.getSizeInt()
	sizeFlLoc=tablaLocal.getSizeFloat()

	sizeIntTemp=tablaTemp.getSizeInt()
	sizeFlTemp=tablaTemp.getSizeFloat()

	virtualMachine=MaquinaVirtual(quads,lisConstInt,lisConstFloat,sizeIntGl,sizeFlGl,sizeIntLoc,sizeFlLoc,sizeIntTemp,sizeFlTemp)
	virtualMachine.run()



#	tablaConst.printTabladeVariables()

def p_neurProStart(p):
	'''
	neurProStart : 
	'''


def p_pro1(p):
	'''
	pro1 : vars pro1
		| funcion pro1
		| empty
	'''
	pass

def p_pro2(p):
	'''
	pro2 : vars pro2
		| estatuto pro2
		| empty 
	'''
	pass



def p_neurPro1(p):
	'''
	neurPro1 :
	'''
	global varContext,quads
	varContext=1
	quads.insert(0,('goto',len(quads)+1))



def p_neurPro(p):
	'''
	neurPro :
	'''
	global quads
	quads+=[('end',1)]

#HASTA AQUI VA PERF


def p_vars(p):
	'''
	vars : tipo vars1 vars2 SEMICOLON
	'''
	global flagTypeVars
	flagTypeVars=''

#def p_neurVars(p):
#	'''
#	neurVars : tipo vars1
#	'''
#	global flagType
#	flagType=p[1]



def p_vars1(p):
	'''
	vars1 : CONST_ID
		| CONST_ID L_BRACKET cte R_BRACKET
		| CONST_ID L_BRACKET cte R_BRACKET L_BRACKET cte R_BRACKET

	'''
	global flagTypeVars,varContext,tablaGlobal,tablaLocal
	
	if(len(p)==2):
		if(varContext==0):
			if(tablaGlobal.existsVar(p[1])):
				print("La variable global " + p[1] + " ya existe")
			else:
				if(flagTypeVars=="int" or flagTypeVars=="INT" or flagTypeVars=="float" or flagTypeVars=="FLOAT"):
					tablaGlobal.addVar(flagTypeVars,p[1])
				else:
					print("Declaraste un tipo incorrecto en la variable "+p[1]+" de tipo global "+flagTypeVars)
		else:
			if(tablaLocal.existsVar(p[1])):
				print("La variable local " + p[1] + " ya existe")
			else:
				if(flagTypeVars=="int" or flagTypeVars=="INT" or flagTypeVars=="FLOAT" or flagTypeVars=="float"):
					tablaLocal.addVar(flagTypeVars,p[1])
				else:
					print("Declaraste un tipo incorrecto en la variable "+p[1]+" de tipo local")
	elif(len(p)==5):

		if(getTypeUniversal(p[3]) != 'INT'):
			print('Parser : declaraste el arreglo '+p[1]+' con dimension incorrecta')
		else:
			temp=tablaConst.getNameVar(p[3])

			if(varContext==0):
				if(tablaGlobal.existsVar(p[1])):
					print("La variable global " + p[1] + " ya existe")
				else:
					if(flagTypeVars=="int" or flagTypeVars=="INT" or flagTypeVars=="float" or flagTypeVars=="FLOAT"):
						tablaGlobal.addVar(flagTypeVars,p[1],temp)
					else:
						print("Declaraste un tipo incorrecto en la variable "+p[1]+" de tipo global ")
			else:
				if(tablaLocal.existsVar(p[1])):
					print("La variable local " + p[1] + " ya existe")
				else:
					if(flagTypeVars=="int" or flagTypeVars=="INT" or flagTypeVars=="FLOAT" or flagTypeVars=="float"):
						tablaLocal.addVar(flagTypeVars,p[1],temp)
					else:
						print("Declaraste un tipo incorrecto en la variable "+p[1]+" de tipo local")

	else:
		if(getTypeUniversal(p[3]) != 'INT' or getTypeUniversal(p[6]) != 'INT'):
			print('Parser : declaraste el arreglo '+p[1]+' con dimension incorrecta')
		else:
			temp=tablaConst.getNameVar(p[3])
			temp2=tablaConst.getNameVar(p[6])


			if(varContext==0):
				if(tablaGlobal.existsVar(p[1])):
					print("La variable global " + p[1] + " ya existe")
				else:
					if(flagTypeVars=="int" or flagTypeVars=="INT" or flagTypeVars=="float" or flagTypeVars=="FLOAT"):
						tablaGlobal.addVar(flagTypeVars,p[1],temp,temp2)
					else:
						print("Declaraste un tipo incorrecto en la variable "+p[1]+" de tipo global "+flagTypeVars)
			else:
				if(tablaLocal.existsVar(p[1])):
					print("La variable local " + p[1] + " ya existe")
				else:
					if(flagTypeVars=="int" or flagTypeVars=="INT" or flagTypeVars=="FLOAT" or flagTypeVars=="float"):
						tablaLocal.addVar(flagTypeVars,p[1],temp,temp2)
					else:
						print("Declaraste un tipo incorrecto en la variable "+p[1]+" de tipo local")


def p_vars2(p):
	'''
	vars2 : COMMA vars1 vars2
		| empty
	'''
	pass


def p_tipo(p):
	'''
	tipo : INT
		| FLOAT
	'''
	global flagTypeVars
	flagTypeVars=p[1]
	p[0]=p[1]

def p_bloque(p):
	'''
	bloque : L_BRACE bloque1 R_BRACE
	'''
	pass

def p_bloque1(p):
	'''
	bloque1 : estatuto bloque1
		| empty
	'''
	pass

def p_estatuto(p):
	'''
	estatuto : condicion
		| lectura
		| ciclo
		| asignacion
		| funcionLL SEMICOLON
		| impresion
	'''
	pass

def p_asignacion(p):
	'''
	asignacion : datStr ASSIGN exp SEMICOLON 
	'''
	global quads
	if(getTypeUniversal(p[3])==getTypeUniversal(p[1])):
		quads=quads + [("=",p[3],p[1])]
	else:
		print('Error no puedes asignar tipos diferentes')

def p_datStr(p):
	'''
	datStr : CONST_ID
		| CONST_ID L_BRACKET exp R_BRACKET
		| CONST_ID L_BRACKET exp R_BRACKET L_BRACKET exp R_BRACKET 
	'''
	global tablaGlobal,tablaLocal,quads,tempCont
	
	if(len(p)==2):
		if(tablaLocal.existsVar(p[1])):
			if(tablaLocal.getLsDim1(p[1])>0):
				print('Error la variable '+p[1]+' debe incluir un indices al ser llamada')
			else:
				address=tablaLocal.getDireccionMem(p[1])
		elif(tablaGlobal.existsVar(p[1])):
			if(tablaGlobal.getLsDim1(p[1])>0):
				print('Error la variable '+p[1]+' debe incluir un indices al ser llamada')
			else:
				address=tablaGlobal.getDireccionMem(p[1])

		else:
			print('La variable '+p[1]+' no existe')
		p[0]=address


	elif(len(p)==5):

		#address=0
		if(tablaLocal.existsVar(p[1])):

			if(tablaLocal.getLsDim2(p[1])>0):
				print('Error la variable '+p[1]+' debe incluir dos indices al ser llamada')
			elif(tablaLocal.getLsDim1(p[1])==0):
				print('Error la variable '+p[1]+' no es dimensionada')
			else:
				address=tablaLocal.getDireccionMem(p[1])
				s1=tablaLocal.getS1(p[1])
				limS=tablaLocal.getLsDim1(p[1])
				varTempType=tablaLocal.getType(p[1])


		elif(tablaGlobal.existsVar(p[1])):
			if(tablaGlobal.getLsDim2(p[1])>0):
				print('Error la variable '+p[1]+' debe incluir dos indices al ser llamada')
			elif(tablaGlobal.getLsDim1(p[1])==0):
				print('Error la variable '+p[1]+' no es dimensionada')
			else:
				address=tablaGlobal.getDireccionMem(p[1])
				s1=tablaGlobal.getS1(p[1])
				limS=tablaGlobal.getLsDim1(p[1])
				varTempType=tablaGlobal.getType(p[1])

		else:
			print('La variable '+p[1]+' no existe')




		

		if(not tablaConst.existsVar(s1)):
			tablaConst.addVar('INT',s1)#s1 lo guardo como constante para que tenga direccion

		if(not tablaConst.existsVar(address)):
			tablaConst.addVar('INT',address)#s1 lo guardo como constante para que tenga direccion

		tablaTemp.addVar(varTempType,'t'+str(tempCont))
		temp='t'+str(tempCont)

		quads+=[('ver',p[3],0,limS-1),('+',tablaConst.getDireccionMem(address),p[3],[tablaTemp.getDireccionMem(temp)])]
		tempCont+=1

		p[0]=[tablaTemp.getDireccionMem(temp)]

	else:	
		address=0
		
		if(tablaLocal.existsVar(p[1])):
			if(tablaLocal.getLsDim2(p[1])==0):
				print('Error la variable '+p[1]+' no es dimensionada a ese nivel')
			else:
				address=tablaLocal.getDireccionMem(p[1])
				s1=tablaLocal.getS1(p[1])
				limS=tablaLocal.getLsDim1(p[1])
				limS2=tablaLocal.getLsDim2(p[1])
				varTempType=tablaLocal.getType(p[1])

			

		elif(tablaGlobal.existsVar(p[1])):
			if(tablaLocal.getLsDim1(p[1])==0):
				print('Error la variable '+p[1]+' no es dimensionada a ese nivel')
			else:
				address=tablaGlobal.getDireccionMem(p[1])
				s1=tablaGlobal.getS1(p[1])
				limS=tablaGlobal.getLsDim1(p[1])
				limS2=tablaGlobal.getLsDim2(p[1])
				varTempType=tablaGlobal.getType(p[1])

		
		else:
			print('La variable '+p[1]+' no existe')
		
		if(not tablaConst.existsVar(s1)):
			tablaConst.addVar('INT',s1)#s1 lo guardo como constante para que tenga direccion

		if(not tablaConst.existsVar(address)):
			tablaConst.addVar('INT',address)#s1 lo guardo como constante para que tenga direccion


		tablaTemp.addVar(varTempType,'t'+str(tempCont))
		temp='t'+str(tempCont)
		tempCont+=1
		
		quads+=[('ver',p[3],0,limS-1),('ver',p[6],0,limS2-1),('*',p[3],tablaConst.getDireccionMem(s1),tablaTemp.getDireccionMem(temp))]
		# temp tiene guardado la multip le falta la suma

		tablaTemp.addVar(varTempType,'t'+str(tempCont))
		temp2='t'+str(tempCont)
		tempCont+=1

		quads+=[('+',tablaTemp.getDireccionMem(temp),p[6],tablaTemp.getDireccionMem(temp2))]
		
		tablaTemp.addVar(varTempType,'t'+str(tempCont))
		temp3='t'+str(tempCont)
		tempCont+=1

		quads+=[('+',tablaConst.getDireccionMem(address),tablaTemp.getDireccionMem(temp2),[tablaTemp.getDireccionMem(temp3)])]


		p[0]=[tablaTemp.getDireccionMem(temp3)]


def p_lectura(p):
	'''
	lectura : READ L_PARENTHESIS datStr R_PARENTHESIS SEMICOLON
	''' 
	global quads
	quads=quads + [("read",p[3])]


def p_impresion(p):
	'''
	impresion : PRINT L_PARENTHESIS datStr R_PARENTHESIS SEMICOLON
	''' 
	global quads
	quads=quads + [("print",p[3])]

def p_expresion(p):
	'''
	expresion : expOp
		| expOp AND expOp
		| expOp OR expOp
	'''
	global quads,tablaTemp,tempCont
	
	if(len(p)==2):
		p[0]=p[1]
	else:
		tablaTemp.addVar('INT','t'+str(tempCont))
		
		if(p[2]=="&&"):
			quads=quads + [("&&",p[1],p[3],tablaTemp.getDireccionMem('t'+str(tempCont)))]
		else:
			quads=quads + [("||",p[1],p[3],tablaTemp.getDireccionMem('t'+str(tempCont)))]

		p[0]=tablaTemp.getDireccionMem('t'+str(tempCont))
		tempCont+=1


def p_expOp(p): 
	'''
	expOp : exp
		| exp GREATER_THAN exp
		| exp LESS_THAN exp
		| exp EQUALS_TO exp 
		| exp DIFF_THAN exp
	'''
	global quads,tablaTemp,tempCont
	if(len(p)==2):
		p[0]=p[1]

	else:
		tablaTemp.addVar('INT','t'+str(tempCont))

		if(p[2]=='>'):
			quads=quads + [(">",p[1],p[3],tablaTemp.getDireccionMem('t'+str(tempCont)))]
		elif(p[2]=='<'):
			quads=quads + [("<",p[1],p[3],tablaTemp.getDireccionMem('t'+str(tempCont)))]	
		elif(p[2]=='=='):
			quads=quads + [("==",p[1],p[3],tablaTemp.getDireccionMem('t'+str(tempCont)))]
		else:
			quads=quads + [("!=",p[1],p[3],tablaTemp.getDireccionMem('t'+str(tempCont)))]
		
		p[0]=tablaTemp.getDireccionMem('t'+str(tempCont))
		tempCont+=1


def p_exp(p):
	'''
	exp : termino
		| termino PLUS exp
		| termino MINUS exp 
	'''
	global quads,tablaTemp,tempCont,cubo
	if(len(p)==2):
		p[0]=p[1]

	elif(p[2]=="+"):
		temp=cubo.checkType(getTypeUniversal(p[1]),getTypeUniversal(p[3]),'+')

		if(temp=='INT'):
			tablaTemp.addVar('INT','t'+str(tempCont))
		elif(temp=='FLOAT'):
			tablaTemp.addVar('FLOAT','t'+str(tempCont))

		quads=quads + [("+",p[1],p[3],tablaTemp.getDireccionMem('t'+str(tempCont)))]
		p[0]=tablaTemp.getDireccionMem('t'+str(tempCont))
		tempCont+=1
	else:
		temp=cubo.checkType(getTypeUniversal(p[1]),getTypeUniversal(p[3]),'-')

		if(temp=='INT'):
			tablaTemp.addVar('INT','t'+str(tempCont))
		elif(temp=='FLOAT'):
			tablaTemp.addVar('FLOAT','t'+str(tempCont))

		quads=quads + [("-",p[1],p[3],tablaTemp.getDireccionMem('t'+str(tempCont)))]
		p[0]=tablaTemp.getDireccionMem('t'+str(tempCont))
		tempCont+=1
	
def p_termino(p):
	'''
	termino : factor
		| factor MULTIP termino
		| factor DIVIDE termino
	'''
	global quads,tablaTemp,tempCont,cubo
	temp=''
	if(len(p)==2):
		p[0]=p[1]
	elif(p[2]=="*"):
		temp=cubo.checkType(getTypeUniversal(p[1]),getTypeUniversal(p[3]),'*')

		if(temp=='INT'):
			tablaTemp.addVar('INT','t'+str(tempCont))
		elif(temp=='FLOAT'):
			tablaTemp.addVar('FLOAT','t'+str(tempCont))

		quads=quads + [("*",p[1],p[3],tablaTemp.getDireccionMem('t'+str(tempCont)))]
		p[0]=tablaTemp.getDireccionMem('t'+str(tempCont))
		tempCont+=1
	
	else:
		temp=cubo.checkType(getTypeUniversal(p[1]),getTypeUniversal(p[3]),'/')

		if(temp=='INT'):
			tablaTemp.addVar('INT','t'+str(tempCont))
		elif(temp=='FLOAT'):
			tablaTemp.addVar('FLOAT','t'+str(tempCont))

		quads=quads + [("/",p[1],p[3],tablaTemp.getDireccionMem('t'+str(tempCont)))]
		p[0]=tablaTemp.getDireccionMem('t'+str(tempCont))
		tempCont+=1
	

def p_factor(p):
	'''
	factor : L_PARENTHESIS expresion R_PARENTHESIS
		| factor1
		| PLUS factor1
		| MINUS factor1
	'''
	global quads,tablaTemp,tempCont

	if(len(p)==4):
		p[0]=p[2]
	elif(len(p)==3):
		if(p[1]=="-"):
			if(getTypeUniversal(p[2])=='INT'):
				tablaTemp.addVar('INT','t'+str(tempCont))
			elif(getTypeUniversal(p[2])=='FLOAT'):
				tablaTemp.addVar('FLOAT','t'+str(tempCont))
			else:
				print("Error usaste una variable que no estaba declarada")

			quads=quads + [("-",0,p[2],tablaTemp.getDireccionMem('t'+str(tempCont)))]
			p[0]=tablaTemp.getDireccionMem('t'+str(tempCont))
			tempCont+=1

		else:
			p[0]=p[2]
	else:
		p[0]=p[1]

def p_factor1(p):
	'''
	factor1 : datStr
		| funcionLL
		| cte
	'''

	p[0]=p[1]

def p_cte(p):
	'''
	cte : CONST_INT
		| CONST_FLOAT empty
	'''
	if(not tablaConst.existsVar(p[1])):
		if(len(p)==2):
			tablaConst.addVar('INT',p[1])
		else:
			tablaConst.addVar('FLOAT',p[1])
	p[0]=tablaConst.getDireccionMem(p[1])




def p_condicion(p):
	'''
	condicion : IF L_PARENTHESIS expresion neurCond1 bloque neurCond2
		|  IF L_PARENTHESIS expresion neurCond1 bloque ELSE neurCond2x1 neurCond3  bloque neurCond4
	'''
	pass

def p_neurCond1(p):
	'''
	neurCond1 : R_PARENTHESIS
	'''
	global pSaltos,quads
	pSaltos.append(len(quads))
	quads+=[("tempBorrar neurcond1")]

def p_neurCond2(p):
	'''
	neurCond2 : 
	'''
	global pSaltos,quads
	temp=pSaltos.pop()
	del quads[temp]
	quads.insert(temp,("gotoF",quads[temp-1][3],len(quads)+1))
	#Si quieres que el indice empiece en 0 entonces debe ser len(quads)+1 de lo contrario sumale 1

def p_neurCond2x1(p):
	'''
	neurCond2x1 : 
	'''
	global pSaltos,quads
	temp=pSaltos.pop()
	del quads[temp]
	quads.insert(temp,("gotoF",quads[temp-1][3],len(quads)+2))
	#Si quieres que el indice empiece en 0 entonces debe ser len(quads)+1 de lo contrario sumale 1

def p_neurCond3(p):
	'''
	neurCond3 :
	'''
	global pSaltos,quads
	pSaltos.append(len(quads))
	quads+=[("tempBorrar neurcond3")]

def p_neurCond4(p):
	'''
	neurCond4 :
	'''
	global pSaltos,quads
	temp=pSaltos.pop()
	del quads[temp]
	quads.insert(temp,("goto",len(quads)+1))





def p_ciclo(p):
	'''
	ciclo : FOR L_PARENTHESIS asignacion neurCiclo1 expresion neurCiclo2 SEMICOLON asignacion R_PARENTHESIS bloque neurCiclo3
		| WHILE neurCiclo1 L_PARENTHESIS expresion R_PARENTHESIS neurCiclo2 bloque neurCiclo3 
	'''
	pass


def p_neurCiclo1(p):#aqui debe regresar para while
	'''
	neurCiclo1 : 
	'''
	global pSaltos
	pSaltos.append(len(quads))

def p_neurCiclo2(p):#gotoF al final
	'''
	neurCiclo2 : 
	'''
	global pSaltos,quads
	pSaltos.append(len(quads))
	quads+=[("tempBorrar neurCiclo2")]

def p_neurCiclo3(p):#goto al inicio y actualizar gotoF
	'''
	neurCiclo3 : 
	'''
	global pSaltos,quads
	temp=pSaltos.pop()
	del quads[temp]
	quads.insert(temp,("gotoF",quads[temp-1][3],len(quads)+2))#en while se debe rest
	quads+=[("goto",pSaltos.pop())]


funcName=''
funcType=''
def p_funcion(p):
	'''
	funcion : neurFunc L_PARENTHESIS neurFunc2 funcion1 R_PARENTHESIS L_BRACE funcionVars bloque1 RETURN expresion SEMICOLON R_BRACE
		| neurFuncVoid L_PARENTHESIS neurFunc2 funcion1 R_PARENTHESIS L_BRACE funcionVars bloque1 R_BRACE
	'''
	global quads,funcName,funcType
	if(len(p)>11):
		if(not getTypeUniversal(p[10])==funcType):
			print('Error estas intentando devolver un tipo incorrecto en la funcion '+funcName)
	
	dirFunciones.setSizeLocalsINT(funcName,tablaLocal.getSizeInt())
	dirFunciones.setSizeLocalsFLOAT(funcName,tablaLocal.getSizeFloat())

	dirFunciones.setSizeTempsINT(funcName,tablaTemp.getSizeInt())
	dirFunciones.setSizeTempsFLOAT(funcName,tablaTemp.getSizeFloat())	

	if(funcType=='VOID' or funcType=='void'):
		quads+=[('endproc','void')]
	else:
		quads+=[('endproc',p[10])]


	funcName=''
	funcType=''
	tablaLocal.eraseAll()
	tablaTemp.eraseAll()


def p_funcionVars(p):
	'''
	funcionVars : vars
		| empty 
	'''
	pass

def p_neurFunc(p):
	'''
	neurFunc : tipo CONST_ID
	'''
	global dirFunciones,funcName,funcType,varContext,quads
	funcName=p[2]
	funcType=p[1]

	#print(funcName)
	if(dirFunciones.existFn(funcName)):
		print("Error declaraste una funcion que ya existe")
	else:
		dirFunciones.addFn(funcType,funcName)
		dirFunciones.setDireccionInicio(funcName,len(quads))
	varContext=1 #se empieza a hacer contexto local
	tempCont=0 # las variables temporales empiezan en 0

def p_neurFuncVoid(p):
	'''
	neurFuncVoid : VOID CONST_ID
	'''
	global dirFunciones,funcName,funcType,varContext,quads
	funcName=p[2]
	funcType=p[1]

	#print(funcName)
	if(dirFunciones.existFn(funcName)):
		print("Error declaraste una funcion que ya existe")
	else:
		dirFunciones.addFn(funcType,funcName)
		dirFunciones.setDireccionInicio(funcName,len(quads))
	varContext=1 #se empieza a hacer contexto local
	tempCont=0 # las variables temporales empiezan en 0




def p_neurFunc2(p):
	'''
	neurFunc2 : tipo vars1
	'''
	global funcName,dirFunciones

	if(p[1]=='int' or p[1]=='INT'):
		dirFunciones.addParamFn(funcName,'int')
#		tablaLocal.addVar('INT',p[2])
	elif(p[1]=='float' or p[1]=='FLOAT'):
		dirFunciones.addParamFn(funcName,'float')
#		tablaLocal.addVar('FLOAT',p[2])
	else:
		print("Pusiste un tipo incorrecto en la declaracion de "+ funcName + ' pusiste '+p[1])

def p_funcion1(p):
	'''
	funcion1 : COMMA neurFunc2 funcion1
		| empty
	'''
	pass



funcNameLL=[]
listParam=[]
contParam=0

listaQuadsPendientes=[]
def p_funcionLL(p):
	'''
	funcionLL : neurFuncLL L_PARENTHESIS neurFuncLL2 funcionLL1 R_PARENTHESIS
	'''
	global listParam,contParam,funcNameLL,quads,tempCont,listaQuadsPendientes
	#print(listParam)
	if(not dirFunciones.verificaParam(funcNameLL[len(funcNameLL)-1],listParam)):
		print("Error declaraste los parametros mal al intentar llamar la funcion "+funcNameLL[len(funcNameLL)-1])
	

	quads+=[('era',funcNameLL[len(funcNameLL)-1])]
	quads+=listaQuadsPendientes
	quads+=[('gosub',dirFunciones.getDireccionInicio(funcNameLL[len(funcNameLL)-1]))]
	
	if(dirFunciones.getTypeFn(funcNameLL[len(funcNameLL)-1])=='INT'):
		tablaTemp.addVar('INT','t'+str(tempCont))
		quads+=[('=',funcNameLL[len(funcNameLL)-1],tablaTemp.getDireccionMem('t'+str(tempCont)))]
		p[0]=tablaTemp.getDireccionMem('t'+str(tempCont))
		tempCont+=1
	
	elif(dirFunciones.getTypeFn(funcNameLL[len(funcNameLL)-1])=='FLOAT'):
		tablaTemp.addVar('FLOAT','t'+str(tempCont))
		quads+=[('=',funcNameLL[len(funcNameLL)-1],tablaTemp.getDireccionMem('t'+str(tempCont)))]
		p[0]=tablaTemp.getDireccionMem('t'+str(tempCont))
		tempCont+=1
	

	funcNameLL.pop()
	listParam=[]
	contParam=0

	

def p_neurFuncLL(p):
	'''
	neurFuncLL : CONST_ID
	'''
	global quads,funcNameLL
	funcNameLL.append(p[1])


def p_neurFuncLL2(p):
	'''
	neurFuncLL2 : exp
	'''
	global listParam,contParam,listaQuadsPendientes
	listaQuadsPendientes+=[('param',p[1],contParam)]
	#quads+=[('param',p[1],contParam)]
	contParam+=1
	listParam+=[getTypeUniversal(p[1])] 


def p_funcionLL1(p):
	'''
	funcionLL1 : COMMA exp funcionLL1
		| empty
	'''
	global listParam,contParam,listaQuadsPendientes
	if(len(p)==2):
		pass
	else:
		listaQuadsPendientes+=[('param',p[2],contParam)]
		#quads+=[('param',p[2],contParam)]
		contParam+=1 
		listParam+=[getTypeUniversal(p[2])] 


#def p_expression(p):
#	'''
#	expression : INT 
#		| FLOAT
#	'''
#	p[0]=p[1]


def p_empty(p):
	'''
	empty :
	'''
	p[0]=None




parser=yacc.yacc()

#while True:
#	try:
#		file = open("input.txt","r")
#	except EOFError:
#		break
#	for line in file:
#		print(line)
#		parser.parse(line)
file = open("input.txt","r")
result=""
for line in file:
		result = result + line
#print(result)
file.close()
parser.parse(result)

