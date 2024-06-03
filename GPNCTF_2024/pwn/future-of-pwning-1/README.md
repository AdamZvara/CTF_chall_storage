# Description

There's this cool new forward compatible ISA. I created an online emulator so that you can try it out!

# Solution

We are given a bunch of files - TLDR; this challenge is about exploring the [forwardcom](https://github.com/ForwardCom) language,
which is kinda like an assembly. The goal is to read the flag at `/flag`. Before diving in, take a look at the [manual](https://github.com/ForwardCom/manual/raw/master/forwardcom.pdf),
which has been useful when doing this challenge. 

First, since I don't know anything about the language but know some assembly, lets try to look for some already written code
to see what and how to run it. I found this [code-examples](https://github.com/ForwardCom/code-examples) page ... let's take a 
look at `hello.as`:
```
extern _puts: function                           // library function: write string to stdout

const section read ip                            // read-only data section
hello: int8 "\nHello ForwardCom world!", 0       // char string with terminating zero
const end

code section execute                             // executable code section

_main function public                            // program start

// breakpoint                                    // uncomment this if you want to wait for user to press run

int64 r0 = address([hello])                      // calculate address of string
call _puts                                       // call puts. parameter is in r0
int r0 = 0                                       // program return value
return                                           // return from main

_main end

code end
```

Looks pretty much like normal assembly .. but we have `.as` file, how do we get executable? We must compile and link it .. 
in order to do that, we must download the [libraries](https://github.com/ForwardCom/libraries). Then we are ready to go:
```shell
./forw -ass hello.as
./forw -link hello.ex hello.ob libraries/libc_light.li libraries/libc.li libraries/math.li
./forw -emu hello.ex
```

We can run it directly with the emulator which has been provided with the challenge (locally) to get the expected output.

<img width="334" alt="Untitled" src="https://github.com/AdamZvara/CTF/assets/36104483/2cf355ce-63da-4ed7-b718-6dafeb1f5b2a">

Another way is to use the website which runs it for you

<img width="158" alt="Untitled (2)" src="https://github.com/AdamZvara/CTF/assets/36104483/799927bf-4225-48d8-bb68-decd10e42e79">

Since the libraries offer most of normal unix functions (like fopen, fread and print) we can use calls to these functions to 
open the flag file, read it and print to user output. The code is not so complicated:
```
extern _puts: function
extern _fopen: function
extern _fread: function

const section read ip                            // read-only data section
    filename: int8 "/flag", 0
    filemode: int8 "r", 0
    formatstring: int8 "flag: %s", 0
const end

bss section datap uninitialized                  // uninitialized read/write data section
    int8 buf[100]
    int64 parlist[4]
bss end

code section execute

_main function public

    int64 r0 = address([filename])
    int64 r1 = address([filemode])
    call _fopen

    int64 r3 = r0
    int64 r0 = address([buf])
    int64 r1 = 8
    int64 r2 = 99
    call _fread

    int64 r0 = address([buf])
    call _puts

    return

_main end

code end
```

The only thing to look out for is when I tried to actually use the printf function it failed on the server side for some reason.
Although it worked locally ... so I just switched to puts instead and got the result.

<img width="282" alt="Untitled (1)" src="https://github.com/AdamZvara/CTF/assets/36104483/5554a0e4-e6e1-44bf-9769-09273886eda1">

