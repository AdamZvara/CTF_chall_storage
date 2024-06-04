import string

LOWERCASE_OFFSET = ord("a")
ALPHABET = string.ascii_lowercase[:16]

def b16_encode(plain):
	enc = ""
	for c in plain:
		binary = "{0:08b}".format(ord(c))
		enc += ALPHABET[int(binary[:4], 2)]
		enc += ALPHABET[int(binary[4:], 2)]
	return enc

def b16_decode(enc):
	plain = ""
	for c in range(0, len(enc), 2):
		f, s = enc[c], enc[c+1]
		f_idx, s_idx = ALPHABET.index(f), ALPHABET.index(s)
		f_idx = f_idx << 4
		f_idx += s_idx
		plain += chr(f_idx)
	return plain

def shift(c, k):
	t1 = ord(c) - LOWERCASE_OFFSET
	t2 = ord(k) - LOWERCASE_OFFSET
	return ALPHABET[(t1 + t2) % len(ALPHABET)]

def unshift(c, k):
	t1 = ord(c) - LOWERCASE_OFFSET
	t2 = ord(k) - LOWERCASE_OFFSET
	return ALPHABET[(t1 - t2)]

flag = "mlnklfnknljflfjljnjijjmmjkmljnjhmhjgjnjjjmmkjjmijhmkjhjpmkmkmljkjijnjpmhmjjgjj"
key = "c"
assert all([k in ALPHABET for k in key])
assert len(key) == 1

# b16 = b16_encode(flag)
# print(b16)

# enc = ""
# for i, c in enumerate(b16):
# 	enc += shift(c, key[i % len(key)])
# print(enc)

for a in ALPHABET:
	key = a
	dec = ""
	for i, c in enumerate(flag):
		dec += unshift(c, key[i % len(key)])

	res = b16_decode(dec)
	print(res)