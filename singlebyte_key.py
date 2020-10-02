import string, sys

def scoreResult(buffer):
	#english character frequency analysis values
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
	#add together the score of each character in the buffer and return the total
	return sum([statisticalFreq.get(chr(byte), 0) for byte in buffer.lower()])

def stringXOR(buffer, char):
	#create bytearray from hex string
	temp = bytes.fromhex(buffer)
	result = b''
	#perform XOR comparison on each character in the buffer and append to result
	for byte in temp:
		result += bytes([byte ^ char])
	return result

def main():
	buffer = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
	print("\nBuffer hex value:", buffer)
	results = []
	#iterate through each character value and XOR against the buffer
	for i in range(256):
		resultXOR = stringXOR(buffer, i)
		#score the line using character frequency analysis to determine most likely key
		resultScore = scoreResult(resultXOR)
		data = {
			"index": i,
			"text": resultXOR,
			"score": resultScore
		}
		#store data object inside results array
		results.append(data)
	#sort results by score DESC	
	sortedResults = sorted(results, key=lambda p: p['score'], reverse=True)
	#print the top 5 most likely single byte keys and the corresponding plaintext for human analysis
	print('\n------ Top 5 Results ------')
	for i in range(5):
		print('\nCharacter:',chr(sortedResults[i]['index']), 'with a score of', sortedResults[i]['score'])
		print('Decrypted Message:', sortedResults[i]['text'])
	
	sys.exit()
	
if __name__ == "__main__":
	length = len(sys.argv)
	if length == 1:
		main()
	else:
		print("\nInvalid number of arguments")
		print("Example: python singlebyte_key.py")
		sys.exit()