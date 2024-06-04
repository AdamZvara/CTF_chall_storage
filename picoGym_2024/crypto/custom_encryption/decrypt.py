def generator(g, x, p):
    return pow(g, x) % p

def dynamic_xor_encrypt(plaintext, text_key):
    cipher_text = ""
    key_length = len(text_key)
    for i, char in enumerate(plaintext[::-1]):
        key_char = text_key[i % key_length]
        encrypted_char = chr(ord(char) ^ ord(key_char))
        cipher_text += encrypted_char
    return cipher_text

def dynamic_xor_decrypt(plaintext, text_key):
    cipher_text = []
    key_length = len(text_key)
    for i, char in enumerate(plaintext):
        key_char = text_key[i % key_length]
        encrypted_char = chr(ord(char) ^ ord(key_char))
        cipher_text.insert(0, encrypted_char)
    return "".join(cipher_text)

def decrypt(plaintext, key):
    cipher = []
    for char in plaintext:
        cipher.append(chr((char // (key*311))))
    return cipher

def encrypt(plaintext, key):
    cipher = []
    for char in plaintext:
        cipher.append(((ord(char) * key*311)))
    return cipher

a = 97
b = 22
cipher = [151146, 1158786, 1276344, 1360314, 1427490, 1377108, 1074816, 1074816, 386262, 705348, 0, 1393902, 352674, 83970, 1141992, 0, 369468, 1444284, 16794, 1041228, 403056, 453438, 100764, 100764, 285498, 100764, 436644, 856494, 537408, 822906, 436644, 117558, 201528, 285498]

p = 97
g = 31
print(f"a = {a}")
print(f"b = {b}")

u = generator(g, a, p)
v = generator(g, b, p)
key = generator(v, a, p)
b_key = generator(u, b, p)
shared_key = None
if key == b_key:
    shared_key = key
else:
    print("Invalid key")
    exit(1)

print(u, v, key, b_key, shared_key)

semi_decipher = decrypt(cipher, shared_key)
print(semi_decipher)

plaintext = dynamic_xor_decrypt(semi_decipher, "trudeau")
print(f'plaintext is: {plaintext}')

semi_cipher = dynamic_xor_encrypt("hello world", "trudeau")
cipher = encrypt(semi_cipher, shared_key)
print(f'cipher is: {cipher}')
