gcc roplevel4.c -o roplevel4 -fno-stack-protector -z execstack -m32 -fPIE -mpreferred-stack-boundary=2 -Wl,-z,norelro

temporarily pause this shit