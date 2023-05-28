### Crackmes 1

https://www.youtube.com/watch?v=tt15P5Om3Zg&ab_channel=CodewithNick

https://stackoverflow.com/questions/28656004/c-random-doesnt-workreturns-same-value-always

### Crackmes 2

https://www.youtube.com/watch?v=zGkgCGbSZvI&ab_channel=areyou1or0

### Crackmes 3

https://www.youtube.com/watch?v=EyNdHy9WtN4&ab_channel=BartySteakfried

### Flare-on

https://flare-on9.ctfd.io/register

### Crackmes 4

6302929933c5d4425e2ccf9c.zip

https://crackmes.one/crackme/6302929933c5d4425e2ccf9c

https://www.rapidtables.com/convert/number/hex-to-decimal.html

https://stackoverflow.com/questions/45898438/understanding-cmp-instruction

https://stackoverflow.com/questions/40831605/translating-conditional-move-cmov-instructions-from-assembly-into-c

https://wiki.cheatengine.org/index.php?title=Assembler:Commands:CMOVNB

https://stackoverflow.com/questions/14841169/jnz-cmp-assembly-instructions

https://stackoverflow.com/questions/18996646/what-does-this-assembly-code-do-test-xor-jnz

https://cplusplus.com/reference/cstring/memcmp/

abcdefghijk

```
.text:00007FF6460712C0 ; int __cdecl main(int argc, const char **argv, const char **envp)
.text:00007FF6460712C0 main proc near                          ; CODE XREF: __scrt_common_main_seh(void)+107↓p
.text:00007FF6460712C0                                         ; DATA XREF: .pdata:00007FF646076078↓o
.text:00007FF6460712C0 sub     rsp, 28h
.text:00007FF6460712C4 mov     rcx, cs:?cout@std@@3V?$basic_ostream@DU?$char_traits@D@std@@@1@A ; std::basic_ostream<char,std::char_traits<char>> std::cout
.text:00007FF6460712CB lea     rdx, aInputPassword             ; "Input Password:"
.text:00007FF6460712D2 call    sub_7FF646071630
.text:00007FF6460712D7 mov     rcx, rax
.text:00007FF6460712DA lea     rdx, sub_7FF646071800
.text:00007FF6460712E1 call    cs:??6?$basic_ostream@DU?$char_traits@D@std@@@std@@QEAAAEAV01@P6AAEAV01@AEAV01@@Z@Z ; std::basic_ostream<char,std::char_traits<char>>::operator<<(std::basic_ostream<char,std::char_traits<char>> & (*)(std::basic_ostream<char,std::char_traits<char>> &))
.text:00007FF6460712E7 mov     rcx, cs:?cin@std@@3V?$basic_istream@DU?$char_traits@D@std@@@1@A ; std::basic_istream<char,std::char_traits<char>> std::cin
.text:00007FF6460712EE call    sub_7FF646071840
.text:00007FF6460712F3 cmp     cs:qword_7FF646075060, 10h
.text:00007FF6460712FB lea     rdx, Buf2
.text:00007FF646071302 mov     r8, cs:Size                     ; Size
.text:00007FF646071309 lea     rcx, Src
.text:00007FF646071310 cmovnb  rdx, cs:Buf2                    ; Buf2
.text:00007FF646071318 cmp     cs:qword_7FF646075080, 10h
.text:00007FF646071320 cmovnb  rcx, cs:Src                     ; Buf1
.text:00007FF646071328 cmp     r8, cs:qword_7FF646075058
.text:00007FF64607132F jnz     short loc_7FF646071341
.text:00007FF646071331 call    memcmp
.text:00007FF646071336 lea     rdx, aCongratsYouGet            ; "Congrats! You get the Password right!"
.text:00007FF64607133D test    eax, eax
.text:00007FF64607133F jz      short loc_7FF646071348
.text:00007FF646071341
.text:00007FF646071341 loc_7FF646071341:                       ; CODE XREF: main+6F↑j
.text:00007FF646071341 lea     rdx, aNopeThatsNotIt            ; "Nope thats not it"
.text:00007FF646071348
.text:00007FF646071348 loc_7FF646071348:                       ; CODE XREF: main+7F↑j
.text:00007FF646071348 mov     rcx, cs:?cout@std@@3V?$basic_ostream@DU?$char_traits@D@std@@@1@A ; std::basic_ostream<char,std::char_traits<char>> std::cout
.text:00007FF64607134F call    sub_7FF646071630
.text:00007FF646071354 lea     rdx, sub_7FF646071800
.text:00007FF64607135B mov     rcx, rax
.text:00007FF64607135E call    cs:??6?$basic_ostream@DU?$char_traits@D@std@@@std@@QEAAAEAV01@P6AAEAV01@AEAV01@@Z@Z ; std::basic_ostream<char,std::char_traits<char>>::operator<<(std::basic_ostream<char,std::char_traits<char>> & (*)(std::basic_ostream<char,std::char_traits<char>> &))
.text:00007FF646071364 lea     rcx, Command                    ; "pause"
.text:00007FF64607136B call    cs:system
.text:00007FF646071371 xor     eax, eax
.text:00007FF646071373 add     rsp, 28h
.text:00007FF646071377 retn
.text:00007FF646071377 main endp
```

cmp     cs:qword_7FF646075060, 10h

qword_7FF646075060 dq 2Fh    

Result : ZF and CF set to ==> "ZF = 0" and "CF = 0"

lea     rdx, Buf2

Buf2 dq 215F99176F0h   

debug033:00000215F99176F0 db  31h ; 1
debug033:00000215F99176F1 db  65h ; e
debug033:00000215F99176F2 db  63h ; c
debug033:00000215F99176F3 db  63h ; c
debug033:00000215F99176F4 db  37h ; 7
debug033:00000215F99176F5 db  64h ; d
debug033:00000215F99176F6 db  64h ; d
debug033:00000215F99176F7 db  37h ; 7
debug033:00000215F99176F8 db  62h ; b
debug033:00000215F99176F9 db  39h ; 9
debug033:00000215F99176FA db  37h ; 7
debug033:00000215F99176FB db  36h ; 6
debug033:00000215F99176FC db  33h ; 3
debug033:00000215F99176FD db  30h ; 0
debug033:00000215F99176FE db  32h ; 2
debug033:00000215F99176FF db  38h ; 8
debug033:00000215F9917700 db  65h ; e
debug033:00000215F9917701 db  31h ; 1
debug033:00000215F9917702 db  31h ; 1
debug033:00000215F9917703 db  39h ; 9
debug033:00000215F9917704 db  65h ; e
debug033:00000215F9917705 db  35h ; 5
debug033:00000215F9917706 db  30h ; 0
debug033:00000215F9917707 db  34h ; 4
debug033:00000215F9917708 db  36h ; 6
debug033:00000215F9917709 db  32h ; 2
debug033:00000215F991770A db  36h ; 6
debug033:00000215F991770B db  38h ; 8
debug033:00000215F991770C db  64h ; d
debug033:00000215F991770D db  39h ; 9
debug033:00000215F991770E db  32h ; 2
debug033:00000215F991770F db  32h ; 2

.text:00007FF646071302 mov     r8, cs:Size                     ; Size

.data:00007FF646075078 Size dq 0Bh

Corresponds to the size of our input (length 11)

.text:00007FF646071310 cmovnb  rdx, cs:Buf2                    ; Buf2

If CF=0 then condition is satisfied, otherwise it will be skipped.

Conditional move does not really matter as Buf2 is already in rdx

.text:00007FF646071318 cmp     cs:qword_7FF646075080, 10h

.data:00007FF646075080 qword_7FF646075080 dq 0Fh               ; DATA XREF: main+58↑r

So we are comparing 10h to 0Fh

.text:00007FF646071320 cmovnb  rcx, cs:Src                     ; Buf1

If CF=0 then condition is satisfied, otherwise it will be skipped.

Conditional move does not really matter as Src is already in rcx

.data:00007FF646075068 Src dq 6867666564636261h                ; DATA XREF: main+49↑o
.data:00007FF646075068                                         ; main+60↑r ...
.data:00007FF646075070 db  69h ; i
.data:00007FF646075071 db  6Ah ; j
.data:00007FF646075072 db  6Bh ; k

Src contains our input string

.text:00007FF646071328 cmp     r8, cs:qword_7FF646075058

.data:00007FF646075058 qword_7FF646075058 dq 20h  

Size of input is store in r8

so the size of our input need to be equal to 20h, if not during the cmp, it will not be equal, and Z flag will be set to 1 and jump will occur during jnz

20h = 32 decimal

11111111111111111111111111111111'

So we passed .text:00007FF64607132F jnz     short loc_7FF646071341

next is call memcpy()

which sets v7 eax as seen below

memcpy() copies

```
int __cdecl main(int argc, const char **argv, const char **envp)
{
  __int64 v3; // rax
  void **v4; // rdx
  size_t v5; // r8
  void **v6; // rcx
  int v7; // eax
  const char *v8; // rdx
  __int64 v9; // rax

  v3 = sub_7FF646071630(std::cout, "Input Password:", envp);
  std::basic_ostream<char,std::char_traits<char>>::operator<<(v3, sub_7FF646071800);
  sub_7FF646071840(std::cin);
  v4 = &Buf2;
  v5 = Size;
  v6 = &Src;
  if ( (unsigned __int64)qword_7FF646075060 >= 0x10 )
    v4 = (void **)Buf2;
  if ( (unsigned __int64)qword_7FF646075080 >= 0x10 )
    v6 = (void **)Src;
  if ( Size != qword_7FF646075058 || (v7 = memcmp(v6, v4, Size), v8 = "Congrats! You get the Password right!", v7) )
    v8 = "Nope thats not it";
  v9 = sub_7FF646071630(std::cout, v8, v5);
  std::basic_ostream<char,std::char_traits<char>>::operator<<(v9, sub_7FF646071800);
  system("pause");
  return 0;
}
```

So we see that memcpy has 3 parameters memcpy(void *dest_str, const void *src_str, size_t number)

in this context it is memcmp(v6, v4, Size)

so it is comparing the memory address of &Src and &Buf2. If it is correct return 0 to v7 which is eax

We need Src2 to equal to Buf2 as later on, there is a test eax eax which we need eax to be 0 for ZF to set to 0 and for us to jump (we want it tojump in this case, if not rdx will be overwritten with "Nope thats not it")

Hence, our input needs to be Buf2, which is 1ecc7dd7b9763028e119e5046268d922

![image](https://user-images.githubusercontent.com/56427824/195388918-251e04aa-76b0-44f5-b1d8-c71e8629c9f1.png)

### CECZ4069 Tutorial 4

garen.exe

This is one of the assignments for a module I took in NTU, CECZ4069 which is a malware analysis module. This assignment teaches the use of IDA

Open Garry.exe in IDA

use msdn documents to find the arguments/parameters to function call

find GetStdHandle

highlight number and press h to change to number (press h to undo)

shift dash to changed to signed integer

ffffffff5h

  - -10 standard output handle

  - can press m in hex mode to look through documentation for ffffffff5h

ffffffff6h

  - -11 standard input handle

  - can press m in hex mode to look through documentation for fffffffff6h

press g then input (jumps to various sections of the code)

  - byte_413000

  - 413000

  - .data:00413000

press a on the array byte (not the content) to see it as an array (one line)

press u to reverse

shift semicolon to add your own comment

[https://www.dcode.fr/cipher-identifier](https://www.dcode.fr/cipher-identifier)

from this we can tell that its a base64 encoding hpwever simply base64 decoding it does not give us the answer.

analysing sub_401260, we make an inference that it is some sort of base64 encoding function

we see multiple references to al, byte ptr aZyxabcdefghijk[ecx] ; "ZYXABCDEFGHIJKLMNOPQRSTUVWzyxabcdefghij"…

.data:00413000 aZyxabcdefghijk db 'ZYXABCDEFGHIJKLMNOPQRSTUVWzyxabcdefghijklmnopqrstuvw0123456789+/',0

this looks very similar to a base64 chracter set

[cyberchef](https://gchq.github.io/CyberChef/#recipe=From_Base64('ZYXABCDEFGHIJKLMNOPQRSTUVWzyxabcdefghijklmnopqrstuvw0123456789%2B/',true,false)&input=eER1ZWJUSzBXamlyeDJpaFdSS0NOMWwwSkFWNU5EU2VhRGlyVzIxZXlFYWV4alJyVjI5cQ)

Can use python script as well

