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