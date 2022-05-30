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
    (gdb) break *[FUNC]
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

