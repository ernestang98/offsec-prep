┌──(george93㉿kali)-[~/…/osed-prep/ROPEmporium/pivot/pivot32]
└─$ readelf -s libpivot32.so 

    51: 00000974   164 FUNC    GLOBAL DEFAULT   12 ret2win

┌──(george93㉿kali)-[~/…/osed-prep/ROPEmporium/pivot/pivot32]
└─$ rabin2 -s libpivot32.so    

    18  0x00000974 0x00000974 GLOBAL FUNC   164      ret2win

                                                                                                                                                                                                               
┌──(george93㉿kali)-[~/…/osed-prep/ROPEmporium/pivot/pivot32]
└─$ ldd pivot32
	linux-gate.so.1 (0xf7fc9000)
	libpivot32.so => ./libpivot32.so (0xf7fc0000)
	libc.so.6 => /lib/i386-linux-gnu/libc.so.6 (0xf7db6000)
	/lib/ld-linux.so.2 (0xf7fcb000)
