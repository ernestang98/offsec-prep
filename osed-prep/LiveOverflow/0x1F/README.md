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

  2. `l = strlen(p);` gets the length of the value that p is pointing to

  3. `start = strstr(buf, "ROOT");` finds the STARTING index of the substring of `ROOT`

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


