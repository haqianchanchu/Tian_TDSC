from pypbc import *
import hashlib
class  Params(object):
	"""docstring for  Params"""
	def get_hash256(self,data):
		hash256 = hashlib.sha256()
		hash256.update(data.encode('utf-8'))
		return hash256.hexdigest()
		
	def start(self):
		try:
			f = open('circle.para','r')
		except:
			return "open error"
		try:
			self.params = Parameters(param_string=f.read())
		except:
			return "para error"
		finally:
			f.close()
		self.pairing = Pairing(self.params)
		self.g = Element.from_hash(self.pairing, G2, self.get_hash256("123"))
		self.u = Element.from_hash(self.pairing, G1, self.get_hash256("456"))


	def e(self,ele1,ele2):
		return self.pairing.apply(ele1,ele2)

	def H(self,input_msg):
		return Element.from_hash(self.pairing, G1, self.get_hash256(input_msg))

	def h(self,input_msg):
		return Element.from_hash(self.pairing, Zr, self.get_hash256(input_msg))

	def pi2(self,zr,number):
		tem = Element(self.pairing, Zr, value=number)
		return tem+zr

	def pi1(self,zr,number,n):
		return (int(str(zr),16)+number)%n

	def ran_zr(self):
		return Element.random(self.pairing,Zr)
	def get_zr(self,number):
		return Element(self.pairing, Zr, value=number)
	def get_G1_zero(self):
		return Element.one(self.pairing,G1)
	def get_G1(self,input):
		return Element(self.pairing,G1,input)
	def get_G2(self,input):
		return Element(self.pairing,G2,input)
		

if __name__ == '__main__':
	my_para = Params()
	my_para.start()
	print(len(str(my_para.g))%16)