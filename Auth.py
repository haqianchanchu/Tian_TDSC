from my_init import *
import random
import time

class SSP1(Params):
	def  __init__(self,filename):
		self.start()
		with open(filename,"r") as f:
			tem_sigma = f.read().split("/n")[4]
		with open(filename,"r") as f:
			self.t = f.read().split("/n")[0]
		with open(filename,"r") as f:
			ci = f.read().split("/n")[5]
		self.ci = ci.split("_")
		self.sigma = []
		for x in range(0,int(len(tem_sigma)/len(str(self.u)))):
			self.sigma.append(tem_sigma[x*len(str(self.u)):(x+1)*len(str(self.u))])
		self.n = len(self.sigma)

	def AuthGen(self,cha_num):
		# self.z = random.randint(1,self.n)
		if cha_num > self.n:
			cha_num = self.n
		self.z = cha_num
		self.r1 = self.ran_zr()
		self.r2 = self.ran_zr()

		ai = []
		bi = []
		
		for x in range(0,self.z):
			ai.append(self.pi1(self.r1,x,self.n))
			bi.append(self.pi2(self.r2,x))
	
		lamuda = self.get_G1_zero()
		time1 = time.time()
		for x in range(0,self.z):
			lamuda *= self.get_G1(self.sigma[x])**bi[x]
		self.time = time.time()-time1
		self.lamuda = lamuda
		self.bi = bi
		self.ai = ai
		return lamuda
	def check(self,daita):
		self.Mi = []
		M = self.get_G1_zero()
		time1 = time.time()
		for count in range(0,self.z):
			tem_c = self.ci[count].encode()
			tem_T = self.h(str(tem_c))
			tem_M = self.H(str(tem_T)+str(count))
			M *= tem_M**self.bi[count]
			self.Mi.append(tem_M)
		t = self.get_G2(self.t)
		self.e(self.lamuda,self.g) == self.e(M*(self.u**daita),t)
		self.time += time.time()-time1


class SSP2(Params):
	"""docstring for SSP2"""
	def __init__(self,filename):
		self.start()
		with open(filename,"r") as f:
			ci = f.read().split("/n")[5]
		self.ci = ci.split("_")
		self.n = len(self.ci)
	def react(self,z,r1,r2):
		ai = []
		bi = []
		time1 = time.time()
		for x in range(0,z):
			ai.append(self.pi1(r1,x,self.n))
			bi.append(self.pi2(r2,x))
		right = []
		ans = self.get_zr(0)
		for x in range(0,z):
			tem_c = self.ci[x].encode()
			right.append(self.h(str(tem_c)))
			ans += bi[x]*right[x]
		self.time = time.time()-time1
		return ans
		
		print(ans)
		
		





def main(cha_num):
	ssp1 = SSP1("./save/1.txt")
	ssp2 = SSP2("./save/1.txt")
	ssp1.AuthGen(cha_num)
	daita = ssp2.react(ssp1.z,ssp1.r1,ssp1.r2)
	ssp1.check(daita)
	return ssp2.time+ssp1.time
	# print(len(ssp1.ci))





if __name__ == '__main__':
	print(main(4600))