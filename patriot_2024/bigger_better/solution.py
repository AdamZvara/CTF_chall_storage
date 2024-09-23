'''
Created on Dec 14, 2011

@author: pablocelayes
'''

import ContinuedFractions, Arithmetic
from Crypto.Util.number import long_to_bytes

def hack_RSA(e,n,c):
    '''
    Finds d knowing (e,n)
    applying the Wiener continued fraction attack
    '''
    _, convergents = ContinuedFractions.rational_to_contfrac(e, n)

    for (k,d) in convergents:

        #check if d is actually the key
        if k!=0 and (e*d-1)%k == 0:
            phi = (e*d-1)//k
            s = n - phi + 1
            # check if the equation x^2 - s*x + n = 0
            # has integer roots
            discr = s*s - 4*n
            if(discr>=0):
                t = Arithmetic.is_perfect_square(discr)
                if t!=-1 and (s+t)%2==0:
                    return d

with open("dist.txt", "r") as f:
    N = int(f.readline().strip().split('=')[1], 16)
    e = int(f.readline().strip().split('=')[1], 16)
    c = int(f.readline().strip().split('=')[1], 16)

d = hack_RSA(e, N, c)
ptext = pow(c, d, N)
print(long_to_bytes(ptext))

