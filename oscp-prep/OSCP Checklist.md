# OSCP Checklist

Make sure to follow everything...

### Enumeration

Port Scanning:

> $ nmap -sC -sV -Pn (TCP scan)	
>
> $ nmap -p- -Pn (full TCP scan)
>
> $ sudo nmap -sU (UDP scan)
>
> $ sudo nmap -sU -p- (full UDP scan)


Vulnerability Scanning:

> $ nmap --script=
>
> $ nikto -h WEBSERVER


Banner Grabbing

> $ telnet IP PORT
>
> $ nc -nvv IP PORT

Useful Websites

> Hacktricks (90% of footholds can be obtained from information on this website)

### Service Authentication Bruteforcing

> (Usually) Require username and or password
>
> Software: hydra/cewl/hashcat
>
> Wordlist: rockyou.txt, custom generated ones
>
> If you have username, try username as password
>
> If you have username, can try creating username wordlist using usernamer
>
> Use commonly used usernames:passwords 
>
> Search for default credentials (if any) 

### Password Cracking

> Need wordlist
>
> Software: jtr, crackstation, cewl, hashcat
>
> Wordlist: rockyou.txt, custom generated ones
>
> Use commonly used passwords 
>
> Search for default credentials (if any)  

### Juicy Files to look out for

> /etc/passwd & /etc/shadow
>
> .RDP files
>
> SAM & SYSTEM Files

### Encryption/Encoding/Steganography-related

> strings
>
> binwalk
>
> base64
>
> [Cipher Identifier](https://www.dcode.fr/cipher-identifier)

### LFI /RFI

> Sometimes, need to analyse web application (especially the URL)
>
> Base64 Encoding: http://ip/?file=php://filter/convert.base64-encode/resource=/location/to/file
> 
> Log Poisoning

### Telnet

> If you have credentials and other services are not opened (such as SSH or port 3389), can authenticate and obtain shell via telnet
>
> Authentication Service Bruteforce

### SMTP

> Protocol that allows SENDING of emails
>
> Usually connected to POP3/IMAP 
>
> Usually/maybe need a valid email for exploit
>
> [Postfix ShellShock](https://github.com/3mrgnc3/pentest_old/blob/master/postfix-shellshock-nc.py)
>
> Client Side Attacks 
> 
> [SWAKS](https://github.com/jetmore/swaks), used in [HTB SneakyMailer](https://p0i5on8.github.io/posts/hackthebox-sneakymailer/#swaks)

### POP3

> Mail-inbox-sort-of protocol, if you have credentials (email and password), you can log in and authenticate, allowing you access to mails for information gathering 
>
> Service authentication bruteforcing
>
> [Commands cheatsheet](https://www.atmail.com/blog/imap-commands/)

### IMAP

> Similar to POP3
>
> Service authentication bruteforcing
>
> [Commands cheatsheet](https://busylog.net/telnet-imap-commands-note/)
> 
> [Evolution tool](https://en.wikipedia.org/wiki/GNOME_Evolution)

### Apache James

> Service authentication bruteforcing
>
> Default credentials root:root

### FTP

> Authentication Service Bruteforce
>
> Anonymous authentication 
>
> Common authentication - admin:admin, root:root, [User:Pass list by SecLists](https://github.com/danielmiessler/SecLists/blob/master/Passwords/Default-Credentials/ftp-betterdefaultpasslist.txt)
>
> $ get ../../../etc/passwd (LFI Exploit) 

### SSH

> Authentication Service Bruteforce
>
> Debian OpenSSL Predictable PRNG
>
> [Private Key Authentication (need to set permissions properly)](https://unix.stackexchange.com/questions/36540/why-am-i-still-getting-a-password-prompt-with-ssh-with-public-key-authentication)

### SMB

> nmap scans for version and vulnerabilities
>
> Service authentication bruteforcing
>
> Try anonymous authentication 
>	
> Tools: smbclient, smbmap, enum4linux
>
> Obtain smb version for exploit (using smbver.py, wireshark, nmap scans)
>
> SOME exploits (too many)
>
>	> MS08-067
>	>	
>	> Symlink Directory Traversal
>	>
>	> usermap_script
>	>
>	> MS17-010

### Authentication Tools

> smb (get file shares)
>
> evil-winrm
>
> pth-winexe 
>
> psexec
>
> wmic-exec 

### RPC/LDAP

> Service authentication bruteforcing
>
> Try anonymous authentication 
>
> Tools: rpcclient/ldapsearch

### Generic Webserver (IIS, Apache etc.)

Fuzzing

> Feroxbuster (AJAX)
>
> gobuster/Dirb
>
>	> Go from common, to small, to medium to large wordlist 
>	>
>	> Set extension flag (-x) 

Vulnerability Scanning

> nmap 
>
> nikto -h HOST

Enumeration

> robots.txt / sitemap
>
> SearchSploit Plugins/Services used
>
> Source code analysis
>
> Web application information gathering (useful especially when they give person information) 

Authentication Service Bruteforce

> If have csrf protection, you may have to use a custom script to avoid it, see 0xdf's writeup on [Bart](https://0xdf.gitlab.io/2018/07/15/htb-bart.html)
>
> If default credentials are not working, try to use information gathered from enumeration as the passwords (e.g. last names) 

Common exploits

> XSS, CSRF, SSRF, SQLi, NoSQLi
>
> File Upload, Command Injection (Hacktricks for bypasses)
>
> HTTP request misconfigurations, try different HTTP methods other than the default GET method
>
> Server misconfiguration (if you know the domain name, set at /etc/hosts file)

Less common exploits

> YAML Deserialization exploit - [SnakeYAML](https://swapneildash.medium.com/snakeyaml-deserilization-exploited-b4a2c5ac0858)
>
> JSON Deserialization exploit - [Jackson](https://blog.doyensec.com/2019/07/22/jackson-gadgets.html) 

HTTPS / SSL

> Heartbleed information disclosure
>
> nmap ssl vulnerability scans

### Specific Webserver

> [APACHE] Apache + PHP < 5.3.12 / < 5.4.2 - cgi-bin Remote Code Execution

### Generic SQL Exploits

> [SQLi] Authentication Bypass
>
> [SQLi] Database injection/changes
>
> [SQLi] RCE
>
> [SQLi] File creation/upload  
>
> [SQLi] Union SQLi
>
> [SQLi] Error-based SQLi  
>
> [SQLi] Blind SQLi  
>
> [ACCESS TO DATABASE] Database injection/changes
>
> [ACCESS TO DATABASE] Service Authentication Bruteforcing
>
> [ACCESS TO DATABASE] RCE

### Specific SQL Exploits

> [MYSQL/MariaDB] UDF
>
> [PostgreSQL] UDF 
>
> [MSSQL] Impackets mssqlclient.py
>
> [MSSQL] Xpcmdshell
>
> [MSSQL] Master MDF File
>
> [MSSQL] SA Password Hash/Plaintext Password 

### Oracle TNS Listener

> Methodology: SID -> Username/Password -> Exploit
>
> Tools to use: sqlplus 
>
>	> [sqlplus installation](https://github.com/rapid7/metasploit-framework/wiki/How-to-get-Oracle-Support-working-with-Kali-Linux)
>	>
> 	> [use `--sysdba` flag if insufficient privileges and all privesc methods fail](https://stackoverflow.com/questions/35199084/forgot-oracle-username-and-password-how-to-retrieve) 
>	>
> 	> [sqlplus: error while loading shared libraries: libsqlplus.so: cannot open shared object file: No such file or directory](https://stackoverflow.com/questions/27717312/sqlplus-error-while-loading-shared-libraries-libsqlplus-so-cannot-open-shared#:~:text=It%20means%20you%20didn't,It%20will%20be%20working.)
>
> Tools to use: odat
> 	>
> 	> [ODAT PrivEsc](https://github.com/quentinhardy/odat/wiki/privesc)
>	>
> 	> [Spartan Blog on Hacking Oracle](https://blog.spartan-cybersec.com/how-to-hack-an-oracle-database-server/)
>
> [Hacking Oracle by OWASP](https://owasp.org/www-pdf-archive//ASDC12-New_and_Improved_Hacking_Oracle_From_Web.pdf)

### SNMP

> Information Gathering using snmpwalk
>	>
> 	> [Help for following error that you may encounter: nsExtendOutput1Line Fails with SNMPD on Debian Wheezy](https://serverfault.com/questions/595440/nsextendoutput1line-fails-with-snmpd-on-debian-wheezyy)

### TFTP

> Arbitrary File Disclosure (you will need to know path to file)

### Active Directory

Objective:
>
> Get Domain Admin
>
> Try to find usernames, passwords and/or hashes 
>
> Try to gather information about the active directory that maybe exploited 
>
> Take note that any hashes/exploits that you find from using AD enumeration tools can usually ONLY be used against DOMAIN accounts and not LOCAL accounts

Background information:
>
> Silver Ticket Attack
>	>
>	> [What is a silver ticket?](https://www.varonis.com/blog/kerberos-attack-silver-ticket#:~:text=A%20Silver%20Ticket%20is%20a,create%20a%20fake%20authentication%20ticket.)
>	>
>	> [Silver Ticket YouTube demo](https://www.youtube.com/watch?v=GTJyd-AMfuM)
>	>
>	> HTB Silver Ticket Exploit Boxes: [Hades](https://snovvcrash.rocks/2020/12/28/htb-hades.html#using-silver-ticket-with-servicespy), [Intelligence](https://www.hackingarticles.in/intelligence-hackthebox-walkthrough/)
>
> Golden Ticket Attack 
>	>
>	> [What is a golden ticket?](https://www.extrahop.com/company/blog/2021/detect-kerberos-golden-ticket-attacks/) 
>	>
>	> [Golden Ticket YouTube demo](https://www.youtube.com/watch?v=f6SleGakcE0) 
>	>
>	> HTB Golden Ticket Exploit Boxes: [Forest](https://infosecwriteups.com/forest-an-asreproast-dcsync-and-golden-ticket-hackthebox-walkthrough-ade8dcdd1ee5)
>
> [Trust Tickets](https://medium.com/r3d-buck3t/breaking-domain-trusts-with-forged-trust-tickets-5f03fb71cd72) 
>
> [Silver Tickets vs Golden Tickets](https://adsecurity.org/?p=1515)

GitHub Cheatsheets:
>
> [Mimikatz Cheatsheet - can be used with or without AD ;)](https://gist.github.com/insi2304/484a4e92941b437bad961fcacda82d49)
>
> [Generic AD Cheatsheet](https://gist.github.com/TarlogicSecurity/2f221924fef8c14a1d8e29f3cb5c5c4a)
>
> [Bigger AD Cheatsheet](https://github.com/S1ckB0y1337/Active-Directory-Exploitation-Cheat-Sheet)

Popular Mindmap/Checklist:
>
> [AD Enumeration/Exploitation mindmap](https://www.xmind.net/m/5dypm8/)
>
> [Checklist version of AD Enumeration/Exploitation mindmap](https://tajdini.net/blog/penetration/active-directory-penetration-mind-map/)

Other resouces:
>
> [WADComs ("Checklist" tool)](https://wadcoms.github.io/)
>
> [AD pentesting notes by zer1t0](https://zer1t0.gitlab.io/posts/attacking_ad/)
>
> [AD pentesting notes by FareedFauzi](https://fareedfauzi.gitbook.io/oscp-notes/others/active-directory-attack)
>
> [AD Pentesting mindmap by Orange-Cyberdefense](https://github.com/Orange-Cyberdefense/arsenal/raw/master/mindmap/pentest_ad.png)
> 
> [Building and attacking an Active Directory Lab](https://1337red.wordpress.com/building-and-attacking-an-active-directory-lab-with-powershell/)

AD Enumeration Commands:
>
> [Finding Domain Controllers and Domain Admins](https://www.netspi.com/blog/technical/network-penetration-testing/5-ways-to-find-systems-running-domain-admin-processes/)
>
> [Listing users in AD Group](https://serverfault.com/questions/49405/command-line-to-list-users-in-a-windows-active-directory-group)
>
> [AD Domain Controller documentation](https://docs.microsoft.com/en-us/powershell/module/activedirectory/get-addomaincontroller?view=windowsserver2022-ps)
> 
> [`net group` vs `net localgroup` #1](https://www.reddit.com/r/sysadmin/comments/cshfvg/net_group_vs_net_localgroup/)
>
> [`net group` vs `net localgroup` #2](https://social.technet.microsoft.com/Forums/lync/en-US/c157d6d4-a21d-44a9-b560-b161f60c3c79/how-to-find-list-of-list-of-domain-admin-and-local-administrator-user-through-command-line?forum=winserverDS)

Exploits:
>
> Pass the ticket
>
> Pass the hash
>
> Overpass the hash  
>
> Zerologon
>
> LSASS dumping
>	>
>	> [Resource on dumping lsass](https://www.whiteoaksecurity.com/blog/attacks-defenses-dumping-lsass-no-mimikatz/)
>
> Service Authentication Bruteforcing 
>	>
>	> Usually/may need username and password/hash
>	>
>	> Use username list as password list if cannot get/generate password list
>	>
>	> can be used against domain `-d` or local computer `--local-auth`
>	>
>	> If crackmapexec smb have "pwned", means correct authentication + have admin shares (can psexec)
>	>
>	> $ crackmapexec smb IP --pass-pol (always run this before bruteforcing to get password policy)
>	>
>	> $ crackmapexec smb IP -u 'user' -p 'PASS' -M spider_plus (to spider through smb shares)
>	>
>	> $ crackmapexec smb IP -u 'user' -p 'PASS' --users (to get list of users)
>
> AD Connect Database Exploit
>	>
>	> [Resource Link #1 by xpnsec](https://blog.xpnsec.com/azuread-connect-for-redteam/)
>	>
> > [Resource Link #2 by vbscrub](https://vbscrub.com/2020/01/14/azure-ad-connect-database-exploit-priv-esc/)
>
> GMSA Password Exposures
>
> DNS Poisoning
>	>
>	> krbrelayx toolkit
>	>
>	> nslookup
>	>
>	> responder
>	>
> 	> msf http_ntlm
>
> Kerberoasting
>	>
>	> [Resource on Kerberoasting #1](https://www.pentestpartners.com/security-blog/how-to-kerberoast-like-a-boss/)
>	>
>	> [Resource on Kerberoasting #2](https://www.hackingarticles.in/deep-dive-into-kerberoasting-attack/)
>	>
>	> [Resource on Kerberoasting #3](https://malicious.link/post/2016/kerberoast-pt1/)
> >
> > HTB Kerberoasting Exploit Boxes: [Active](https://0xdf.gitlab.io/2018/12/08/htb-active.html#kerberoasting)

Tools:
>
> crackmapexec
>
> impacket suit of tools
>
> bloodhound
>
> mimikatz.exe 
>
> responder 
>
> [adPEAS](https://github.com/61106960/adPEAS)

### Generic PrivEsc/Post-Exploitation

If you have administrative credentials, can just authenticate/switch to administrator account depending on your OS
>
> [Linux]  If you have the plaintext password of a user, can try running `su -` or `sudo su`, and you should get root if you are allowed to run sudo or su

Look at what privileges you have
>
> [Linux] sudo -l
>
> [Windows] whoami /priv 

PEAS Tool
>
> [Linux] Linpeas
>
> [Windows] Winpeas

OS Kernel Exploit/Enumeration Tool
>
> [Linux] LinEnum, Linux Smart Enumeration, Linux Exploit Suggester
>
> [Windows] [Windows Exploit Suggester](https://github.com/AonCyberLabs/Windows-Exploit-Suggester), [wes](https://github.com/bitsadmin/wesng)
>
> [Windows] Sherlock.ps1 - [How to use sherlock?](https://vk9-sec.com/sherlock-find-missing-windows-patches-for-local-privilege-escalation/), Watson.exe, JAWS.ps1 
>
> [Windows] [Windows KE Enumeration - Sakshamdix pt 1](https://www.sakshamdixit.com/enumerate-windows-exploit-part-1/), [Windows KE Enumeration - Sakshamdix pt 2](https://www.sakshamdixit.com/enumerate-windows-exploit-part-2/)
>
> [Windows] [Kakyouim Windows KE Cheatsheet](https://kakyouim.hatenablog.com/entry/2020/05/27/010807#MS10_015-high) 

Searchsploit/enumerate binaries/files/services/processes owned by root (Searchsploit/whatever-suggester-tool-you-are-using may not detect the exploit, sometimes, you need to Google and use the first few results)
>
> [Linux & Windows] Tib3rius Course on Windows & Linux Privilege Escalation is pretty good for this 

PrivEsc Cheatsheet
>
> [Linux] [Linux Priv Esc Cheatsheet by swisskyrepo](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Linux%20-%20Privilege%20Escalation.md)
>
> [Windows] [Windows Priv Esc Cheatsheet by swisskyrepo](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Windows%20-%20Privilege%20Escalation.md)

Post Exploitatiion Cheatsheet
>
> [Linux] [Mubix Cheatsheet](https://github.com/mubix/post-exploitation/wiki/Linux-Post-Exploitation-Command-List)
>
> [Windows] [Emilyanncr Cheatsheet](https://github.com/emilyanncr/Windows-Post-Exploitation)

### Linux PrivEsc

> Cronjobs/Schedulers 
>	>
>	> cat /etc/crontab
>	>
>	> cat /etc/crontab.bak 
>
> Sensitive Files
>	>
>	> SSH Keys
>	>
>	> /etc/passwd, /etc/shadow
>	>
>	> Can try password cracking 
>
> Container Exploit (docker/lxd/lxc)
>
> SUID/GTFO Bins 

### Windows PrivEsc

> AlwaysInstallElevated exploit
>
> Seimpersonate exploit (Juicy Potatoes)
>
> UAC
> 	>
> 	> [UACME](https://github.com/hfiref0x/UACME)

### Buffer Overflow 

> Finding bad chars using mona (google/youtube)
>
> Other out-of-oscp-scope/htb binary exploit things:
>	>
>	> Tools: 
>	>	>
>	> 	> gdp-peda: helps with debugging and analysing binaries
>	>	>
>	> 	> ldd: helps to see location of library in memory
>	>	>
>	>	> checksec: helps to see properties of binaries
>	>	>
>	>	> readelf, strings: get offsets of calls from memory location of library
>	>	>
>	> Some memory protection properties we need to check for:
>	> 	>
>	> 	> ASLR 
>	>	>	>
>	>	>	> If enabled, randomize location of programs in memory
>	>	>	>
>	>	>	> Not a problem as we can run exploit repeatedly in loop if the range is small
>	> 	>	
>	> 	> NX
>	>	> 	>
>	>	> 	> If enabled, cannot run shellcode in stack (where we usually run shellcode)
>	>	> 	>
>	>	> 	> We need to perform a `return to libc attack` - instead of dropping shellcode in stack, we can drop the memory address of system call in linux pointed to a string which we will input (e.g. /bin/bash)

### Other Stuff

> [PHP language Exploit](https://github.com/flast101/php-8.1.0-dev-backdoor-rce)
>
> If you have sudo privileges to edit a file, maybe you can do a symlink
>
> May have to change the exploit depending on scenario (good example: HTB Optimum)
>
> Installing impacket for python2
>	>
>	> $ curl https://bootstrap.pypa.io/pip/2.7/get-pip.py -o get-pip.py
>	>
>	> $ python get-pip.py
>	>
>	> $ PATH=/home/kali/.local/bin:$PATH
>	>
>	> $ pip --version
>	>
> 	> $ pip install --upgrade setuptools
>	>
> 	> $ pip install impacket 
