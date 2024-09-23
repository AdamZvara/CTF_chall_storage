# Description

I spent a couple of hours with ???; now I am the world's best cryptographer!!! note: the flag contents will just random chars-- not english/leetspeak

Cipher Text: `QRVWUFdWEUpdXEVGCF8DVEoYEEIBBlEAE0dQAURFD1I=`

Please wrap the flag with pctf{}.

# Solution

We are given an `encode.py`, with which the ciphertext has been generated. If we look at the source code, we can see
that it still contains the original secret key - therefore we only need to reverse the cipher.

```python
rsv_input = usr_input[::-1]
output_arr = []
for i in range(int(len(usr_input) / 2)):
    c1 = ord(usr_input[i])
    c2 = ord(rsv_input[i])
    enc_p1 = chr(c1 ^ ord(srt_key[i % len(srt_key)]))
    enc_p2 = chr(c2 ^ ord(srt_key[i % len(srt_key)]))
    output_arr.append(enc_p1)
    output_arr.append(enc_p2)
```

This is the core of the encryption and basically it goes over the input from start and end at the same time and XORs the
plaintext with the key. In the end, the result is base64 encoded

```python
b64_enc_val = base64.b64encode(encoded_val.encode())
```

In order to decrypt, we first need to decode it from base64, then go through each pair of letters from the beggining and XOR
them with appropriate key value and place them in correct order (the first letter is from the beginning and the other from the end)

```python3
for i in range(int(len(usr_input) / 2)):
    c1 = ord(usr_input[i])
    c2 = ord(usr_input[i+1])
    enc_p1 = chr(c1 ^ ord(srt_key[i % len(srt_key)]))
    enc_p2 = chr(c2 ^ ord(srt_key[i % len(srt_key)]))
    output_arr.append(enc_p1)
    output_arr2.append(enc_p2)
    usr_input = usr_input[1:]
```

`output_arr2` contains reversed second half of the plaintext, reverse it back and append to the first half to get the flag.