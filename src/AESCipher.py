from Crypto.Cipher import AES
from Crypto import Random
import os

BLOCKLENGTH = 16
pad = lambda s: s + (BLOCKLENGTH - len(s) % BLOCKLENGTH) * chr(BLOCKLENGTH - len(s) % BLOCKLENGTH) 
unpad = lambda s : s[0:-ord(s[-1])]

def add_hex(hex1, hex2):
    return str(hex(int(hex1, 16) + int(hex2, 16)))[2:34].decode("hex")

class AESCipher:
    def __init__(self, key):        
        self.key = key.decode("hex")

    def decryptCBC(self,enc):        
        enc = enc.decode("hex")
        iv = enc[:16]
        enc = enc[16:]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt( enc))

    def encryptCTR(self, raw):
        # raw = pad(raw)
        secret = os.urandom(16)
        cipher = AES.new(self.key, AES.MODE_CTR, counter = lambda:secret)
        return (secret + cipher.encrypt(raw)).encode("hex")     

    def decryptCTR(self, enc):                
        nblocks = len(enc)/BLOCKLENGTH
        ORIGINAL = enc.decode("hex")        
        enc = enc.decode("hex")
        secret = enc[:BLOCKLENGTH]                   
        result = ""

        for i in xrange(1,nblocks):                        
            nextblockStart = BLOCKLENGTH*i
            nextblockEnd = nextblockStart + BLOCKLENGTH
            enc = ORIGINAL[nextblockStart:nextblockEnd]                    
            cipher = AES.new(self.key, AES.MODE_CTR, counter = lambda:add_hex(secret.encode("hex"),hex(i-1)))            
            result += cipher.decrypt(enc)

        return result

def onetwo():
    cbcCipher = AESCipher('140b41b22a29beb4061bda66b6747e14')
    print "1. " + cbcCipher.decryptCBC('4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81')
    print "2. " + cbcCipher.decryptCBC('5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253')

def threefour():
    ctrCipher = AESCipher('36f18357be4dbd77f050515c73fcf9f2')
    print "3. " + ctrCipher.decryptCTR('69dda8455c7dd4254bf353b773304eec0ec7702330098ce7f7520d1cbbb20fc388d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97ef79d59ce29f5f51eeca32eabedd9afa9329')
    print "4. " + ctrCipher.decryptCTR('770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca695ae45faa8952aa0e311bde9d4e01726d3184c34451')

if __name__ == "__main__":
    onetwo()
    threefour()
