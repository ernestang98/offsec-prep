# LiveOverflow Binary Exploitation / Memory Corruption

### 0x00 - 0x03

Skipped

### 0x04: CPU and Assembler

Components of a computer:

- CPU

- Memory

- Registers (located in CPU)

Memory:

- Each memory location which stores assembly instruction has an address in hexadecimal numbers (e.g. 0x0000fa19)

- Each memory location stores assembly instructions as previously mention, such as `MOV EAX 5`, which means move the value 5 to register EAX.

Stack:

- Bottom part of memory

- To add values/instructions into the top of the stack, we use the PUSH instruction (e.g. `PUSH 0x5` pushes 0x5 to the top of the stack and updates the SP by -/+1 depending on memory architcture)

- To remove values/instructions from the top of the stack, we use the POP instruction (e.g. `POP EAX` removes the value at the top of the stack and puts it in the EAX register, before updating the SP by +/-1 depending on memory architecture) 

Registries:

- Registries in memory are like variables which can store values

- You can also store variables in the memory itself

- Some registries are special, such as:

    1. RIP/EIP/PC (Instruction Pointer): Points to the memory address of the next instruction in memory to be executed

    2. ESP/RSP/SP (Stack Pointer): Points to the nenory address of the address location at the top of the stack. 

Instructions:

- Expressed in hexadecimals/bits as well

- JMP instruction: `JMP 0x5` Jumps to memory location at memory address 0x5, updates IP to 0x5. It is the same as `MOV EIP 5` 

- JE instruction: `JE 0x5` jump to memory location at memory address 0x5 if the last instruction resulted in 0 (ZF flag set to 1)

- CALL: Used for calling functions when executing an instruction in assembly. Usually these functions may/will be located in other parts of your memory. So CALL wil push the memory address of the next instruction to be executed from the IP to the stack before proceeding to executing the function.

- RET: Used for returning back to the next address after the function call ends. RET pops the memory address from the stack to the IP which thereby allows you to continue the assembly program after calling a function.

Status Flags:

- ZF Zero Flag: Set to 1 if the last computation resulted in 0

Disassembler:

- Converts hexadecimals/bits into assembly instruction which allows us to analyse and study assembly code better

Mentioned/Additional Resources:

- https://microcorruption.com

- https://sockpuppet.org/issue-79-file-0xb-foxport-hht-hacking.txt.html




