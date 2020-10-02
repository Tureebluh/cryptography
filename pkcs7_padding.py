import sys


def addPadding(buffer, blocksize):
	#determine how many bytes need to padded
	remainder = blocksize - (len(buffer) % blocksize)
	padding = b''
	if remainder != 0:
		#pads with byte value N, N times (i.e b'\x05\x05\x05\x05\x05')
		padding = bytes([remainder] * remainder)
	return buffer + padding

def main():
	#create bytearray from user input
	buffer = bytearray(sys.argv[1], "utf-8")
	print(addPadding(buffer, 16))
		
if __name__ == "__main__": 
	if len(sys.argv) == 2:
		main()
	else:
		print("\nInvalid number of arguments")
		print("Example: python pkcs7_padding.py randomstring")
		sys.exit()