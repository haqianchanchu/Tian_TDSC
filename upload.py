from my_init import *
import AES
import random
import time
class  Upload_U(Params):
	"""docstring for  Upload"""
	def __init__(self, file_name, filesize):
		self.file_name = file_name
		self.time = []
		time1 = time.time()
		self.start()
		self.time.append(time.time()-time1)
		self.FILESIZE = filesize;
		

	def encrypt(self,cha_num):
		self.ki = []
		self.ci = []
		self.Ti = []
		self.n = 0
		self.Ck = ""
		time1 = time.time()
		with open(self.file_name,"r") as f:
			tem_str = f.read()
			self.sk = str(self.h(tem_str))
			self.sk_real = self.h(tem_str)
		self.t = self.g**self.sk_real
		
		with open(self.file_name) as f:
			tem_str = f.read(self.FILESIZE)
			while tem_str:
				key = str(self.h(tem_str))
				self.ki.append(key)
				tem_c = AES.encrypt(key,tem_str)
				self.ci.append(tem_c.decode())
				tem_t = self.h(str(tem_c))
				self.Ti.append(tem_t)
				self.n += 1
				tem_str = f.read(self.FILESIZE)
		self.Ck = AES.encrypt(self.sk,"".join(self.ki))
		self.time.append(time.time()-time1)
		# self.deptime = time2-time1+(time.time()-time2)*(300/self.n)
		time2 = time.time()
		if(cha_num>self.n):
			cha_num = self.n
		for x in range(0,cha_num):
			tem_str = "hahaha"
			key = str(self.h(tem_str))
			tem_c = AES.encrypt(key,tem_str)
			tem_t = self.h(str(tem_c))
		self.deptime = time.time()-time2
		# time2 = time.time()
		# print(time2-time1)
	def decrypt(self,sk,ck,ci):
		ki = AES.decrypt(sk,ck)
		ki = ki.split("0x")
		ki = ki[1:]
		ans = ""
		for count in range(0,len(ki)):
			ans += AES.decrypt("0x"+ki[count],ci[count])
		return ans


	def AuthGen(self):
		self.Mi = []
		self.sigema = []
		tem_T = ""
		time1 = time.time()
		for count in range(0,self.n):
			tem_M = self.H(str(self.Ti[count])+str(count))
			tem_T += str(self.Ti[count])
			self.Mi.append(tem_M)
			self.sigema.append((tem_M*(self.u**self.Ti[count]))**self.sk_real)
		self.t_star = self.h(tem_T)
		self.time.append(time.time()-time1)
		

	def end_init(self):
		ans = str(self.t)
		tem_T = ""
		tem_sigema = ""
		with open("./user/data","w") as f:
			f.write(ans+"_"+str(self.t_star)+"_"+self.sk)
		for count in range(0,self.n):
			tem_T += str(self.Ti[count])
			tem_sigema += str(self.sigema[count])
		ans += "/n"+tem_T+"/n"+tem_sigema
		return ans
	def sub_up(self,z,r1,r2):
		ai = []
		bi = []
		for x in range(0,z):
			ai.append(self.pi1(r1,x,self.n))
			bi.append(self.pi2(r2,x))
		proof = self.get_zr(0)
		# here is a error supposed to be ai[x]
		for x in range(0,z):
			proof += bi[x]*self.Ti[x]
		return proof

class Upload_SSP(Params):
	def first_up(self,U_t_T_sigma,U_name):
		self.time = []
		self.U_name = U_name
		self.check_table = "./check_table"
		self.file_name = "Saved_T"
		self.start()
		self.t = U_t_T_sigma.split("/n")[0]
		check_T = U_t_T_sigma.split("/n")[1]
		check_T = check_T.split("0x")
		check_T = check_T[1:]
		self.U_msg = U_t_T_sigma
		self.n = len(check_T)
		self.sigmas = []
		tem_sigema = U_t_T_sigma.split("/n")[2]

		for x in range(0,int(len(tem_sigema)/len(str(self.u)))):
			self.sigmas.append(tem_sigema[x*len(str(self.u)):(x+1)*len(str(self.u))])


		# if self.if_exit(self.file_name,check_T):
		# 	print("exit")
		# else:
		# 	print("the unique,please upload Ci ans Ck")

	def if_exit(self,file_name,check_T):
		with open(file_name,"r") as f:
			while True:
				saved_T = f.read(len(check_T[0])+2)
				if len(saved_T) == 0:
					return False
				for tem_T in check_T:
					if "0x"+tem_T == saved_T:
						return True

	def C_uni(self,Ci,Ck,file_name):
	
		self.ci = Ci.split("_")
		self.Ck = Ck.encode()
		self.T = []
		tem_T = ""
		time1 = time.time()
		for tem_c in self.ci:
			tem_Ti = str(self.h(str(tem_c.encode())))
			self.T.append(tem_Ti)
			tem_T += tem_Ti
		self.time.append((time.time()-time1)/4)
		self.t_star = self.h(tem_T)
		self.sigma = self.U_msg.split("/n")[2]
		# self.sigma = self.cut(self.sigma,len(str(self.H("a"))))
		with open(self.file_name,"a") as f:
			for tem_T in self.T:
				f.write(tem_T)
		with open(file_name,"w+") as f:
			f.write(self.t+"/n"+str(self.t_star)+"/n"+"".join(self.T)+"/n"+Ck+"/n"+self.sigma+"/n"+Ci)
		with open(self.check_table,"a") as f:
			f.write(str(len(self.T))+"_"+str(self.t_star)+"_"+self.U_name+"><")
		return "".join(self.T)+"/n"+str(self.t_star)

	def C_dep(self,obj_u,U_name,t_star,cha_num):

		# self.z = random.randint(1,self.n)
		if(cha_num>self.n):
			cha_num = self.n
		self.z = cha_num
		self.r1 = self.ran_zr()
		self.r2 = self.ran_zr()

		proof = obj_u.sub_up(self.z,self.r1,self.r2)
	
		ai = []
		bi = []
		self.Mi = []
		time1 = time.time()
		for count in range(0,self.z):
			tem_M = self.H(str(self.T[count])+str(count))
			self.Mi.append(tem_M)
		
		for x in range(0,self.z):
			ai.append(self.pi1(self.r1,x,self.n))
			bi.append(self.pi2(self.r2,x))
		# print(ai)
		left = self.get_G1_zero()
		right = self.get_G1_zero()
		for x in range(0,self.z):
			left *= self.get_G1(self.sigmas[x])**bi[x]
			right *= self.Mi[x]**bi[x]
		right *= self.u**proof
		judge = self.e(left,self.g) == self.e(right,self.get_G2(self.t))
		self.time.append(time.time()-time1)
		if judge:
			with open(self.check_table,"a") as f:
				f.write(str(self.n)+"_"+str(self.t_star)+"_"+U_name+"><")
		return judge


	def cut(self,obj,sec):
		return [obj[i:i+sec] for i in range(0,len(obj),sec)]
		
def main(filename,cha_num):
	my_upload = Upload_U(filename,1024*4)
	my_upload.encrypt(cha_num)
	my_upload.AuthGen()
	U_msg = my_upload.end_init()
	SSP = Upload_SSP()
	SSP.first_up(U_msg,"U1")
	
	SSP.C_uni("_".join(my_upload.ci),my_upload.Ck.decode(),"./save/1.txt")

	# print(SSP.T[1] == str(my_upload.Ti[1]))
	# print("/n")
	
	SSP.C_dep(my_upload,"U1",my_upload.t_star,cha_num)
	timeuni = my_upload.time[1:3]+SSP.time[0:1]
	timedep = []
	timedep.append(my_upload.deptime)
	timedep.append(SSP.time[1])
	# timeuni = timeuni[0]+timeuni[1]
	return timeuni[0]+timeuni[1],timeuni[2],timedep[0],timedep[1]



if __name__ == '__main__':
	print(main("./time/upload/1M",300))

	
	