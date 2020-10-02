import string, sys, base64

def calcHamDistance(buffer1, buffer2):
	#byte array returned from XOR on buffer1 and buffer2
	xorb = bytes(a ^ b for a, b in zip(buffer1, buffer2))
	distance = 0
	#loop through XOR byte array
	for byte in xorb:
		#add hamming distance or the number of differing bits
		#since (0 ^ 0 OR 1 ^ 1) is equal to 0 - 1 must be a differing bit
		distance += sum([1 for bit in bin(byte) if bit == '1'])
	return distance

def scoreResult(buffer):
	#Scores based on ETAOIN SHRDLU - char frequency analysis
	statisticalFreq = {
		'a': .08167, 'b': .01492, 'c': .02782,
		'd': .04253, 'e': .12702, 'f': .02228,
		'g': .02015, 'h': .06094, 'i': .06094,
		'j': .00153, 'k': .00772, 'l': .04025,
        'm': .02406, 'n': .06749, 'o': .07507,
		'p': .01929, 'q': .00095, 'r': .05987,
		's': .06327, 't': .09056, 'u': .02758,
		'v': .00978, 'w': .02360, 'x': .00150,
        'y': .01974, 'z': .00074, ' ': .19500
	}
	#Sum scores for each character in buffer
	return sum([statisticalFreq.get(chr(byte), 0) for byte in buffer.lower()])

def singleCharXOR(buffer, char):
	result = b''
	#loop through bytes in buffer
	for byte in buffer:
		#add result of XOR against single char
		result += bytes([byte ^ char])
	return result

def repeatingKeyXOR(buffer, key):
	results = ""
	#loop through bytes in buffer
	for i in range(len(buffer)):
		#add result of XOR against revolving key characters
		#i.e I C E I C E I C E
		results += chr(buffer[i] ^ key[i%len(key)])
	return bytes(results, 'utf-8')

def bf_singleXOR(buffer):
	results = []
	#loop through possible char values
	for key in range(256):
		#store returned bytes as message for this key
		message = singleCharXOR(buffer, key)
		#store ham distance score
		score = scoreResult(message)
		data = {
			'message': message,
			'score': score,
			'key': key
			}
		#append data and return back the first index of reverse sorted array
		#this is our statistical guess at the key value
		results.append(data)
	return sorted(results, key=lambda p: p['score'], reverse=True)[0]['key']

def bruteforceBlocks(keysize, buffer):
	key = b''
	
	#loop through each index in key
	for i in range(keysize):
		block = b''
		#loop through buffer and add each index from each chunk to an array
		#i.e the first char in each block, 2nd char in each block...etc
		for j in range(i, len(buffer), keysize):
			block += bytes([buffer[j]])
		#bruteforce single char XOR for each block
		key += bytes([bf_singleXOR(block)])
	#return suggested key and decrypted message
	return (repeatingKeyXOR(buffer,key), key)
	
def findKeysize(cipher):
	avgKeyHams = []
	
	#loop through potential key sizes - could be extended
	for keysize in range(2,41):
		distances = []
		
		#break cipher into chunks of bytes equal to the current keysize
		chunks = [cipher[i:i+keysize] for i in range(0, len(cipher), keysize)]
		i = 0
		
		#calculate hamming distance for each sequential chunk
		#break while loop once index out of range is thrown
		#normalize the distance by dividing by the keysize
		while True:
			try:
				distance = calcHamDistance(chunks[i],chunks[i+1])
				distances.append(distance/keysize)
				i+=1
			except Exception as e:
				break
		
		#average the total sum by the number of distances
		result = {
			'key': keysize,
			'distance': sum(distances)/len(distances)
		}
		avgKeyHams.append(result)
	#sort by lowest distance and return the keysize
	return sorted(avgKeyHams, key=lambda p: p['distance'])[0]['key']

def main():
	#open file and decode as base64 string
	with open('./resources/6.txt', 'r') as f:
		result = base64.b64decode(f.read())
	
	#determine most probable keysize by hamming distance
	bestKeysize = findKeysize(result)
	
	#try and bruteforce with suggested keysize
	result, key = bruteforceBlocks(bestKeysize,result)
	
	#Style and print output
	print("\nKey:", key.decode("utf-8"))
	print("\nDecrypted Message:\n\n", result.decode("utf-8"))
	sys.exit()
	
if __name__ == "__main__":
	length = len(sys.argv)
	if length == 1:
		main()
	else:
		print("\nInvalid number of arguments")
		print("Example: repeating_key_crack.py")
		sys.exit()