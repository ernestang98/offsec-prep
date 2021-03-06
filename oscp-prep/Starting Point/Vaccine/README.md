## Vaccine


1. nmap -sC -sV -Pn IP 

	![](./Screenshots/1nmap.png)

2. Following ports opened

	1. Port 80 (Apache HTTP Web Server)
	
		![](./Screenshots/1.2.png)
	
	2. Port 22 (SSH)
	
	3. Port 21 (FTP)

3. Enumrate FTP Server first 

	![](./Screenshots/2ftp.png)

4. Try to unzip file but they are locked

	![](./Screenshots/2.2.png)

5. According to this [link](https://linuxconfig.org/how-to-crack-zip-password-on-kali-linux), we can install the following modules and brute force the zipped password

	![](./Screenshots/3.png)
	
	![](./Screenshots/4.png)
	
6. Lets run the files on a webserver

	![](./Screenshots/5.1.png)

	![](./Screenshots/5.png)
	
7. Lets checkout the files

	![](./Screenshots/6.png)
	
8. Crack the hash value using this [link](https://crackstation.net/)

	![](./Screenshots/7.png)
	
9. Login with credentials admin & qwerty789

	![](./Screenshots/8.png)

10. Play around with website and looks like SQL injections are possible

	![](./Screenshots/9.png)

11. ilike seems to mean that postgresql is running 

	![](./Screenshots/1.1.png)

12. Trying SQLi manually to no avail

13. Let's use sqlmap to enumerate host (sqlmap is NOT allowed for OSCP)

	![](./Screenshots/12.png)

14. Use burpsuite or inspect browser cookie store to get cookies for sqlmap

	![](./Screenshots/10.png)

15. use `--os-shell` flag to obtain os shell, upgrade to reverse shell and connect it back via nc. Navigate through the various directories to get user flag

	![](./Screenshots/13.png)
	
	[How to get reverse shell from web shell? (add bash -c 'BASH SCRIPT')](https://w00troot.blogspot.com/2017/05/getting-reverse-shell-from-web-shell.html)
	
	[Upgrade shell to fully interactive ttys](https://blog.ropnop.com/upgrading-simple-shells-to-fully-interactive-ttys/)
	
16. Obtain user flag without using reverse shell or nc

	![](./Screenshots/14.png)

17. Directory traversal to /var/www/html/dashboard.php and get credentials for postgres user

	![](./Screenshots/15.png)
	
18. SSH to target using postgres credentials for more stable shell and obtain sudo privileges

	![](./Screenshots/16.png)
	
19. Get sudo privileges, realise that there is this strange message "User postgres may run the following commands on vaccine: ....". Looks like we are indeed able to run the following command with sudo privileges.

	![](./Screenshots/17.1.png)

20. According to this [link](https://gtfobins.github.io/gtfobins/vi/) and this [link](https://medium.com/@pettyhacks/linux-privilege-escalation-via-vi-36c00fcd4f5e), we can abuse the privilege of using vi to escalate our current privileges. So lets do that.

21. Oops the first method from the first link seems to have failed, let's use the second method

	1. First method 
	
		![](./Screenshots/18.png)
	
	2. Second method (press enter after every `:command`)
	
		![](./Screenshots/19.1.png)
		
		![](./Screenshots/19.2.png)
		
		![](./Screenshots/19.3.png)
		
		![](./Screenshots/19.4.png)
		
		![](./Screenshots/19.5.png)	

22. We can also use the method from the second link (didn't take the screenshots for the whole process but tested it and it works)

	![](./Screenshots/19.6.png)		

## Additional links on stuff (mostly on sqlmap)

- [SimpleHttpServer deprecated to http.server](https://stackoverflow.com/questions/7943751/what-is-the-python-3-equivalent-of-python-m-simplehttpserver)

- [Quickly starting a webserver in kali](https://medium.com/@narayan_snr/how-to-start-a-web-server-in-kali-linux-apache2-python-54b780bde351)

- [ftp exploits](https://www.globalscape.com/blog/top-4-ftp-exploits-used-hackers)

- [encountered this issue when trying to use sqlmap --os-pwn](https://github.com/rapid7/metasploit-framework/issues/13581)

- [linux web exploitation](https://mrw0r57.github.io/2020-05-30-linux-exploitation-9-2/)

- [os shell to reverse shell](https://www.youtube.com/watch?v=leFcSaiSgw0)

- [upload reverse shell using sqlmap](https://www.hackingarticles.in/shell-uploading-in-web-server-using-sqlmap/)

- [sqlmap enumeration](https://www.securesolutions.no/enumeration-with-sqlmap/)

- [sqlmap with burpsuite](https://resources.infosecinstitute.com/topic/important-sqlmap-commands/)

- [sqlmap for post authentication](http://suraj-raghuvanshi.blogspot.com/2014/06/sqlmap-for-post-authenticationafter.html)

- [printing values with sqlmap](https://hackertarget.com/sqlmap-tutorial/)

- [database enumeration with sqlmap (this is good!)](https://www.security-sleuth.com/sleuth-blog/2017/1/3/sqlmap-cheat-sheet)
