import string, sys

def cipher_xor(msg, key):
	results = ""
	#perform XOR comparison iterating through each index in the msg and key
	for i in range(len(msg)):
		#modulo always returns back a whole number
		#modulo always returns back i when i is less than the len of key
		results += chr(msg[i] ^ key[i%len(key)])
	return bytes(results, 'utf-8')

def main():
	#create a bytearray of the plaintext
	plaintext = "Burning 'em, if you ain't quick and nimble I go crazy when I hear a cymbal"
	msg = bytearray(plaintext, "utf-8")
	#create a bytearray of the key - ICE
	key = bytearray("ICE", "utf-8")
	
	#print the original plaintext and key
	print("\nOriginal plain-text:", plaintext)
	print("Key:", key)

	#encrypt the plaintext with the key and print the cipher
	cipher = cipher_xor(msg, key)
	print("\nCipher-text: ", cipher)
	
	#verify proper encryption by decrypting the cipher with the key
	#print the decrypted plain-text
	cipher = cipher_xor(cipher, key)
	print("Decrypted plain-text: ", cipher)
	
	sys.exit()
	
if __name__ == "__main__":
	if len(sys.argv) == 1:
		main()
	else:
		print("\nInvalid number of arguments")
		print("Example: repeating_key_xor.py")
		sys.exit()