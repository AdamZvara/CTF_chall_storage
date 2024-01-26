#!/usr/bin/python3

from wasmtime import Store, Module, Instance, Memory, MemoryType, Limits
from itertools import product
import string

# Create WASM instance
store = Store()
module = Module.from_file(store.engine, 'assembly4.wat')
instance = Instance(store, module, [])

# Get memory and exported function
assembly4 = instance.exports(store)
mem = assembly4["memory"]
mem_data = mem.data_ptr(store)
check_flag = assembly4["check_flag"]

# Define possible letters and already guessed final flag
possible_letters = string.ascii_lowercase + "_" + string.digits + string.ascii_uppercase + "{" +  "}\x00"
guessed_flag = ""

def count_flag():
    count = 0
    while (mem_data[1024 + count] == mem_data[1072 + count]):
        count += 1
    return count

for (idx, i) in enumerate("pocoCTF{"):
    mem_data[1072 + idx] = ord(i)

check_flag(store)

for (idx, i) in enumerate("picoCTF{"):
    print("original:", mem_data[1024 + idx], "updated:", mem_data[1072 + idx])

def init_flag(guessed, pair):
    for (idx, item) in enumerate(guessed):
        mem_data[1072 + idx] = ord(item)
    mem_data[1072 + len(guessed)] = ord(pair[0])
    mem_data[1072 + len(guessed) + 1] = ord(pair[1])

for idx in range(24): # Iterate through all leftover letters in flag, which are not guessed yet
    for pair in product(possible_letters, repeat = 2): # For each new combination
#        init_flag(guessed_flag, pair)
#        check_flag(store)
        if (count_flag() >= 2 + len(guessed_flag)):
            print(idx, pair)
            guessed_flag += (pair[0] + pair[1]) 
            print(guessed_flag)
            break
