# LiveOverflow Binary Exploitation / Memory Corruption

### Radare2 Introduction

- Disassmebly and decompilation, Reverse Engineering Tool

- Install by git cloning the repository and running `./sys/install.sh`

### Commands

`?` (get help/manual)

`[0x004004d0]> aaa` (analyse everything)

`[0x004004d0]> afl` (print all functions radare found)

```
[0x004004d0]> afl
0x004004d0    1 42           entry0
0x004004a0    1 6            sym.imp.__libc_start_main
0x00400500    4 41           sym.deregister_tm_clones
0x00400530    4 57           sym.register_tm_clones
0x00400570    3 28           sym.__do_global_dtors_aux
0x00400590    4 45   -> 42   entry.init0
0x004006b0    1 2            sym.__libc_csu_fini
0x004006b4    1 9            sym._fini
0x00400640    4 101          sym.__libc_csu_init
0x004005bd    6 119          main
0x00400450    3 26           sym._init
0x004004c0    1 6            loc.imp.__gmon_start__
0x00400480    1 6            sym.imp.puts
0x00400490    1 6            sym.imp.printf
0x004004b0    1 6            sym.imp.strcmp
```
`s ARGS` (seek command, go to the address stated in ARGS)

```
[0x004004d0]> s s
section.                     section..comment             
section..shstrtab            section..symtab              
section..strtab              segment.GNU_STACK            
sym..comment                 segment.LOAD0                
segment.ehdr                 segment.PHDR                 
section..interp              segment.INTERP               
sym..interp                  section..note.ABI_tag        
segment.NOTE                 sym..note.ABI_tag            
section..note.gnu.build_id   sym..note.gnu.build_id       
section..gnu.hash            sym..gnu.hash                
section..dynsym              sym..dynsym                  
section..dynstr              sym..dynstr                  
section..gnu.version         sym..gnu.version             
section..gnu.version_r       sym..gnu.version_r           
section..rela.dyn            sym..rela.dyn                
section..rela.plt            sym..rela.plt                
section..init                sym..init                    
sym._init                    section..plt                 
sym..plt                     sym.imp.puts                 
sym.imp.printf               sym.imp.__libc_start_main    
sym.imp.strcmp               section..text                
sym..text                    sym._start                   
sym.deregister_tm_clones     sym.register_tm_clones       
sym.__do_global_dtors_aux    sym.frame_dummy              
sym.main                     sym.__libc_csu_init          
sym.__libc_csu_fini          section..fini                
sym..fini                    sym._fini                    
section..rodata              sym..rodata                  
str.Checking_License:__s_n   str.AAAA_Z10N_42_OK          
str.Access_Granted_          str.WRONG_                   
str.Usage:__key_             section..eh_frame_hdr        
segment.GNU_EH_FRAME         sym..eh_frame_hdr            
section..eh_frame            sym..eh_frame                
section..init_array          segment.LOAD1                
segment.GNU_RELRO            sym..init_array              
section..fini_array          sym..fini_array              
section..jcr                 sym..jcr                     
section..dynamic             segment.DYNAMIC              
sym..dynamic                 section..got                 
sym..got                     section..got.plt             
sym..got.plt                 section..data                
sym..data                    section..bss                 
sym..bss                     
[0x004004d0]> s sym.main
[0x004005bd]>
```

`pdf` (prints disassembly)

```
[0x004005bd]> pdf
            ; DATA XREF from entry0 @ 0x4004ed
┌ 119: int main (uint32_t argc, char **argv);
│           ; var char **s1 @ rbp-0x10
│           ; var uint32_t var_4h @ rbp-0x4
│           ; arg uint32_t argc @ rdi
│           ; arg char **argv @ rsi
│           0x004005bd      55             push rbp
│           0x004005be      4889e5         mov rbp, rsp
│           0x004005c1      4883ec10       sub rsp, 0x10
│           0x004005c5      897dfc         mov dword [var_4h], edi     ; argc
│           0x004005c8      488975f0       mov qword [s1], rsi         ; argv
│           0x004005cc      837dfc02       cmp dword [var_4h], 2
│       ┌─< 0x004005d0      7551           jne 0x400623
│       │   0x004005d2      488b45f0       mov rax, qword [s1]
│       │   0x004005d6      4883c008       add rax, 8
│       │   0x004005da      488b00         mov rax, qword [rax]
│       │   0x004005dd      4889c6         mov rsi, rax
│       │   0x004005e0      bfc4064000     mov edi, str.Checking_License:__s_n ; 0x4006c4 ; "Checking License: %s\n" ; const char *format
│       │   0x004005e5      b800000000     mov eax, 0
│       │   0x004005ea      e8a1feffff     call sym.imp.printf         ; int printf(const char *format)
│       │   0x004005ef      488b45f0       mov rax, qword [s1]
│       │   0x004005f3      4883c008       add rax, 8
│       │   0x004005f7      488b00         mov rax, qword [rax]
│       │   0x004005fa      beda064000     mov esi, str.AAAA_Z10N_42_OK ; 0x4006da ; "AAAA-Z10N-42-OK" ; const char *s2
│       │   0x004005ff      4889c7         mov rdi, rax                ; const char *s1
│       │   0x00400602      e8a9feffff     call sym.imp.strcmp         ; int strcmp(const char *s1, const char *s2)
│       │   0x00400607      85c0           test eax, eax
│      ┌──< 0x00400609      750c           jne 0x400617
│      ││   0x0040060b      bfea064000     mov edi, str.Access_Granted_ ; 0x4006ea ; "Access Granted!" ; const char *s
│      ││   0x00400610      e86bfeffff     call sym.imp.puts           ; int puts(const char *s)
│     ┌───< 0x00400615      eb16           jmp 0x40062d
│     │││   ; CODE XREF from main @ 0x400609
│     │└──> 0x00400617      bffa064000     mov edi, str.WRONG_         ; 0x4006fa ; "WRONG!" ; const char *s
│     │ │   0x0040061c      e85ffeffff     call sym.imp.puts           ; int puts(const char *s)
│     │┌──< 0x00400621      eb0a           jmp 0x40062d
│     │││   ; CODE XREF from main @ 0x4005d0
│     ││└─> 0x00400623      bf01074000     mov edi, str.Usage:__key_   ; 0x400701 ; "Usage: <key>" ; const char *s
│     ││    0x00400628      e853feffff     call sym.imp.puts           ; int puts(const char *s)
│     ││    ; CODE XREFS from main @ 0x400615, 0x400621
│     └└──> 0x0040062d      b800000000     mov eax, 0
│           0x00400632      c9             leave
└           0x00400633      c3             ret
[0x004005bd]> 
```

`VV` (after running `pdf`, allows you to enter visual mode)

- Use arrow keys to move around

- blue box indicates the section of control graph we are at

- ta/shift-tab to move around different control boxes

- shift + h/j/k/l to move the control box you are at now

- p to toggle about different views of the control graph

- ? to launch help

- similar to vim/vi, use `:COMMAND` to run commands

`r2 -d BINARY` (run radare in debug mode)

- `db ADDRESS` to set breakpoint

- `dc` to run the program

- `s` to step into the next instruction (includes function calls)

- `S` to step into the next instruction (skipping function calls)
