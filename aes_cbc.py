import sys, base64, re
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def addPadding(buffer, blocksize):
	#performs PKCS#7 padding
	remainder = blocksize - (len(buffer) % blocksize)
	padding = b''
	if remainder != 0:
		#pads with byte value N, N times (i.e b'\x05\x05\x05\x05\x05')
		padding = bytes([remainder] * remainder)
	return buffer + padding

def bufferXOR(buffer1, buffer2):
	#performs XOR comparison between two buffers and returns back the result in a bytearray
	return bytes([a ^ b for a, b in zip(buffer1, buffer2)])

def Encrypt_CBC_Mode(buffer, key):
	#encrypt with my own CBC mode encryption implementation
	#CBC mode still utilizes a repeating key encryption
	cipher = AES.new(key, AES.MODE_ECB)
	#add padding to make sure all blocks are equal to the size of the key
	buffer = addPadding(buffer, len(key))
	#initialize the same zero byte valued array as used for the initial encryption. normally you would want this randomized.
	iv = bytearray(len(key))
	output = bytearray()
	#loop through the entire buffer, grabbing block sizes equal to the key
	for i in range(0, len(buffer), len(key)):
		#perform XOR operations on the current block with the IV
		temp = bufferXOR(buffer[i:i+len(key)], iv)
		#now we treat it like ECB mode and XOR against the key, replacing our IV with the returned ciphertext
		iv = cipher.encrypt(temp)
		#and finally add the ciphertext to our output buffer
		output += iv
	#return a new base64 encoded bytearray of the data
	return base64.b64encode(output)

def Decrypt_CBC_Mode(buffer, key):
	#decrypt with standard security library
	#create initialization vector of size equal to length of key with all zero values
	iv = bytearray(len(key))
	cipher = AES.new(key, AES.MODE_CBC, iv)
	#decrypt ciphertext and remove padding if any exist
	plaintext = cipher.decrypt(buffer)
	plaintext = unpad(plaintext, AES.block_size)
	return plaintext


def main():
	#open txt file
	with open("./resources/10.txt") as f:
		#read base64 data from file and remove new lines with regex
		old_cipher = re.sub('[\n]', '', f.read())

		#decode output to remove base64 encoding
		decoded_output = base64.b64decode(old_cipher)

		#initialize bytearray to be used as the key
		key = bytearray("YELLOW SUBMARINE", "utf-8")

		#decrypt decoded ciphertext with created key
		plaintext = Decrypt_CBC_Mode(decoded_output, key)

		#encrypt return plaintext to verify proper decryption
		ciphertext = Encrypt_CBC_Mode(plaintext, key)
		ciphertext = ciphertext.decode("utf-8")

		print("")
		print("ORIGINAL ENCRYPTED VALUE (first 40 chars)")
		print(old_cipher[:40] + "...\n")

		print("")
		print("MY ENCRYPTED VALUE (first 40 chars)")
		
		print(ciphertext[:40] + "...\n")

		print("*"*50)
		print("Are the two ciphers equal?", "Yes" if old_cipher == ciphertext else "No")
		
	sys.exit()
	
if __name__ == '__main__':
	if len(sys.argv) == 1:
		main()
	else:
		print("\nInvalid number of arguments")
		print("Example: python aes_cbc.py")
		sys.exit()