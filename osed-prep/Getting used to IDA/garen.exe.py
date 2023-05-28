import base64
import string
import random

# https://stackoverflow.com/questions/58917280/how-can-i-base64-encode-using-a-custom-letter-set
# https://github.com/kingaling/custombase64/blob/master/custombase64.py

encoded_string     = "xDuebTK0Wjirx2ihWRKCN1l0JAV5NDSeaDirW21eyEaexjRrV29q"
decoded_string     = 'playctfinsideCECZ4069@eatingmalware.com'
std_base64chars    = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
custom_base64chars = "ZYXABCDEFGHIJKLMNOPQRSTUVWzyxabcdefghijklmnopqrstuvw0123456789+/"

encodedset = string.maketrans(std_base64chars, custom_base64chars)
decodedset = string.maketrans(custom_base64chars, std_base64chars)

def dataencode(x):
    y = base64.b64encode(x)
    y = y.translate(encodedset)
    return y

def datadecode(x):
    y = x.translate(decodedset)
    y = base64.b64decode(y)
    return y

enc = dataencode(decoded_string)
dec = datadecode(encoded_string)

print("Use Python2 to run!")

print(enc)
print(dec)

print(enc == encoded_string)
print(dec == decoded_string)

