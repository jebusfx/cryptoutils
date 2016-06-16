from gmpy2 import mpz,divm,powmod,f_mod,mul

p=mpz('13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690031858186486050853753882811946569946433649006084171')
g=mpz('11717829880366207009516117596335367088558084999998952205599979459063929499736583746670572176471460312928594829675428279466566527115212748467589894601965568')
h=mpz('3239475104050450443565264378728065788649097520952449527834792452971981976143292558073856937958553180532878928001494706097394108577585732452307673444020333')

hashtableLeft = {}
hashtableRight = {}
rightHandSideValues = []

B = 2**20
possibleXs = 2**20

#Find x1 and x0 for the following equation: h*g^-x1 = g^(B*x0)

if __name__ == "__main__":
	#Build hash tables
	while possibleXs>-1:
		lefthandside = f_mod(mul(h,powmod(g,possibleXs*-1,p)),p)	
		hashtableLeft[str(lefthandside)] = possibleXs

		righthandside = powmod(g,B*possibleXs,p)
		hashtableRight[str(righthandside)] = possibleXs
		rightHandSideValues.append(str(righthandside))	
		possibleXs -= 1	

	for i in xrange(len(rightHandSideValues)):
		try:		
			x = hashtableRight[rightHandSideValues[i]]*B + hashtableLeft[rightHandSideValues[i]] #if a value is in both hashtables we calculate the solution
			print 'Solution: ' + str(x)
		except KeyError:
			continue
