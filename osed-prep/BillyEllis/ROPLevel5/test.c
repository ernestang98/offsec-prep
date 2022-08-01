//
//  roplevel5.c
//  
//
//  Created by Billy Ellis on 09/08/2017.
//
//

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

char feedbackString[32];
char feedbackString2[32];

void secret(){

printf("\n\x1b[32myou win ;)\n");
system("ls -sail");

}

void give_feedback(){
printf("%x\n", &secret);
    printf("\033[1mLeave some feedback:\n");
    char string[16];
    //scanf("%s",string);
    gets(string);

if (strcmp(string,"q") == 0){
exit(0);
}

char leakme[] = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAA";
    
    printf(string);
    printf("\n");

    sprintf(feedbackString,string,string);
    char leakme2[] = "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB";
    sprintf(feedbackString2,feedbackString,feedbackString);
    FILE *f = fopen("./feedback.txt","w");
    fprintf(f,"%s",feedbackString2);
    fclose(f);
    //printf("%s\n", feedbackString);
    //printf("%s\n", feedbackString2);
    
}

int main(){
    
    printf("\033[1m\x1B[34m================================================\x1B[0m\n");
    printf("\033[1mWelcome to ROPLevel5 by Billy Ellis (@bellis1000)\n");
    printf("\x1B[34m================================================\x1B[0m\n\n");
    
    int a = 1;


    
    while (a){
    
give_feedback();
sleep(1);
    }
    
    return 0;
    
}
