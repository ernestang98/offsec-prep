# ROPEmporium

- [Installation Guide](https://ropemporium.com/guide.html)

### Pre-requisites

1. [checksec](https://installati.one/kalilinux/checksec/)

    `checksec --file=BINARY`

    - Does not check for ASLR... I think... to see if ASLR is enabled, you can compile the following test.c program under the following conditions

        1. `echo 0 > /proc/sys/kernel/randomize_va_space && gcc test.c -o test-no-aslr` (disable ASLR)
        
        2. `echo 1 > /proc/sys/kernel/randomize_va_space && gcc test.c -o test-aslr` (enable ASLR)

    - For the one with aslr, running `ldd BINARY` should result in different base addresses of libc library referenced by program

        ```
        ┌──(root㉿kali)-[/home/george93/Desktop/rop_emporium_all_challenges]
        └─# ldd test-aslr
        	linux-vdso.so.1 (0x00007ffd22a95000)
        	libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007fda328b3000)
        	/lib64/ld-linux-x86-64.so.2 (0x00007fda32aa9000)
                                                                                                                                                                                                                                      
        ┌──(root㉿kali)-[/home/george93/Desktop/rop_emporium_all_challenges]
        └─# ldd test-aslr
        	linux-vdso.so.1 (0x00007ffc0171b000)
        	libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f3a3611f000)
        	/lib64/ld-linux-x86-64.so.2 (0x00007f3a36315000)
                                                                                                                                                                                                                                      
        ┌──(root㉿kali)-[/home/george93/Desktop/rop_emporium_all_challenges]
        └─# ldd test-aslr
        	linux-vdso.so.1 (0x00007ffdb016d000)
        	libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f1a6455a000)
        	/lib64/ld-linux-x86-64.so.2 (0x00007f1a64750000)
                                                                                                                                                                                                                                      
        ┌──(root㉿kali)-[/home/george93/Desktop/rop_emporium_all_challenges]
        └─# ldd test-aslr
        	linux-vdso.so.1 (0x00007ffc99b86000)
        	libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007fa3c4de2000)
        	/lib64/ld-linux-x86-64.so.2 (0x00007fa3c4fd8000)
                                                                                                                                                                                                                              
        ┌──(root㉿kali)-[/home/george93/Desktop/rop_emporium_all_challenges]
        └─# ldd test-no-aslr 
        	linux-vdso.so.1 (0x00007ffff7fca000)
        	libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007ffff7dd0000)
        	/lib64/ld-linux-x86-64.so.2 (0x00007ffff7fcc000)
                                                                                                                                                                                                                                      
        ┌──(root㉿kali)-[/home/george93/Desktop/rop_emporium_all_challenges]
        └─# ldd test-no-aslr
        	linux-vdso.so.1 (0x00007ffff7fca000)
        	libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007ffff7dd0000)
        	/lib64/ld-linux-x86-64.so.2 (0x00007ffff7fcc000)
                                                                                                                                                                                                                                      
        ┌──(root㉿kali)-[/home/george93/Desktop/rop_emporium_all_challenges]
        └─# ldd test-no-aslr
        	linux-vdso.so.1 (0x00007ffff7fca000)
        	libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007ffff7dd0000)
        	/lib64/ld-linux-x86-64.so.2 (0x00007ffff7fcc000)
        ```

2. [gdb](https://www.kali.org/tools/gdb/)

3. [ropper](https://www.kali.org/tools/ropper/)

4. [pwntools](https://github.com/Gallopsled/pwntools)

5. [radare2](https://github.com/radareorg/radare2)

6. [pwndbg and other stuff for gdb](https://github.com/apogiatzis/gdb-peda-pwndbg-gef)

7. [ROPGadget](https://github.com/JonathanSalwan/ROPgadget)

    `sudo apt install python3-ropgadget`

### 32bit vs 64bit

- https://www.ired.team/miscellaneous-reversing-forensics/windows-kernel-internals/linux-x64-calling-convention-stack-frame

### Analyse libraries/binaries

- `objdump -S /path/to/library.so`

- `rabin2 -s /path/to/binary`

- `ropper -f /path/to/bianry --search "pop"`

- `ROPgadget --binary /path/to/binary`