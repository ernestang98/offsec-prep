//
//  ROPLevel4.c
//  
//
//  Created by Billy Ellis on 20/05/2017.
//
// gcc roplevel4.c -o roplevel4 -fno-stack-protector -m32 -mpreferred-stack-boundary=2 -Wl,-z,norelro
// echo 2 | sudo tee /proc/sys/kernel/randomize_va_space 
// aslr & pie must be enabled for this challenge

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

char leakme[] = "hello roplevel4";

void secret() {
    printf("DANG IT YOU FOUND ME");
    exit(0); // ensure program does not crash as a result of Buffer Overflow
}

void leak_address(){
    printf("Address of leakme is: %p\n\n",&leakme);  
    FILE *f = fopen("./leak.txt","w");
    fprintf(f,"%p",&leakme);
    fclose(f);
}

int main(){
    char name[16];
    
    system("clear");
    
    printf("\x1B[35m=====================================================================\n");
    printf("Welcome to ROPLevel4 by Billy Ellis (@bellis1000) edited by Potatodev\n");
    printf("=====================================================================\x1B[0m\n\n");
    
    printf("Leaking address...\n");
    leak_address();
    
    printf("Enter your name:\n");
    gets(name);
    // scanf("%s",name); // stops at \x0d \x0c \x0a and many others
    printf("Welcome, %s!\n",name);
    
    return 0;   
}
