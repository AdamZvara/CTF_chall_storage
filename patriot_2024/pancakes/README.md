# Description

How many layers are on your pancakes?

# Solution

After connecting to a server we get this message:

```
Welcome to the pancake shop!
Pancakes have layers, we need you to get through them all to get our secret pancake mix formula.
This server will require you to complete 1000 challenge-responses.
A response can be created by doing the following:
1. Base64 decoding the challenge once (will output (encoded|n))
2. Decoding the challenge n more times.
3. Send (decoded|current challenge iteration)
Example response for challenge 485/1000: e9208047e544312e6eac685e4e1f7e20|485
Good luck!

Challenge: Vm0weGQxSXlTWGxWV0doVlltdHdUMVl3VlRGaU1WSlZVMnBTV0ZKdGVIcFpWVnBQWVVaS2MyTkliRmhoTW1neldWUkJlRmRHVm5WaVJtaG9UVmhDYjFaclpEUlpWbHBYVm01R1YySkhVbkJWYWtwdlpWWlplRmR0UmxSaVZscEpWV3hvZDFsV1NuTlhia0phWWxoU1RGWldXbXRXTVZwMFVtMXdUbFp1UWxsV2JUQXhWVEpHYzFOWVpGaGlWR3hoVm10V2RtUXhVbFZTYlVaVFZtdHdlbFpIZUZkVWJVVjRZMFZvVjFKc2NIWldWRVpoVmpGa2NsWnNTbGRTTTAwMXw3
```

The solution is simple:
1. get the current challenge, decode it and get `chall|n`
2. decode `chall` until `n = 0`
3. send the result with the current "round" index
4. repeat 1000 times and get the flag