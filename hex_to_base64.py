import string, base64, sys


def hexToBase64(hex):
	#return a base64 encoded bytearray from a hex value
	return base64.b64encode(bytes.fromhex(hex))

def main():
	hex = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
	print("\nHex value:", hex)
	result = hexToBase64(hex)
	print("\nBase64 encoded:", result)
	
if __name__ == "__main__":
	if len(sys.argv) == 1:
		main()
	else:
		print("\nInvalid number of arguments")
		print("Example: python hex_to_base64.py")
		sys.exit()