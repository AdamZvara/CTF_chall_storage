# Description

Exciting news! Our chief scientists found a way to do frequency analysis on binary files. Surprinsingly it isn't just 
changing the file ending to .mp3 and putting it into Audacity. Have a try for yourself below!

Note: The binary `/catflag` prints the flag

Hint: This challenge is about ELF Binaries (Linux executables)

# Solution
We have access to a website which prints out information about binary file (something like frequency analysis of used 
libraries and stuff). The goal is to execute the `/catflag` file. Let’s try and upload some binary file from other challs:

<img width="592" alt="Untitled (3)" src="https://github.com/AdamZvara/CTF/assets/36104483/c7d0a789-ec76-4303-b4ac-6254edda49e1">

Based on the names of the library files we can assume, that the analysis tool uses ldd to fetch the libraries. From the `man ldd` 
we can see that:
```
Be  aware that in some circumstances (e.g., where the program specifies an ELF interpreter other than ld-linux.so), some versions of
ldd may attempt to obtain the dependency information by attempting to directly execute the program, which may lead to the
execution of whatever code is defined in the program's ELF interpreter, and perhaps to execution of the program itself.
(Before glibc 2.27, the upstream ldd implementation did this for  example, although most distributions provided a modified version that did not.)
```

Interesting .. so if we set the interpreter to some other file, ldd might try to run that file -> let’s set the interpreter of 
our empty binary with `patchelf` to `/catflag` (like this: `patchelf --set-interpreter /catflag bin`). Ipload the file and inspect
the results:

<img width="592" alt="Untitled" src="https://github.com/AdamZvara/CTF/assets/36104483/177c2c7f-a084-489d-b684-7d1a9a83b771">
