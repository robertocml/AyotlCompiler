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
