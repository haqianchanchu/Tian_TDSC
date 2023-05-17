from my_init import *
import random
import time
class Auth_up_SSP(Params):
	"""docstring for Auth_up"""
	def __init__(self,file_name):
		self.start()
		self.file_name = file_name
		with open(file_name,"r") as f:
			msg = f.read()
		Ti = msg.split("/n")[2]
		Ti = Ti.split("0x")[1:]
		ci = msg.split("/n")[5]
		ci = ci.split("_")
		self.t = msg.split("/n")[0]
		self.t = self.get_G2(self.t)
		self.Mi = []
		count = 0
		self.time = []
		time1 = time.time()
		for tem_T in Ti:
			self.Mi.append(self.H("0x"+tem_T+str(count)))
			count += 1
		self.n = len(self.Mi)
		self.S = []
		for x in range(0,self.n):
			self.S.append(random.randint(0,123456789))
		self.rou = []
		for x in range(0,self.n):
			tem_h = self.h(ci[x]+str(self.S[x]))
			self.rou.append(self.Mi[x]*(self.u**tem_h))
		self.aux = self.get_G1_zero()
		for x in range(0,self.n):
			self.aux *= self.rou[x]
		self.time.append(time.time()-time1)

	def checkSave(self,sigma):
		Pw = self.get_G1_zero()
		for tem_sigma in sigma:
			Pw *= tem_sigma
		time1 = time.time()
		if self.e(Pw,self.g) == self.e(self.aux,self.t):
			self.time.append(time.time()-time1)
			with open(self.file_name,"r") as f:
				msg = f.read()
			msg = msg.split("/n")
			sigma_str = []
			for tem_sigma in sigma:
				sigma_str.append(str(tem_sigma))
			msg[4] = "".join(sigma_str)
			msg = "/n".join(msg)
			with open(self.file_name,"w") as f:
				f.write(msg)


class Auth_up_U(Params):
	"""docstring for Auth_up_U"""
	def encrypt(self,file_name,rou):
		self.start()
		with open(file_name,"r") as f:
			self.sk = f.read().split("_")[2]
		self.sk = self.get_zr(int(self.sk,16))
		self.sigma = []
		time1 = time.time()
		for tem_rou in rou:
			self.sigma.append(tem_rou**self.sk)
		self.time = time.time()-time1
			




		
		


def main():
	SSP = Auth_up_SSP("./save/1.txt")
	U = Auth_up_U()
	U.encrypt("./user/data",SSP.rou)
	SSP.checkSave(U.sigma)
	# print(SSP.time,U.time)
	return SSP.time[0]+SSP.time[1],U.time

if __name__ == '__main__':
	print(main())