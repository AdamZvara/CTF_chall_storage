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


