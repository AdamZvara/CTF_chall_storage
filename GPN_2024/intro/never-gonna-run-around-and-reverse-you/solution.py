from binascii import unhexlify

with open("hash", "r") as f:
    flag = f.read().strip()

flag = unhexlify(flag)

solved = "G"

for i in range(len(flag)-1):
    solved += chr(flag[i] ^ flag[i-1])

print(solved)