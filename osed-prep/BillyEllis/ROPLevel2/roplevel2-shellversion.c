#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

char str1[] = "uname -a";
char str2[] = "touch pwned.txt";
char str3[] = "ls -sail";

void winner(){
	printf("Nothing interesting here...\n");
	system("# this does nothing...");
	exit(0);
}

void gadget(){
	__asm__("pop %ebx; ret");
	//__asm__("pop {r0,pc}\n");
}

int main(){
	char buff[16];
	printf("Welcome to ROPLevel2 created by Billy Ellis (@bellis1000) edited by Potato_dev :)\n");
	printf("The objective of this level is to obtain a shell via Ret2libc/ROP\n");
	printf("Good luck: ");
	scanf("%s",buff);
	printf("Nice try ;)\n");
	return 0;
}
