import upload
import Auth
import Auth_update
import retrive


def main():
	size = "1M"
	max_cha = 500
	with open("./time/upload"+size,"w") as f:
		for x in range(0,max_cha,50):
			f.write(str(upload.main("./files/"+size,x))+"\n")
	with open("./time/Auth"+size,"w") as f:
		for x in range(0,max_cha,50):
			f.write(str(Auth.main(x))+"\n")
	with open("./time/Auth_update"+size,"w") as f:
		f.write(str(Auth_update.main()))
	with open("./time/retrive"+size,"w") as f:
		f.write(str(retrive.main()))

if __name__ == '__main__':
	main()