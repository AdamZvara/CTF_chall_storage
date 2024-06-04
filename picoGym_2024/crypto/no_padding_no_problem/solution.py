from pwn import *
from Crypto.Util.number import long_to_bytes

# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    return remote(sys.argv[1], sys.argv[2], *a, **kw)

# Start program
io = start()

io.recvuntil(b'\n\n\n')
n = int(io.recvline().split()[1].strip())
e = int(io.recvline().split()[1].strip())
c = int(io.recvline().split()[1].strip())

io.recvuntil(b': ')

myctext = (pow(2, e, n) * c) % n

print('myctext = ', myctext)

io.send(str(myctext))
io.send(b'\n')
res = int(io.recvline().split()[3].strip())

print("n = ", n)
print("e = ", e)
print("c = ", c)

print("res = ", res)

print(long_to_bytes(res // 2))
