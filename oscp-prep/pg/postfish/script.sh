#!/bin/bash
# ./script.sh | nc 192.168.222.137 25

for sender in $(cat /home/george93/usernamer/new_custom_email.txt)
do
	for rcv in $(cat /home/george93/usernamer/new_custom_email.txt)
	do
		echo "mail from:$sender"
		echo "rcpt to:$rcv"
		echo "data"
		echo "Subject: testing"
		echo "http://192.168.49.222"
		echo "."
	done
done
		
		
