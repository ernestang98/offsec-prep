# LiveOverflow Binary Exploitation / Memory Corruption

### 0x05: Reversing & Cracking First Program (introduction to GNU Debugger - GDB)

GDB commands:

- Attaches binary to debugger
    
    ```
    gdb BINARY
    ```

- Disassembles function, usually use with main as we know that every C program has a main() function.

    ```
    (gdb) disassemble FUNC
    ```

- Disassemble function with better formatting

    ```
    (gdb) set disassembly-flavor intel
    (gdb) disassemble FUNC
    ```

- Add breakpoints

    ```
    (gdb) break *FUNC
    ```

- Run program (with arguments

    ```
    (gdb) run [ARGS1 ARGS2 ARGS3]
    ```

- Get registers

    ```
    (gdb) info registers
    ```

- Step into next instruction (follow function calls)

    ```
    (gdb) si
    ```

- Step into next instruction (ignore function calls)

    ```
    (gdb) ni
    ```

- Change register values

    ```
    (gdb) set $REGISTER=VALUE
    ```

Disassembled `licence` linux executable

```
0x00000000004005bd <+0>:	push   rbp
0x00000000004005be <+1>:	mov    rbp,rsp
0x00000000004005c1 <+4>:	sub    rsp,0x10
0x00000000004005c5 <+8>:	mov    DWORD PTR [rbp-0x4],edi
0x00000000004005c8 <+11>:	mov    QWORD PTR [rbp-0x10],rsi
0x00000000004005cc <+15>:	cmp    DWORD PTR [rbp-0x4],0x2
0x00000000004005d0 <+19>:	jne    0x400623 <main+102>
0x00000000004005d2 <+21>:	mov    rax,QWORD PTR [rbp-0x10]
0x00000000004005d6 <+25>:	add    rax,0x8
0x00000000004005da <+29>:	mov    rax,QWORD PTR [rax]
0x00000000004005dd <+32>:	mov    rsi,rax
0x00000000004005e0 <+35>:	mov    edi,0x4006c4
0x00000000004005e5 <+40>:	mov    eax,0x0
0x00000000004005ea <+45>:	call   0x400490 <printf@plt>
0x00000000004005ef <+50>:	mov    rax,QWORD PTR [rbp-0x10]
0x00000000004005f3 <+54>:	add    rax,0x8
0x00000000004005f7 <+58>:	mov    rax,QWORD PTR [rax]
0x00000000004005fa <+61>:	mov    esi,0x4006da
0x00000000004005ff <+66>:	mov    rdi,rax
0x0000000000400602 <+69>:	call   0x4004b0 <strcmp@plt>
0x0000000000400607 <+74>:	test   eax,eax
0x0000000000400609 <+76>:	jne    0x400617 <main+90>
0x000000000040060b <+78>:	mov    edi,0x4006ea
0x0000000000400610 <+83>:	call   0x400480 <puts@plt>
0x0000000000400615 <+88>:	jmp    0x40062d <main+112>
0x0000000000400617 <+90>:	mov    edi,0x4006fa
0x000000000040061c <+95>:	call   0x400480 <puts@plt>
0x0000000000400621 <+100>:	jmp    0x40062d <main+112>
0x0000000000400623 <+102>:	mov    edi,0x400701
0x0000000000400628 <+107>:	call   0x400480 <puts@plt>
0x000000000040062d <+112>:	mov    eax,0x0
0x0000000000400632 <+117>:	leave  
0x0000000000400633 <+118>:	ret   
```

- `cmp    DWORD PTR [rbp-0x4],0x2`: compare register/pointer/function to 0x2, if true set ZF to 1 or else set ZF to 0. Reference [here](https://reverseengineering.stackexchange.com/questions/20838/how-the-cmp-instruction-uses-condition-flags)

- `jne 0x400623`: jump to address location 0x400623 if zero flag set to 0. Hence, with respect to the previous instruction, if PTR does not equal to 2 and hence the ZF is 0, then we will jump the address location 0x400623. Reference [here](https://www.aldeid.com/wiki/X86-assembly/Instructions/jnz)

- `call   0x400490 <printf@plt>`: prints statements

- `call 0x4004b0 strcmp@plt`: call strcmp function, compare strings and returns 0 if both strings are the same

- `test eax,eax`: Performs AND operator on eax register and sets ZF to 1 if result is 0

- `jne 0x400617`: jump to address location 0x400617 if zero flag is set to 0. Hence, if the previous `test` instruction does not result to 0, then we will jump to address location 0x40617. 

- `call 0x400480 puts@plt`: call puts function which is similar to printf

Assembly code analysis principles:

- Ignore most of it, focus on only a few instructions/function calls, such as CALL,  CMP, jump-related instructions, STRCMP, TEST

- EAX refers to the first half of the RAX register

Methodology:

1. Set breakpoint at main(), step through the program an instruction at a time

2. Realise that we will jump from 5d0 to 623

3. At 628, we observe "Usage <key>" printed out, which corresponds to the instruction of puts being called at that address location

4. From this, we can deduce we failed the previous `cmp` instruction, and it should be because we did not put in a key. So we will re-run the debugger with a random key

5. On this run, we do not jump from 5d0 to 623 but continue till 5ea where we observe the debugger printing "Checking license: <OUR_INPUT>" which corresponds to the printf instruction we observe in the disassembler

6. On this run, we observe that we jump from 609 to 617 before observing the following statements "WRONG" in the debugger at 61c which corresponds to the assembly instruction puts

7. To bypass the jump from 609 to 617, we need to make the output of the `test eax eax` instruction 0. We can set the $rax register to 0x0 when our debugger is at the 607 address to do this.

8. On this run, we observe access granted being printed at 610

### 0x06: Tools for binary analysis/disassembly

Reading the binary as it is:

- `cat BINARY`

- `vim BINARY`

- `strings BINARY`

- `hexdump -C BINARY`

Tracing function calls

- `man syscalls` (get manual of system calls in linux kernel, relevant when running strace)

- `strace BINARY` (strace traces system calls)

- `ltrace BINARY` (ltrace traces library calls)

Disassembly

- Hopper Disassembler (IDA Pro alternative for Mac)

    1. Provides decompiler (reverses binary assembly code into psuedocode)

    2. Automatically converts hexadecimal strings into C readable string

- Radare (IDA Pro alternative for Linux)

- `objdump -d BINARY` (disassemble entire binary along with the functions it calls, usually only main is relevant)

- `objdump -x BINARY | less` (get the headers, before piping it into `less` for better viewing)

    ```
    license_1:     file format elf64-x86-64
    license_1
    architecture: i386:x86-64, flags 0x00000112:
    EXEC_P, HAS_SYMS, D_PAGED
    start address 0x00000000004004d0
    
    Program Header:
        PHDR off    0x0000000000000040 vaddr 0x0000000000400040 paddr 0x0000000000400040 align 2**3
             filesz 0x00000000000001f8 memsz 0x00000000000001f8 flags r-x
      INTERP off    0x0000000000000238 vaddr 0x0000000000400238 paddr 0x0000000000400238 align 2**0
             filesz 0x000000000000001c memsz 0x000000000000001c flags r--
        LOAD off    0x0000000000000000 vaddr 0x0000000000400000 paddr 0x0000000000400000 align 2**21
             filesz 0x000000000000083c memsz 0x000000000000083c flags r-x
        LOAD off    0x0000000000000e10 vaddr 0x0000000000600e10 paddr 0x0000000000600e10 align 2**21
             filesz 0x0000000000000240 memsz 0x0000000000000248 flags rw-
     DYNAMIC off    0x0000000000000e28 vaddr 0x0000000000600e28 paddr 0x0000000000600e28 align 2**3
             filesz 0x00000000000001d0 memsz 0x00000000000001d0 flags rw-
        NOTE off    0x0000000000000254 vaddr 0x0000000000400254 paddr 0x0000000000400254 align 2**2
             filesz 0x0000000000000044 memsz 0x0000000000000044 flags r--
    EH_FRAME off    0x0000000000000710 vaddr 0x0000000000400710 paddr 0x0000000000400710 align 2**2
             filesz 0x0000000000000034 memsz 0x0000000000000034 flags r--
       STACK off    0x0000000000000000 vaddr 0x0000000000000000 paddr 0x0000000000000000 align 2**4
             filesz 0x0000000000000000 memsz 0x0000000000000000 flags rw-
       RELRO off    0x0000000000000e10 vaddr 0x0000000000600e10 paddr 0x0000000000600e10 align 2**0
             filesz 0x00000000000001f0 memsz 0x00000000000001f0 flags r--
    
    Dynamic Section:
      NEEDED               libc.so.6
      INIT                 0x0000000000400450
      FINI                 0x00000000004006b4
      INIT_ARRAY           0x0000000000600e10
      INIT_ARRAYSZ         0x0000000000000008
      FINI_ARRAY           0x0000000000600e18
      FINI_ARRAYSZ         0x0000000000000008
      GNU_HASH             0x0000000000400298
      STRTAB               0x0000000000400348
      SYMTAB               0x00000000004002b8
      STRSZ                0x000000000000004b
      SYMENT               0x0000000000000018
      DEBUG                0x0000000000000000
      PLTGOT               0x0000000000601000
      PLTRELSZ             0x0000000000000078
      PLTREL               0x0000000000000007
      JMPREL               0x00000000004003d8
      RELA                 0x00000000004003c0
      RELASZ               0x0000000000000018
      RELAENT              0x0000000000000018
      VERNEED              0x00000000004003a0
      VERNEEDNUM           0x0000000000000001
      VERSYM               0x0000000000400394
    
    Version References:
      required from libc.so.6:
        0x09691a75 0x00 02 GLIBC_2.2.5
    
    Sections:
    Idx Name          Size      VMA               LMA               File off  Algn
      0 .interp       0000001c  0000000000400238  0000000000400238  00000238  2**0
                      CONTENTS, ALLOC, LOAD, READONLY, DATA
      1 .note.ABI-tag 00000020  0000000000400254  0000000000400254  00000254  2**2
                      CONTENTS, ALLOC, LOAD, READONLY, DATA
      2 .note.gnu.build-id 00000024  0000000000400274  0000000000400274  00000274  2**2
                      CONTENTS, ALLOC, LOAD, READONLY, DATA
      3 .gnu.hash     0000001c  0000000000400298  0000000000400298  00000298  2**3
                      CONTENTS, ALLOC, LOAD, READONLY, DATA
      4 .dynsym       00000090  00000000004002b8  00000000004002b8  000002b8  2**3
                      CONTENTS, ALLOC, LOAD, READONLY, DATA
      5 .dynstr       0000004b  0000000000400348  0000000000400348  00000348  2**0
                      CONTENTS, ALLOC, LOAD, READONLY, DATA
      6 .gnu.version  0000000c  0000000000400394  0000000000400394  00000394  2**1
                      CONTENTS, ALLOC, LOAD, READONLY, DATA
      7 .gnu.version_r 00000020  00000000004003a0  00000000004003a0  000003a0  2**3
                      CONTENTS, ALLOC, LOAD, READONLY, DATA
      8 .rela.dyn     00000018  00000000004003c0  00000000004003c0  000003c0  2**3
                      CONTENTS, ALLOC, LOAD, READONLY, DATA
      9 .rela.plt     00000078  00000000004003d8  00000000004003d8  000003d8  2**3
                      CONTENTS, ALLOC, LOAD, READONLY, DATA
     10 .init         0000001a  0000000000400450  0000000000400450  00000450  2**2
                      CONTENTS, ALLOC, LOAD, READONLY, CODE
     11 .plt          00000060  0000000000400470  0000000000400470  00000470  2**4
                      CONTENTS, ALLOC, LOAD, READONLY, CODE
     12 .text         000001e2  00000000004004d0  00000000004004d0  000004d0  2**4
                      CONTENTS, ALLOC, LOAD, READONLY, CODE
     13 .fini         00000009  00000000004006b4  00000000004006b4  000006b4  2**2
                      CONTENTS, ALLOC, LOAD, READONLY, CODE
     14 .rodata       0000004e  00000000004006c0  00000000004006c0  000006c0  2**2
                      CONTENTS, ALLOC, LOAD, READONLY, DATA
     15 .eh_frame_hdr 00000034  0000000000400710  0000000000400710  00000710  2**2
                      CONTENTS, ALLOC, LOAD, READONLY, DATA
     16 .eh_frame     000000f4  0000000000400748  0000000000400748  00000748  2**3
                      CONTENTS, ALLOC, LOAD, READONLY, DATA
     17 .init_array   00000008  0000000000600e10  0000000000600e10  00000e10  2**3
                      CONTENTS, ALLOC, LOAD, DATA
     18 .fini_array   00000008  0000000000600e18  0000000000600e18  00000e18  2**3
                      CONTENTS, ALLOC, LOAD, DATA
     19 .jcr          00000008  0000000000600e20  0000000000600e20  00000e20  2**3
                      CONTENTS, ALLOC, LOAD, DATA
     20 .dynamic      000001d0  0000000000600e28  0000000000600e28  00000e28  2**3
                      CONTENTS, ALLOC, LOAD, DATA
     21 .got          00000008  0000000000600ff8  0000000000600ff8  00000ff8  2**3
                      CONTENTS, ALLOC, LOAD, DATA
     22 .got.plt      00000040  0000000000601000  0000000000601000  00001000  2**3
                      CONTENTS, ALLOC, LOAD, DATA
     23 .data         00000010  0000000000601040  0000000000601040  00001040  2**3
                      CONTENTS, ALLOC, LOAD, DATA
     24 .bss          00000008  0000000000601050  0000000000601050  00001050  2**0
                      ALLOC
     25 .comment      0000004d  0000000000000000  0000000000000000  00001050  2**0
                      CONTENTS, READONLY
    SYMBOL TABLE:
    0000000000400238 l    d  .interp        0000000000000000              .interp
    0000000000400254 l    d  .note.ABI-tag  0000000000000000              .note.ABI-tag
    0000000000400274 l    d  .note.gnu.build-id     0000000000000000              .note.gnu.build-id
    0000000000400298 l    d  .gnu.hash      0000000000000000              .gnu.hash
    00000000004002b8 l    d  .dynsym        0000000000000000              .dynsym
    0000000000400348 l    d  .dynstr        0000000000000000              .dynstr
    0000000000400394 l    d  .gnu.version   0000000000000000              .gnu.version
    00000000004003a0 l    d  .gnu.version_r 0000000000000000              .gnu.version_r
    00000000004003c0 l    d  .rela.dyn      0000000000000000              .rela.dyn
    00000000004003d8 l    d  .rela.plt      0000000000000000              .rela.plt
    0000000000400450 l    d  .init  0000000000000000              .init
    0000000000400470 l    d  .plt   0000000000000000              .plt
    00000000004004d0 l    d  .text  0000000000000000              .text
    00000000004006b4 l    d  .fini  0000000000000000              .fini
    00000000004006c0 l    d  .rodata        0000000000000000              .rodata
    0000000000400710 l    d  .eh_frame_hdr  0000000000000000              .eh_frame_hdr
    0000000000400748 l    d  .eh_frame      0000000000000000              .eh_frame
    0000000000600e10 l    d  .init_array    0000000000000000              .init_array
    0000000000600e18 l    d  .fini_array    0000000000000000              .fini_array
    0000000000600e20 l    d  .jcr   0000000000000000              .jcr
    0000000000600e28 l    d  .dynamic       0000000000000000              .dynamic
    0000000000600ff8 l    d  .got   0000000000000000              .got
    0000000000601000 l    d  .got.plt       0000000000000000              .got.plt
    0000000000601040 l    d  .data  0000000000000000              .data
    0000000000601050 l    d  .bss   0000000000000000              .bss
    0000000000000000 l    d  .comment       0000000000000000              .comment
    0000000000000000 l    df *ABS*  0000000000000000              crtstuff.c
    0000000000600e20 l     O .jcr   0000000000000000              __JCR_LIST__
    0000000000400500 l     F .text  0000000000000000              deregister_tm_clones
    0000000000400530 l     F .text  0000000000000000              register_tm_clones
    0000000000400570 l     F .text  0000000000000000              __do_global_dtors_aux
    0000000000601050 l     O .bss   0000000000000001              completed.6973
    0000000000600e18 l     O .fini_array    0000000000000000              __do_global_dtors_aux_fini_array_entry
    0000000000400590 l     F .text  0000000000000000              frame_dummy
    0000000000600e10 l     O .init_array    0000000000000000              __frame_dummy_init_array_entry
    0000000000000000 l    df *ABS*  0000000000000000              crack.c
    0000000000000000 l    df *ABS*  0000000000000000              crtstuff.c
    0000000000400838 l     O .eh_frame      0000000000000000              __FRAME_END__
    0000000000600e20 l     O .jcr   0000000000000000              __JCR_END__
    0000000000000000 l    df *ABS*  0000000000000000              
    0000000000600e18 l       .init_array    0000000000000000              __init_array_end
    0000000000600e28 l     O .dynamic       0000000000000000              _DYNAMIC
    0000000000600e10 l       .init_array    0000000000000000              __init_array_start
    0000000000601000 l     O .got.plt       0000000000000000              _GLOBAL_OFFSET_TABLE_
    00000000004006b0 g     F .text  0000000000000002              __libc_csu_fini
    0000000000000000  w      *UND*  0000000000000000              _ITM_deregisterTMCloneTable
    0000000000601040  w      .data  0000000000000000              data_start
    0000000000000000       F *UND*  0000000000000000              puts@@GLIBC_2.2.5
    0000000000601050 g       .data  0000000000000000              _edata
    00000000004006b4 g     F .fini  0000000000000000              _fini
    0000000000000000       F *UND*  0000000000000000              printf@@GLIBC_2.2.5
    0000000000000000       F *UND*  0000000000000000              __libc_start_main@@GLIBC_2.2.5
    0000000000601040 g       .data  0000000000000000              __data_start
    0000000000000000       F *UND*  0000000000000000              strcmp@@GLIBC_2.2.5
    0000000000000000  w      *UND*  0000000000000000              __gmon_start__
    0000000000601048 g     O .data  0000000000000000              .hidden __dso_handle
    00000000004006c0 g     O .rodata        0000000000000004              _IO_stdin_used
    0000000000400640 g     F .text  0000000000000065              __libc_csu_init
    0000000000601058 g       .bss   0000000000000000              _end
    00000000004004d0 g     F .text  0000000000000000              _start
    0000000000601050 g       .bss   0000000000000000              __bss_start
    00000000004005bd g     F .text  0000000000000077              main
    0000000000000000  w      *UND*  0000000000000000              _Jv_RegisterClasses
    0000000000601050 g     O .data  0000000000000000              .hidden __TMC_END__
    0000000000000000  w      *UND*  0000000000000000              _ITM_registerTMCloneTable
    0000000000400450 g     F .init  0000000000000000              _init
    ```

    1. the .text field is interesting to us as it shows the address range of our code from 4004d0 to 4006b2 (4004d0 + 1e2 = 4006b2). 1e2 translates to 482 bytes.

    2. the .rodata (read only data) field is also interesting to us! Address range for .rodata is from 4006c0 to 40070e (4006c0 + 4e = 40070e).

More GDB things:

```
(gdb) break 0x0000000000400602
Function "0x0000000000400602" not defined.
Make breakpoint pending on future shared library load? (y or [n]) n
(gdb) break *0x0000000000400602
Breakpoint 1 at 0x400602
(gdb) run asd
Starting program: /home/george93/Desktop/offsec-prep/osed-prep/LiveOverflow/0x05-0x06/license_1 asd
Checking License: asd

Breakpoint 1, 0x0000000000400602 in main ()
(gdb) info registers
rax            0x7fffffffe1b0      140737488347568
rbx            0x400640            4195904
rcx            0x0                 0
rdx            0x0                 0
rsi            0x4006da            4196058
rdi            0x7fffffffe1b0      140737488347568
rbp            0x7fffffffdce0      0x7fffffffdce0
rsp            0x7fffffffdcd0      0x7fffffffdcd0
r8             0x7ffff7f69040      140737353519168
r9             0x7ffff7f690c0      140737353519296
r10            0x7ffff7f68fc0      140737353519040
r11            0x246               582
r12            0x4004d0            4195536
r13            0x0                 0
r14            0x0                 0
r15            0x0                 0
rip            0x400602            0x400602 <main+69>
eflags         0x212               [ AF IF ]
cs             0x33                51
ss             0x2b                43
ds             0x0                 0
es             0x0                 0
fs             0x0                 0
gs             0x0                 0
(gdb) x/s 0x4006da
0x4006da:	"AAAA-Z10N-42-OK"
```

- Stopping at the strcmp address, we realise that the rsi register holds a memory address which is within range of the .rodata address range. Accessing the register value as a c string using `x/s HEXADECIMAL_STRING`, we obtain the key as well.

- Cheatsheet on `x/[] HEXADECIMAL_STRING` can be found [here](https://blogs.oracle.com/linux/post/8-gdb-tricks-you-should-know)





