- Source Code Analysis

  ```
  void check_path(char *buf)
  {
    char *start;
    char *p;
    int l;

    /*
    * Work out old software bug
    */

    p = rindex(buf, '/');
    l = strlen(p);
    if(p) {
        start = strstr(buf, "ROOT");
        if(start) {
            while(*start != '/') start--;
            memmove(start, p, l);
            printf("moving from %p to %p (exploit: %s / %d)\n", p, start, start < buf ?
            "yes" : "no", start - buf);
        }
    }
  }
  ```
  
  1. `p = rindex(buf, '/');` returns pointer to the last occurence of `/`
  
     ```
     Given /lol/ROOT/blah, return pointer to /lol/ROOT/blah
                                                      ^
                                                      |
                                                pointer here
     ```

  2. `l = strlen(p);` gets the length of the value that p is pointing to (i.e. length of `blah` in this context but it would refer to the length of the string after the last `/`)

  3. `start = strstr(buf, "ROOT");` finds the STARTING index of the substring of `ROOT`

  4. `while(*start != '/') start--;` decrement start variable till it finds the first `/` before `ROOT`
  
  5. `memmove(start, p, l);` moves the data starting from the starting address pointed by `p` to the ending address indicated by `l` to the memory address pointed by the `start` pointer (i.e. `/lol/ROOT/blah` &rarr; `/lol/blah/blah`

  ```
  int get_requests(int fd)
  {
    char *buf;
    char *destroylist[256];
    int dll;
    int i;

    dll = 0;
    while(1) {
        if(dll >= 255) break;

        buf = calloc(REQSZ, 1);
        if(read(fd, buf, REQSZ) != REQSZ) break;

        if(strncmp(buf, "FSRD", 4) != 0) break;

        check_path(buf + 4);     

        dll++;
    }

    for(i = 0; i < dll; i++) {
                  write(fd, "Process OK\n", strlen("Process OK\n"));
        free(destroylist[i]);
    }
  }
  ```

  1. `buf = calloc(REQSZ, 1);` allocates 256 bytes of memory in heap and returns pointer to `buf`

  2. `if(read(fd, buf, REQSZ) != REQSZ) break;` ensures that the input we are reading is 256 bytes long

  3. `if(strncmp(buf, "FSRD", 4) != 0) break;` ensures that the 1st 4 chars of our input is equal to FSRD

- Exploit methodology: unsafe code + `memmove()` which calls `free()`

  1. Realise that during the while-loop in search of the first `/` after the last `/`, if we do not specify a proper path (e.g. `AAAAROOTBBBB/CCCC`) then the function will continue to look through the buffer behind the input and only stop at the first `/` it finds, before performing a memmove() and overwriting that segment of the buffer with `/CCCC` from our original input.

  2. We can send 2 payloads, one with slashes and one with data. The first payload will inject the heap with slashes. The second payload will crafted in a way whereby the while-loop will reach the slashes as injected by the first payload
  
  3. After the while-loop chunk exits, we will iterate through a for loop and start to write "Process OK" messages and free our heap
  
      ```
      for(i = 0; i < dll; i++) {
        write(fd, "Process OK\n", strlen("Process OK\n"));
        free(destroylist[i]);
      }
      ```
      
  4. What you have to do now is that using the free() function call on the first iteration of the for-loop, we have to overwrite the write function in the GOT table to redirect code execution as we did in heap3 such that on the second iteration of the for-loop (there will be 2 iterations since we sent 2 payloads), we will be able to call our redirected code when the write() function is called as it has already been overwritten by the initial first free() function call.
  
- Analyzing the _int_free() function call within the malloc.c source code:

    ```
    ...
    else if (!chunk_is_mmapped(p)) {
    nextchunk = chunk_at_offset(p, size);
    nextsize = chunksize(nextchunk);
    assert(nextsize > 0);

    /* consolidate backward */
    if (!prev_inuse(p)) {
      prevsize = p->prev_size;
      size += prevsize;
      p = chunk_at_offset(p, -((long) prevsize));
      unlink(p, bck, fwd);
    }

    if (nextchunk != av->top) {
      /* get and clear inuse bit */
      nextinuse = inuse_bit_at_offset(nextchunk, nextsize);

      /* consolidate forward */
      if (!nextinuse) {
        unlink(nextchunk, bck, fwd);
        size += nextsize;
      } else
        clear_inuse_bit_at_offset(nextchunk, 0);

    ...
    ```

    - Given that the size memory address of the first chunk we are freeing is at 0x89, we skip the first if-block as the prev-inuse bit is set (last bit)

    - We then check whether the next chunk is in use or not. It should not be in use as the program will refer look at the size of the next next chunk located at 0x804e08c - 0x4 (same as 0x804e08c + 0xfffffffc) which should also be a 0xfffffffc. All of this is a result of abusing and exploiting the poorly written code where memmove() is called.

    - As the next chunk is not in use, we will unlink the next chunk and thereby successfully abusing the dlmalloc unlink() exploit

    - Once we can redirect code execution to different sections of our heap, we can inject shellcode in our first payload and use the unlink() exploit to overwrite the write function in the GOT table to point to the beginning address of the shellcode in our first payload
