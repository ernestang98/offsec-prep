# Callme

Objective:

Overflow buffer, call callme_one(0xdeadbeef, 0xcafebabe, 0xd00df00d), callme_two(0xdeadbeef, 0xcafebabe, 0xd00df00d), callme_three(0xdeadbeef, 0xcafebabe, 0xd00df00d)

Security:

|RELRO|STACK CANARY|NX|PIE|RPATH|RUNPATH|Symbols|FORTIFY|Fortified|Fortifiable|FILE|ASLR|
|-|-|-|-|-|-|-|-|-|-|-|-|
|Partial RELRO|No canary found|NX enabled|No PIE|No RPATH|No RUNPATH|72) Symbols|No|0|3|ret2win32|ASLR Disabled|

