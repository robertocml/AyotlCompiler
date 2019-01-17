from Complementos.TablaVariables import TablaVariables
from Complementos.DirFunciones import DirFunciones

tabla = TablaVariables('global')
dirf = DirFunciones()
listaPar = ['INT']


dirf.addFn('int','uno')
dirf.setDireccionInicio('uno',2000)
print(dirf.getDireccionInicio('uno'))
dirf.addParamFn('uno','int')



print("---------------")

if dirf.verificaParam('uno',listaPar):
	print("son iguales")
else:
	print("lista del dir " + str(dirf.getParametersAddresses('uno')))
print("---------------")



