import sys, base64
from Crypto.Cipher import AES

def main():
	#create bytearray of key string
	key = b"YELLOW SUBMARINE"
	cipher = AES.new(key, AES.MODE_ECB)
	#attempt to open file
	with open("./resources/7.txt") as f:
		#read base64 data from file and decode
		output = base64.b64decode(f.read())
		#decrypt using raw byte values
		dec = cipher.decrypt(output)
	#print as utf-8 decoded string
	print(dec.decode("utf-8"))
if __name__ == '__main__':
	main()