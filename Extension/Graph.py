

class ComputationalGraph:

	def __init__(self):

		self.Nodeindex = 0 
		self.NodeList =[]

	def append(self, Node):
		'''
		This method append the node to the graph in sequence and record the index of that node

		INPUTS
		======

		Node: The Node that is to be appended on the List

		Return
		======
		None

		'''
		self.Nodeindex +=1
		self.NodeList.append(Node)



	def ValidOp(self,i):  #Valid operation
		'''

		INPUT
		=====
		i : The number corresponding to the operators 

		Return
		======
		The Value of the key in the swither


		NOTES
		======
		This method structurally defines a way to 
		store all the valid operators 
		supported by this reverse mode class 

		'''
		switcher ={
			1 : "add",
			2 : "mul",
			3 : "neg",
			4 : "div",
			5 : "pow",
			6 : "sub"
		}
		return  switcher.get(i," Invalid Operator")

	def ComputeValue(self):
		'''
		This function utilize forward pass to compute the value of the function

		'''
		for node in self.NodeList:
			if node.operation == self.ValidOp(1):
				node.value = self.NodeList[node.nodeleft].value + self.NodeList[node.noderight].value

			elif node.operation == self.ValidOp(2):
				node.value = self.NodeList[node.nodeleft].value*self.NodeList[node.noderight].value

			elif node.operation == self.ValidOp(4):
				node.value = self.NodeList[node.nodeleft].value/self.NodeList[node.noderight].value

			elif node.operation == self.ValidOp(6):
				node.value = self.NodeList[node.nodeleft].value-self.NodeList[node.noderight].value

			elif node.operation == self.ValidOp(5):
				node.value = self.NodeList[node.nodeleft].value**self.NodeList[node.noderight].value




	def ComputeGradient(self,lastIndex = -1):
		'''
		This function back propagate to calculate the gradient of the variables with reverse mode

		INPUT 
		=====

		'''
		#Set the seed 
		self.clearGraph()
		self.NodeList[lastIndex].deri = 1.0
		#Perform back prop
		for node in self.NodeList[-1::-1]:
			if node.operation == self.ValidOp(1):
				self.NodeList[node.nodeleft].deri += node.deri
				self.NodeList[node.noderight].deri += node.deri

			if node.operation == self.ValidOp(6):
				self.NodeList[node.nodeleft].deri += node.deri
				self.NodeList[node.noderight].deri -= node.deri

			elif node.operation == self.ValidOp(2):
				self.NodeList[node.nodeleft].deri += node.deri * self.NodeList[node.noderight].value
				self.NodeList[node.noderight].deri += node.deri * self.NodeList[node.nodeleft].value

			elif node.operation == self.ValidOp(4):
				self.NodeList[node.nodeleft].deri += node.deri / self.NodeList[node.noderight].value
				self.NodeList[node.noderight].deri += -node.deri * self.NodeList[node.nodeleft].value/self.NodeList[node.noderight].value**2

			elif node.operation == self.ValidOp(5):
				self.NodeList[node.nodeleft].deri =  self.NodeList[node.noderight].value * self.NodeList[node.nodeleft].value **(self.NodeList[node.noderight].value-1)

				# There is sth weird here


	def clearGraph(self):
		'''
		In order to reuse the node for different functions, 
		we clear the graph by reassign the derivatives for all node to zero
		'''
		for i in self.NodeList:
			i.deri = 0 


	def WIPER(self,D):
		for i in self.NodeList[D:]:
			if i.operation != "Const":
				i.deri = 0
				i.value = 0

	def SeriesValues(self,C,D):
		ValList=[]
		DerList =[]
		C= C.T
		for j in range(len(C)):
			self.WIPER(D)
			for i in range(0,D):
				self.NodeList[i].value = C[j][i]
			self.ComputeValue()
			self.ComputeGradient()
			ValList.append(self.NodeList[-1].value)
			Deri =[]
			for i in range(0,D):
				 Deri.append(self.NodeList[i].deri)
			DerList.append(Deri)
		return ValList,DerList


