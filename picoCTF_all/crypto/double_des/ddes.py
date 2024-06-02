#!/usr/bin/python3 -u
from Crypto.Cipher import DES
from pwn import *
import binascii
import itertools
import string

# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    return remote(sys.argv[1], sys.argv[2], *a, **kw)

def pad(msg):
    block_len = 8
    over = len(msg) % block_len
    pad = block_len - over
    return (msg + " " * pad).encode()

# Start program
io = start()

io.recvline()
flag = io.recvline().decode().strip()

# Try all possible keys
keys = []
for i in itertools.product(string.digits, repeat=6):
    keys.append(pad("".join(i)))

my_input = '11223344556677'
io.send(my_input)
io.send(b"\n")

my_input_enc = io.recvline().decode().strip().split(' ')[-1]
print("Encrypted input:", my_input_enc)

my_input = binascii.unhexlify(my_input).decode()
input_enc = binascii.unhexlify(my_input_enc)

ciphers1 = {}
for key in keys:
    cipher1 = DES.new(key, DES.MODE_ECB)
    enc_msg = cipher1.encrypt(pad(my_input))
    enc_msg = binascii.hexlify(enc_msg).decode()
    ciphers1[enc_msg] = key

print("Generated all possible ciphertexts for first key")

keys_final = None
for key in keys:
    cipher1 = DES.new(key, DES.MODE_ECB)
    enc_msg = cipher1.decrypt(input_enc)
    enc_msg = binascii.hexlify(enc_msg).decode()
    if enc_msg in ciphers1:
        print("Key2 found:", key)
        print("Key1 found:", ciphers1[enc_msg])
        keys_final = (ciphers1[enc_msg], key)
        break

# Decrypt flag
c = DES.new(keys_final[1], DES.MODE_ECB)
flag = c.decrypt(binascii.unhexlify(flag))
c2 = DES.new(keys_final[0], DES.MODE_ECB)
flag = c2.decrypt(flag)
print(flag)
