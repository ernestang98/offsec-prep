# ret2csu

### Finding offsets for functions within `.so` libraries

- rabin2, objdump, readelf

### __libc_csu_init:

```
pwndbg> disas __libc_csu_init
Dump of assembler code for function __libc_csu_init:
   0x0000000000400640 <+0>:	push   r15
   0x0000000000400642 <+2>:	push   r14
   0x0000000000400644 <+4>:	mov    r15,rdx
   0x0000000000400647 <+7>:	push   r13
   0x0000000000400649 <+9>:	push   r12
   0x000000000040064b <+11>:	lea    r12,[rip+0x20079e]        # 0x600df0
   0x0000000000400652 <+18>:	push   rbp
   0x0000000000400653 <+19>:	lea    rbp,[rip+0x20079e]        # 0x600df8
   0x000000000040065a <+26>:	push   rbx
   0x000000000040065b <+27>:	mov    r13d,edi
   0x000000000040065e <+30>:	mov    r14,rsi
   0x0000000000400661 <+33>:	sub    rbp,r12
   0x0000000000400664 <+36>:	sub    rsp,0x8
   0x0000000000400668 <+40>:	sar    rbp,0x3
   0x000000000040066c <+44>:	call   0x4004d0 <_init>
   0x0000000000400671 <+49>:	test   rbp,rbp
   0x0000000000400674 <+52>:	je     0x400696 <__libc_csu_init+86>
   0x0000000000400676 <+54>:	xor    ebx,ebx
   0x0000000000400678 <+56>:	nop    DWORD PTR [rax+rax*1+0x0]
   0x0000000000400680 <+64>:	mov    rdx,r15
   0x0000000000400683 <+67>:	mov    rsi,r14
   0x0000000000400686 <+70>:	mov    edi,r13d
   0x0000000000400689 <+73>:	call   QWORD PTR [r12+rbx*8]
   0x000000000040068d <+77>:	add    rbx,0x1
   0x0000000000400691 <+81>:	cmp    rbp,rbx
   0x0000000000400694 <+84>:	jne    0x400680 <__libc_csu_init+64>
   0x0000000000400696 <+86>:	add    rsp,0x8
   0x000000000040069a <+90>:	pop    rbx
   0x000000000040069b <+91>:	pop    rbp
   0x000000000040069c <+92>:	pop    r12
   0x000000000040069e <+94>:	pop    r13
   0x00000000004006a0 <+96>:	pop    r14
   0x00000000004006a2 <+98>:	pop    r15
   0x00000000004006a4 <+100>:	ret    
End of assembler dump.
```

```
└─$ gdb-pwndbg ret2csu
Reading symbols from ret2csu...
(No debugging symbols found in ret2csu)
pwndbg: loaded 192 commands. Type pwndbg [filter] for a list.
pwndbg: created $rebase, $ida gdb functions (can be used with print/break)
pwndbg> x _fini
0x4006b4 <_fini>:	0x08ec8348

gef➤  search-pattern 0x4006b4
[+] Searching '\xb4\x06\x40' in memory
[+] In '/home/george93/Desktop/offsec-prep/osed-prep/ROPEmporium/ret2csu/ret2csu'(0x400000-0x401000), permission=r-x
  0x4003b0 - 0x4003bc  →   "\xb4\x06\x40[...]" 
  0x400e48 - 0x400e54  →   "\xb4\x06\x40[...]" 
[+] In '/home/george93/Desktop/offsec-prep/osed-prep/ROPEmporium/ret2csu/ret2csu'(0x600000-0x601000), permission=r--
  0x6003b0 - 0x6003bc  →   "\xb4\x06\x40[...]" 
  0x600e48 - 0x600e54  →   "\xb4\x06\x40[...]" 
```

```
   0x000000000040068d <+77>:	add    rbx,0x1
   0x0000000000400691 <+81>:	cmp    rbp,rbx
=> 0x0000000000400694 <+84>:	jne    0x400680 <__libc_csu_init+64>
```

- After executing the mov gadget, we will be adding 1 to rbx and comparing it with rbp. We will jmp if rbp does not equal to rbp but we want them to be equal cause we don't want to jump


### Related Links

- https://ir0nstone.gitbook.io/notes/types/stack/ret2csu

- https://stackoverflow.com/questions/17437191/function-parameters-transferred-in-registers-on-64bit-os

- https://stackoverflow.com/questions/17437191/function-parameters-transferred-in-registers-on-64bit-os

- https://stackoverflow.com/questions/21879454/how-to-convert-a-hex-string-to-hex-number

- https://stackoverflow.com/questions/68892212/assembly-what-does-register-in-square-brackets-means?noredirect=1&lq=1

- https://stackoverflow.com/questions/48608423/what-do-square-brackets-mean-in-x86-assembly

- https://stackoverflow.com/questions/2030366/what-do-the-brackets-mean-in-nasm-syntax-for-x86-asm

- https://downloads.ti.com/docs/esd/SPNU118O/Content/SPNU118O_HTML/assembler_description.html

- https://guyinatuxedo.github.io/18-ret2_csu_dl/ropemporium_ret2csu/index.html#:~:text=We%20can%20find%20a%20pointer%20to%20it%20using%20

- https://stackoverflow.com/questions/21612765/what-is-fini-as-defined-by-gprof-output

- https://stackoverflow.com/questions/606191/convert-bytes-to-a-string

- https://stackoverflow.com/questions/21879454/how-to-convert-a-hex-string-to-hex-number

- https://stackoverflow.com/questions/57952088/how-to-fix-unpack-require-a-buffer-of-8-bytes-error-when-handling-8-bytes

- https://ir0nstone.gitbook.io/notes/other/pwntools/packing

- https://ctftime.org/writeup/17397

- https://radiofreerobotron.net/blog/2017/11/23/ropemporium-pivot-ctf-walkthrough/