from random import randint
from itertools import chain, combinations

# Get the flag
with open('output.txt') as f:
    flag = bytes.fromhex(f.read())
print("original: ", flag)

def encrypt(ptxt, key):
    ctxt = b''
    for i in range(len(ptxt)):
        a = ptxt[i]
        b = key[i % len(key)]
        ctxt += bytes([a ^ b])
    return ctxt

# Get all possible XORs
def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

random_strs = [
    b'my encryption method',
    b'is absolutely impenetrable',
    b'and you will never',
    b'ever',
    b'break it'
]

x = list(powerset(random_strs))

ctxts = []
for poss in x:
    tmp = flag
    for random_str in poss:
        tmp = encrypt(tmp, random_str)
    ctxts.append(tmp)

for j in ctxts:
    print(encrypt(j, b'picoCTF{'))

# Found Africa! key

for j in ctxts:
    print(encrypt(j, b'Africa!'))