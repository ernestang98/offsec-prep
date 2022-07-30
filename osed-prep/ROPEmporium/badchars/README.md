# Badchars

Objective:

Basically same as write4 but you cannot use 'x', 'g', 'a', '.', hence you can't hardcode the string "flag.txt". Use a xor function to convert the flag.txt into some other byte string without 'a', 'g', and '.'. After storing it appropriately in .data section as we did in write4, we will write an exploit that will iterate over each byte of the xor-ed flag.txt and convert it back to its normal form.

Security:

|RELRO|STACK CANARY|NX|PIE|RPATH|RUNPATH|Symbols|FORTIFY|Fortified|Fortifiable|FILE|ASLR|
|-|-|-|-|-|-|-|-|-|-|-|-|
|Partial RELRO|No canary found|NX enabled|No PIE|No RPATH|No RUNPATH|72) Symbols|No|0|3|ret2win32|ASLR Disabled|