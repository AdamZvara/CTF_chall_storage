from pwn import *

# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    return remote(sys.argv[1], sys.argv[2], *a, **kw)

# Start program
io = start()

# Get the ciphered flag
cflag = io.recvuntil(b'? ').split()[10]
print(cflag)

# Send so many bytes, that we overflow the key and start again
key_file_size = 50000
flag_len = 32
input_symbol = b'a'
io.send(((key_file_size - flag_len) * input_symbol) + b'\n')
io.recvuntil(b'? ')

# Send a message of 32 * 'a' symbols so we can leak the keystream
inseq = flag_len * input_symbol
io.send(inseq + b'\n')
keystream = io.recvuntil(b'? ').split(b'\n')[1]
keystream = keystream.decode('utf8')
print(keystream)

# Convert keystream into list of integers
kstream = []
for a in range(0, len(keystream), 2):
    kstream.append(int(keystream[a:a+2], 16))

# Calculate the key
key = [a ^ b for a, b in zip(kstream, inseq)]

print("key:", key)

cflag2 = []
for a in range(0, len(cflag), 2):
    cflag2.append(int(cflag[a:a+2], 16))

plaintext = list(map(lambda p, k: chr(p ^ k), cflag2, key))
print("".join(plaintext))