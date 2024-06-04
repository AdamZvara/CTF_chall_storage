from pwn import *


# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    return remote(sys.argv[1], sys.argv[2], *a, **kw)

# Start program
io = start()

flag = b"picoCTF{"

io.sendlineafter(b': ', flag)
io.recvline()
io.recvline()
length = int(io.recvline().decode().strip())

symbols = b"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_{}"

while True:
    for s in symbols:
        io.sendlineafter(b': ', flag + bytes([s]))
        io.recvline()
        io.recvline()
        new_length = int(io.recvline().decode().strip())
        if new_length == length:
            flag += bytes([s])
            print(flag)
            break
