import urllib2
import sys
import traceback

def xor_padding(hex1, npad):        
    new = hex1[:len(hex1)-npad]        
    aux = ''
    for i in xrange(1,npad+1):                              
        aux += chr((ord(hex1[len(hex1)-i]) ^ npad))                 
    new += aux[::-1]    
    return new    
def xor_guess(hex1,guess,npad):        
    new = hex1[:len(hex1)-npad]            
    new += chr((ord(hex1[len(hex1)-npad]) ^ guess))
    new += hex1[len(hex1)-npad+1:]        
    return new
def assign_bytesfound(hex1):    
    new = hex1[:len(hex1)-len(bytesFound)]    
    aux =  hex1[len(hex1)-len(bytesFound):]       
    for i in xrange(1,len(bytesFound)+1):                
        new += chr(ord(bytesFound[len(bytesFound) - i]) ^ ord(aux[i-1]))
    return new
#--------------------------------------------------------------
# padding oracle
#--------------------------------------------------------------
class PaddingOracle(object):

    def guess(self,firstAssignment,paddingByte,guessByte):                
        q = xor_guess(firstAssignment,guessByte,paddingByte)         
        q = xor_padding(q,paddingByte)                               
        new = CIPHERTEXT[:len(CIPHERTEXT)-32]
        new += q
        new += CIPHERTEXT[len(CIPHERTEXT)-16:]                   
        return new.encode('hex')
                    

    def query(self,q,j):                                             
        target = TARGET + urllib2.quote(q)    # Create query URL
        req = urllib2.Request(target)         # Send HTTP request to server
        try:
            f = urllib2.urlopen(req)          # Wait for response
        except urllib2.HTTPError, e:          
           # print "We got: %d" % e.code       # Print response code
            if e.code == 404:
                print j    
                print i
                print chr(j)                                                        
                bytesFound.append(chr(j))                
                return True # good padding
            return False # bad padding

if __name__ == "__main__":       
    try:
        TARGET = 'http://crypto-class.appspot.com/po?er='
        CIPHERTEXT_ORIGINAL = 'f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4'
        CIPHERTEXT_ORIGINAL = CIPHERTEXT_ORIGINAL.decode('hex')    
        bytesFound = []
        res = ''
        po = PaddingOracle()                   
        nblocks = (len(CIPHERTEXT_ORIGINAL)/16) - 1   
        nblocks = 1
        count = 1
        for k in xrange(0,nblocks):                    
            bytesFound = []          
            CIPHERTEXT = CIPHERTEXT_ORIGINAL[:len(CIPHERTEXT_ORIGINAL) - k*16]                             
            bytesFound = [chr(9),chr(9),chr(9),chr(9),chr(9),chr(9),chr(9),chr(9),chr(9)]                 
            for i in xrange(10,17):                
                firstAssignment = assign_bytesfound(CIPHERTEXT[len(CIPHERTEXT)-32:len(CIPHERTEXT)-16])                                                     
                for j in xrange(count,256):                                                                             
                    q = po.guess(firstAssignment,i,j)                                                                    
                    if(po.query(q,j)):                
                        break        
        # print len(res)
        # print res[::-1]                        
    except Exception as ex:
            template = "An exception of type {0} occured. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            traceback.print_exc()
            print message           
            quit()                    
