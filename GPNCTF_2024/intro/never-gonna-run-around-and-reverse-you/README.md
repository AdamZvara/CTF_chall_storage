# Description

I thought of this really cool collision free hash function and hashed the flag with it. Theoretically you shouldn't be able to reverse it...

# Solution

We are given a binary file and a hash file and the goal is to reverse the hash and get the flag. The hash is 
`4717591a4e08732410215579264e7e0956320367384171045b28187402316e1a7243300f501946325a6a1f7810643b0a7e21566257083c63043404603f5763563e43`.

After opening the binary in ghidra I found out that this function is responsible for creating the hash:

<img width="328" alt="Untitled (3)" src="https://github.com/AdamZvara/CTF/assets/36104483/aed9b469-5099-439c-bafa-0bcbad6d6b37">

The function is really simple: first, it copies the flag into new buffer and then each letter (apart from the first) is 
XORed with the previous letter. I’ve made this little python script to get the flag from the hash file
```python
from binascii import unhexlify

with open("hash", "r") as f:
    flag = f.read().strip()

flag = unhexlify(flag)

solved = "G"

for i in range(len(flag)-1):
    solved += chr(flag[i] ^ flag[i-1])

print(solved)
```
