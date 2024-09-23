from pwn import *
import base64

io = remote("chal.pctf.competitivecyber.club", 9001)

for i in range(1000):
    io.recvuntil(b'Challenge: ')
    chal = io.recvline()

    res = base64.b64decode(chal.strip())
    (chal, iter) = res.split(b'|')

    for _ in range(int(iter)):
        chal = base64.b64decode(chal)

    print(chal.decode() + '|' + str(i))
    io.sendlineafter(b'>> ', chal.decode() + '|' + str(i))

print(io.recvall().decode())