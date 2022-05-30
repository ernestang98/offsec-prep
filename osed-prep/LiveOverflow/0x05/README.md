# LiveOverflow Binary Exploitation / Memory Corruption

### 0x05: Reversing & Cracking First Program (introduction to GNU Debugger - GDB)

GDB commands:

- `gdb BINARY`: attaches binary to debugger

- `(gdb) disassemble FUNC`: disassembles function FUNC(), usually use with main as we know that every C program has a main() function. 

- ```
  (gdb) set disassembly-flavor intel
  (gdb) disassemble FUNC
  ```
    
    Disassemble function with better formatting

Assembly code analysis principles:

