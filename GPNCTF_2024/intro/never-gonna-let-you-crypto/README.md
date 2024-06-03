# Description

You read the title and thought Blockchain? You were successfully baited. 
Like the people before you, you now have to solve this challenge.

# Solution
We are given encryption file in python and encrypted flag = `d24fe00395d364e12ea4ca4b9f2da4ca6f9a24b2ca729a399efb2cd873b3ca7d9d1fb3a66a9b73a5b43e8f3d`

Encryption file:
```python
import os
def encrypt(message,key):
    message = message.encode()
    out = []
    for i in range(len(message)):
        out+= [message[i]^key[i%len(key)]]
    return bytes(out).hex()
FLAG = "GPNCTF{fake_flag}"
key = os.urandom(5)

print(encrypt(FLAG,key))
```

This is a XOR cipher … we know the beginning of the plaintext (`GPNCTF{`) and the ciphertext. We also know that the key is 
5B long so we can XOR the plaintext and the ciphertext to recover the key and use it to get the full flag. Then use the
flag to decypher the rest:
```python
key = "GPNCTF".encode()

def decrypt(message):
    message = bytes.fromhex(message)
    out = []
    for i in range(len(message)):
        out+= [message[i]^key[i%len(key)]]
    return bytes(out)

with open("flag.enc") as f:
    flag = f.read().strip()
    key = decrypt(flag)[0:5]

print(decrypt(flag).decode())
```
