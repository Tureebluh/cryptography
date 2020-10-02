import sys, base64, datetime

def main():
	blocksize = 16 #number of bytes in AES block
	blocks = set() #set has O(1) access time and prevents duplicates
	
	with open("./resources/8.txt") as f:
		print("\nOpening file and beginning analysis...")
		begin = datetime.datetime.now()
		i = 1 #keep track of what line we're on
		
		#loop through each line of the file
		for line in f:
			blocks = set() #reinitialize to an empty set
			
			#break line into chunks of blocksize
			for k in range(0, len(line), blocksize):
				block = line[k:k+blocksize]
				#if true we have a matching block
				if block in blocks:
					end = datetime.datetime.now()
					elapsed = end - begin
					print("---Aborting Analysis---")
					print("Duplicate block detected on line", i, "with block:", block)
					print("Total elapsed time:", elapsed.microseconds / 1000, "ms")
					sys.exit()
				#otherwise add block to set and continue to next
				else:
					blocks.add(block)
			i+=1
if __name__ == '__main__':
	main()