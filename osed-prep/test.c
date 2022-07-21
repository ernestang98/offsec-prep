#include<stdio.h>
#include<stdlib.h>

// https://security.stackexchange.com/questions/70569/aslr-does-not-seem-to-randomize-text-section
// https://www.geeksforgeeks.org/dynamic-memory-allocation-in-c-using-malloc-calloc-free-and-realloc/
// gcc test.c -o test -no-pie -m32

int func() {
  return 1; 
}

int main() {
  int i_should_be_on_stack = 0;
  int *i_should_be_on_heap;
  int size_of_chunk_on_heap;
  i_should_be_on_heap = (int*)malloc(size_of_chunk_on_heap * sizeof(int));
  
  printf("Location of local function func() :%p\n", &func); 
  printf("Location of main function         :%p\n", &main);
  printf("Location of variable on stack     :%p\n", &i_should_be_on_stack);
  printf("Location of pointer on heap       :%p\n", &i_should_be_on_heap);
  printf("Location of system in libc        :%p\n", &system);
  
  system("echo 'Disable & Enable ASLR and observe the differences :D'");
  system("echo 'Disable & Enable PIE and observe the differences :D'");
  
  return 0; 
}
