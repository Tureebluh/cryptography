import string, sys

def stringXOR(buffer1, buffer2):
	#create byte array from hex encoded string
	temp1 = bytes.fromhex(buffer1)
	temp2 = bytes.fromhex(buffer2)
	#XOR compare on the two buffers and return a new bytearray
	return bytes([a ^ b for a, b in zip(temp1, temp2)])
	
def getMaxLength(buffer1, buffer2):
	#store the length of each buffer
	bufOneLen = len(buffer1)
	bufTwoLen = len(buffer2)
	#compare the lengths and return the greater as an int
	if bufOneLen > bufTwoLen:
		return int(bufOneLen)
	else:
		return int(bufTwoLen)

def main():
	#declare buffers
	buffer1 = "1c0111001f010100061a024b53535009181c"
	buffer2 = "686974207468652062756c6c277320657965"
	
	#get maxlength of buffer
	max = getMaxLength(buffer1, buffer2)
	
	#left justify each buffer and add 0's for padding if less than max
	buffer1 = buffer1.ljust(max, "0")
	buffer2 = buffer2.ljust(max, "0")
	
	#perform XOR comparison between buffers
	result = stringXOR(buffer1, buffer2)

	#print the starting buffer hexstrings
	print("\nBuffer 1:", buffer1)
	print("Buffer 2:", buffer2)
	print("\n")
	print("*" *50)
	print("Results")
	print("*" *50)
	#print the hex encoded result
	print("Hex: " + result.hex())
	#print the result bytearray
	print(result)
	
	sys.exit()
	
if __name__ == "__main__":
	length = len(sys.argv)
	if length == 1:
		main()
	else:
		print("\nInvalid number of arguments")
		print("Example: python xor_buffers.py")
		sys.exit()