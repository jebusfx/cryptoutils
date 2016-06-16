from hashlib import sha256

# def intToHex(s):	
# 	aux = ""
# 	for x in s:				
# 		aux += (str(hex(ord(x)))[2:])
# 	return aux
# def padhexa(s):
#     return s[2:].zfill(16)

KB = 1024

if __name__ == "__main__":
	filePath = "6 - 2 - Generic birthday attack (16 min).mp4"
	f = open(filePath, "rb")

	bytesRead = f.read(KB)	
	bytes = bytesRead
	while bytesRead != "":
		bytesRead = f.read(KB)
		bytes += bytesRead
	f.close()

	h = sha256()
	length = len(bytes)
	n_blocks = length/KB
	newlength = length % KB
	#get the digest of the last block, which may not be multiple of KB
	h.update(bytes[length-newlength:])
	length = length-newlength	
	res = h.digest()

	for i in xrange(n_blocks):			
		h = sha256()
		newlength = length-KB
		h.update(bytes[newlength:length] + res)	
		length = newlength	
		res = h.digest()		
	print res.encode("hex")
