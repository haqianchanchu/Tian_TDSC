from upload import *
import os
class download_u(Upload_U):
	"""docstring for download"""
	def __init__(self, user_file,filesize):
		filename = ""
		super(download_u, self).__init__(filename,filesize)
		self.user_file = user_file
	def down(self):
		with open(self.user_file,"r") as f:
			tem_msg = f.read()
		self.t = tem_msg.split("_")[0]
		self.t_star = tem_msg.split("_")[1]
		self.sk = tem_msg.split("_")[2]
		return self.t+"/n"+self.t_star
	def end(self,ck,c):
		# print(ck)
		# print("".join(c.split("_")))
		time1 = time.time()
		ans = self.decrypt(self.sk,ck,c.split("_"))
		return time.time()-time1
		# return ans

class download_SSP(object):
	"""docstring for download_SSP"""
	def check(self,check_msg,filename):
		files = []
		for tem_file in os.walk(filename):
			files.append(tem_file)
		files_head = files[0][0]
		files = files[0][2]

		for tem_file in files:
			with open(files_head+"/"+tem_file,"r") as f:
				ans = f.read(len(check_msg))
			if ans == check_msg:
				with open(files_head+"/"+tem_file,"r") as f:
					return f.read()

		return ""


		

def main():
	dow_u = download_u("./user/data",1024)
	check_msg = dow_u.down()
	dow_SSP = download_SSP()
	SSP_msg_ck = dow_SSP.check(check_msg,"./save").split("/n")[3]
	SSP_msg_ci = dow_SSP.check(check_msg,"./save").split("/n")[5]
	ans = dow_u.end(SSP_msg_ck,SSP_msg_ci)
	return ans


if __name__ == '__main__':
	print(main())

