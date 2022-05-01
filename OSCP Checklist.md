# OSCP Checklist

Make sure to follow everything...

### General

- nmap

	- mini scan -sC -sV -Pn

	- full scan -p-

	- udp scan -sU (1nsider, pit)

	- full udp scan -sU -p-

	- search for nmap vuln scan scripts

- Hacktricks (most HTB initial shells can be found here)

	- finger

	- swaks for client side attacks on SMTP

- Bruteforce (related to authentication)

	- Usually need username and password, can try if you can find/guess a username

	- if you have the username, try the username as the password

	- Custom wordlist generator

		- Cewl

		- Hashcat --force --stdout -r /usr/share/hashcat/rules/best64.rule passwordlist > passwordlist

- Juicy Files

	- .RDP files (may contain credentials)

	- SAM & SYSTEM files (samdump2)

- Encryption/Encoding/Steganography-related

	- strings

	- binwalk 

	- base64

	- [Cipher Identifier](https://www.dcode.fr/cipher-identifier)

- Password Cracking

	- /etc/passwd & /etc/shadow

	- [CrackStation](https://crackstation.net/)

- LFI/RFI

	- Log Poisoning

	- Base64 Encoding: http://ip/?file=php://filter/convert.base64-encode/resource=/location/to/file

	- Look at URL

- Other exploits

	- PHP language Exploit

	- If you have sudo privileges to edit a file, maybe you can do a symlink

### Telnet

1. Exploit

	- Default Credentials

	- Bruteforce authentication

	- Weak passwords

	- If you have credentials and other services are not opened (such as SSH or port 3389), can authenticate and obtain shell via telnet

### SMTP

1. Exploit

	- Usually/maybe need a valid email

	- [Postfix ShellShock](https://github.com/3mrgnc3/pentest_old/blob/master/postfix-shellshock-nc.py)

### FTP

1. Information Gathering

	- Bruteforce (need a username)

	- Weak passwords

	- Default Credentials

	- Anonymous authentication

	- Try common authentication

		- admin:admin

		- root:root

		- [User:Pass list by SecLists](https://github.com/danielmiessler/SecLists/blob/master/Passwords/Default-Credentials/ftp-betterdefaultpasslist.txt)

2. Exploit

	- lfi exploit

### MySQL, MariaDB

1. Exploit

	- UDF Priv Esc

### SSH

1. Information Gathering

	- Bruteforce (need a username)

		- try username as the password

	- Weak passwords

	- Default Credentials

2. Exploit

	- Debian SSH Exploit

	- Possible priv esc vector if everything else fails

3. Others

	- [Private Key Authentication (need to set permissions properly)](https://unix.stackexchange.com/questions/36540/why-am-i-still-getting-a-password-prompt-with-ssh-with-public-key-authentication)

### Apache

1. Exploit

	- Server misconfiguration

		- If you know the domain name, set at /etc/hosts file

	- [PHP Exploit](https://github.com/flast101/php-8.1.0-dev-backdoor-rce)

	- Apache + PHP + cgi-bin

### HTTP

1. Information Gathering

	- Fuzzing
	
		- Feroxbuster (AJAX)
	
		- Gobuster/Dirb
	
			- common, small, medium, large wordlist
	
			- extensions -x
	
	- Nikto
	
	- robots.txt

	- SearchSploit Plugins/Services used
	
		- Advanced Comment System
	
		- Voting System for PHP (HTB Love)
	
		- Mongo/2.2.3 

	- Source code analysis

2. Exploits

	- Authentication-related

		- Default Credentials

			- If default credentials are not working, try to use information gathered from enumeration as the passwords (e.g. last names) 

		- Weak passwords (username, password, admin, root etc.)

		- Bruteforce*** (may need to create wordlist)

			- if have csrf protection, you may have to use a custom script to avoid it

			- Hydra

		- SQLi

		- NoSQLi

3. Others

	- File Upload

		- File Upload Filter Bypass

	- Command Injection

		- Command Injection Filter Bypass

	- YAML Deserialization exploit

		- [SnakeYAML](https://swapneildash.medium.com/snakeyaml-deserilization-exploited-b4a2c5ac0858)

	- JSON Deserialization exploit

		- [Jackson](https://blog.doyensec.com/2019/07/22/jackson-gadgets.html)

	- Configure domain name and target ip in Kali's /etc/hosts file

	- Server misconfigurations:

		- try different HTTP methods other than the default GET method

### HTTPS

1. Information Gathering

	- nmap ssl vulnerability scans

2. Exploit

	- Heartbleed 

### WinRM

1. Exploit

	- Shell using Evil-Winrm (need username & password/hash)

### MSSQL

1. Information Gathering

	- SA Password Hash/Plaintext Password
	
	- Master MDF File (google for location)

2. Exploit

	- mssqlclient.py (need credentials)

	- xpcmdshell

	- [RCE from SQLi](https://www.tarlogic.com/blog/red-team-tales-0x01/)

### Active Directory

- Objectives

	- Try to find usernames, passwords, or hashes!

	- Generate service tickets to authenticate

1. Information Gathering:

	- RPC enumeration
	
	- SMB enumeration

	- LDAP enumeration

	- AD Users/Group/Service enumeration

	- Normal web application/service enumeration

		- Attempt to find credentials for RPC/SMB/CME
	
	- Mimikatz.exe (need privileged access)

2. Exploit

	- Zerologon
	
	- Crackmapexec***

		- Usually/may need username & password

			- obtained usually using basic enumeration

			- if can only find username list, can try generating password list from username list
	
		- crackmapexec smb IP --pass-pol (always run this before bruteforcing)

		- bruteforcing*** with custom password list (smb/winrm)

		- smb -M spider_plus to spider through smb shares

		- --users for user enumeration

		- if have "pwned", means correct authentication + have admin shares (can psexec)
	
	- bloodhound (next level shit)

	- gMSA dumper
 
	- getST.py (service ticket)

		- need domain/acc_name

		- need SPN

		- credentials (hashes/password)

		- who you are requesting ticket for (usually put administrator)

	- psexec

		- using credentials (plaintext password)

		- using service tickets in linux
	
	- Azure AD Exploit (AD Connect)

		- [Link #1 by xpnsec](https://blog.xpnsec.com/azuread-connect-for-redteam/)

		- [Link #2 by vbscrub](https://vbscrub.com/2020/01/14/azure-ad-connect-database-exploit-priv-esc/)

3. DNS Poisoning (HTB - Intelligence)

	- krbrelayx toolkit

	- nslookup

	- responder

	- msf http_ntlm

4. Cheatsheets/Additional Tools

	- [adPEAS](https://github.com/61106960/adPEAS)

	- [AD Exploiation Cheatsheet by S1ckB0y1337](https://github.com/S1ckB0y1337/Active-Directory-Exploitation-Cheat-Sheet#using-powerview)

	- [AD Enumeration/Exploitation mindmap](https://www.xmind.net/m/5dypm8/)

	- [WADComs](https://wadcoms.github.io/)

	- [Attacking AD by zer1t0](https://zer1t0.gitlab.io/posts/attacking_ad/)

	- [AD Pentesting mindmap by Orange-Cyberdefense](https://github.com/Orange-Cyberdefense/arsenal/raw/master/mindmap/pentest_ad.png)

	- [Reddit resource on AD by u/apoklinon](https://www.reddit.com/r/oscp/comments/s1k6wk/pentesting_ad_mindmap/)

	- [AD resource by FareedFauzi](https://fareedfauzi.gitbook.io/oscp-notes/others/active-directory-attack)

	- [Tarlogic Security AD Cheatsheet](https://gist.github.com/TarlogicSecurity/2f221924fef8c14a1d8e29f3cb5c5c4a)

	- [Silver Tickets vs Golden Tickets](https://adsecurity.org/?p=1515)

5. Reddit Resources

	- [Kerberoasting](https://www.pentestpartners.com/security-blog/how-to-kerberoast-like-a-boss/)

	- [Tarlogic Cheatsheet](https://gist.github.com/TarlogicSecurity/2f221924fef8c14a1d8e29f3cb5c5c4a)

	- [Kerberoasting again](https://www.hackingarticles.in/deep-dive-into-kerberoasting-attack/)

	- https://malicious.link/post/2016/kerberoast-pt1/

	- https://tajdini.net/blog/penetration/active-directory-penetration-mind-map/

	- https://www.whiteoaksecurity.com/blog/attacks-defenses-dumping-lsass-no-mimikatz/

	- https://www.xmind.net/m/5dypm8/

	- Google Kerberoasting + GetUserSPN

### RPC

1. Information Gathering:

	- rpcclient
	
	- anonymous authentication

### SMB

1. Information Gathering:

	- nmap scans for vulnerabilities

	- anonymous authentication

	- enumerate other vectors for credentials
	
	- smbclient/smbmap

	- obtain smb version
	
		- smbver.py
	
		- wireshark
	
		- nmap

2. Exploit (some examples)		

	- MS08-067
	
	- Symlink Directory Traversal

	- usermap_script

	- MS17-010

### SNMP

1. Information Gathering

	- snmpwalk

		- [nsExtendOutput1Line Fails with SNMPD on Debian Wheezy](nsExtendOutput1Line Fails with SNMPD on Debian Wheezy)

### Oracle TNS Listener

1. Others

	- Methodology: SID -> Username/Password -> Exploit

	- odat tool + sqlplus 

	- [sqlplus installation](https://github.com/rapid7/metasploit-framework/wiki/How-to-get-Oracle-Support-working-with-Kali-Linux)

	- [use `--sysdba` flag if insufficient privileges and all privesc methods fail](https://stackoverflow.com/questions/35199084/forgot-oracle-username-and-password-how-to-retrieve) 

	- [sqlplus: error while loading shared libraries: libsqlplus.so: cannot open shared object file: No such file or directory](https://stackoverflow.com/questions/27717312/sqlplus-error-while-loading-shared-libraries-libsqlplus-so-cannot-open-shared#:~:text=It%20means%20you%20didn't,It%20will%20be%20working.)

	- [ODAT PrivEsc](https://github.com/quentinhardy/odat/wiki/privesc)

	- [Spartan Blog on Hacking Oracle](https://blog.spartan-cybersec.com/how-to-hack-an-oracle-database-server/)

	- [Hacking Oracle by OWASP](https://owasp.org/www-pdf-archive//ASDC12-New_and_Improved_Hacking_Oracle_From_Web.pdf)

### TFTP

1. Information Gathering:

	- Arbitrary File Disclosure (you will need to know path to file)

### Apache James

1. Information Gathering

	- Default Credentials (root/root)

	- Bruteforce authentication

	- Weak passwords

### POP3

1. Information Gathering***

	- Manual enumeration (Require credentials)

	- Bruteforce authentication (need email)

	- Weak passwords (need email)

2. Others

	- [Commands cheatsheet](https://www.atmail.com/blog/imap-commands/)

### Linux PrivEsc

1. Information Gathering

	- sudo -l

	- Cronjobs/Schedulers

	- linEnum

	- linpeas

	- lse.sh

	- linux exploit suggester

	- Searchsploit/enumerate binaries/files/services

		- Most likely need to be run/owned by Root

		- Not so simple

	- If can read /etc/passwd file or /home directory, try bruteforcing user passwords

		- if SSH is enabled, use hydra

		- if SSH disabled, try commonly used passwords or even the username itself as the password

2. Exploit

	- Insecure File Permissions (at least writeable access)

	- SUID/GTFO Bins

	- Docker/lxd/lxc Container Exploit
	
	- Linux Kernel Exploit

		- Searchsploit/LSE may not detect the exploit, sometimes, you need to Google and use the first few results

	- If you have the plaintext password of a user, can try running `su -` or `sudo su`, and you should get root if you are allowed to run sudo or su

### Windows PrivEsc

1. Information Gathering

	- Sherlock.ps1
	
		- [How to use sherlock?](https://vk9-sec.com/sherlock-find-missing-windows-patches-for-local-privilege-escalation/)
	
	- Watson.exe
	
	- [wes](https://github.com/bitsadmin/wesng)
	
	- [Windows Exploit Suggester](https://github.com/AonCyberLabs/Windows-Exploit-Suggester)
	
	- JAWS
	
	- WinPEAS
	
	- whoami /groups
	
	- whoami /priv

	- [Windows KE Enumeration - Sakshamdix pt 1](https://www.sakshamdixit.com/enumerate-windows-exploit-part-1/)
	
	- [Windows KE Enumeration - Sakshamdix pt 2](https://www.sakshamdixit.com/enumerate-windows-exploit-part-2/)
	
	- Searchsploit/enumerate binaries/files/services

		- Most likely need to be run/owned by NT AUTHORITY/SYSTEM

		- Not so simple

	- AlwaysInstallElevated (Love HTB)
		
2. Exploit

	- Bypass UAC
	
	- Insecure File Permissions (at least writeable access)
	
	- Unquoted Service Paths
	
	- Juicy Potatoes
	
	- Windows Kernel Exploit
	
		- Searchsploit/WES may not detect the exploit, sometimes, you need to Google and use the first few results

3. Others

	- [Kakyouim Windows KE Cheatsheet](https://kakyouim.hatenablog.com/entry/2020/05/27/010807#MS10_015-high)
		
		- if windows exploit suggesters/winpeas failing, run systeminfo and slowly cross check with the compiled list here
		
		- If real don't have, can also try to google/searchsploit the windows OS version for KE exploits

	- [Windows Priv Esc Cheatsheet by swisskyrepo](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Windows%20-%20Privilege%20Escalation.md)

### Buffer Overflow

1. Exploit

	- Fuzz the vulnerable program until it crashes
	
	- Use msfpattern to generate pattern, use it to find exact number of initial buffer
	
	- Show that initial buffer is correct and EIP is controlled

2. Others

	- gdp-peda: helps with debugging and analysing binaries

	- ldd: helps to see location of library in memory

	- checksec: helps to see properties of binaries
 
	- readelf & strings: get offsets of calls from memory location of library

	- ASLR enabled: randomize location of programs in memory

		- Solution: run exploit repeatedly in loop if the range is small
	
	- NX enabled: cannot run shellcode in stack (where we usually run shellcode)

		- Solution: return to libc attack - instead of dropping shellcode in stack, we can drop the memory address of system call in linux pointed to a string which we will input (e.g. /bin/bash)

### Windows Post Exploitatiion

- [Emilyanncr Cheatsheet](https://github.com/emilyanncr/Windows-Post-Exploitation)

### Linux Post Exploitation

- [Mubix Cheatsheet](https://github.com/mubix/post-exploitation/wiki/Linux-Post-Exploitation-Command-List)

### Others

- Installing impacket for python2

	```
	1- u need to install the old pip (unofficial way),

	curl https://bootstrap.pypa.io/pip/2.7/get-pip.py -o get-pip.py
	python get-pip.py
	
	2- Weird, it doesn't update the PATH, so u need to do it manually
	
	PATH=/home/kali/.local/bin:$PATH
	
	3- to confirm, u have PIP v2 not v3;
	
	└─$ pip --version
	pip 20.3.4 from /home/kali/.local/lib/python2.7/site-packages/pip (python 2.7)
	
	4- install some packages;
	
	pip install --upgrade setuptools
	
	5- Finally, install impacket;
	
	pip install impacket 
	```
	
- May have to change the exploit depending on scenario

	- HTB Optimum/Certain Box in OSCP
