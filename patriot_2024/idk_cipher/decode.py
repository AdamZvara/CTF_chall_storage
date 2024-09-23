
import base64

srt_key = 'secretkey' # // TODO: change the placeholder
usr_input = base64.b64decode("QRVWUFdWEUpdXEVGCF8DVEoYEEIBBlEAE0dQAURFD1I=").decode("utf-8")

output_arr = []
output_arr2 = []

for i in range(int(len(usr_input) / 2)):
    c1 = ord(usr_input[i])
    c2 = ord(usr_input[i+1])
    enc_p1 = chr(c1 ^ ord(srt_key[i % len(srt_key)]))
    enc_p2 = chr(c2 ^ ord(srt_key[i % len(srt_key)]))
    output_arr.append(enc_p1)
    output_arr2.append(enc_p2)
    usr_input = usr_input[1:]

output_arr2 = output_arr2[::-1]
result = ''.join(output_arr) + ''.join(output_arr2)
print(f'pctf{{{result}}}')