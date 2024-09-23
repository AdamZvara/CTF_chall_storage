# Description

I heard choosing a small value for e when creating an RSA key pair is a bad idea. So I switched it up!

# Solution
We are given `N`, `e` and `c` (ciphertext). Use wiener attack to get `d` and decrypt the flag.