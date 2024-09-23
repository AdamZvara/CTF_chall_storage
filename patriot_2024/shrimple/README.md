# Description

Peel back the shell, unless you eat shrimp with the shell.

# Solution

We get a 64b binary called shrimple, which essentially reads the input from the user and concatenates it to a buffer. However it uses
a small and calls strncat with big enough size to overflow it. We can use this to overwrite the return address and jump to the win function `shrimp`. However, there is a catch ... The address of the win function is `0x000000000040127d` and the original return address is `0x7ffff7deec8a`. Since the app uses strncat, which stops after null byte, we need to find a way to nullify the return address. Fortunatelly, we are able to overflow the buffer 3 times, which is barely enough to nullify the return address.

In the first overflow we set the highest byte, then the second highest (0x0000XXXXXXXX) and in the run we set the lower part of the address to 0040127d. I found the offset by running the app and inserting cyclic string, then searching for the part which overwrites the return address. The by trial and error I set the rest of the bits and got the payload to work locally. However, this payload
did not work remotely, so I just tried increasing the return address by some amount (alignment problems or something like that) and after trial and error got the correct solution.

The whole payload is in `pwn_template.py`