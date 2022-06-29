program generates a random number, sends it to client in decimal form and asks for it to be translated into 32 bit little endian format (how the number itself is stored in memory, which is also the format that we are comparing the input to)

import socket
import struct

HOST="127.0.0.1"
PORT=2999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
data = s.recv(1024)
print "Received following data from socket: " + data

value = filter(str.isdigit, data) # extract number from data
value = value[:-2] # last 2 digits is 32 which indicates that it is 32bit

payload = struct.pack("I", int(value)) #32 bit little endian format
s.send(payload)
data = s.recv(1024)
print "Received following data from socket: " + data


for this level, the number stored in fub is stored as a decimal, hence you don't have to pack it into bytes

https://www.delftstack.com/howto/python/how-to-convert-bytes-to-integers/

import socket
import struct
import time

HOST="127.0.0.1"
PORT=2998

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
data = s.recv(1024) # need to be big enough to properly get the full data sent from socket
print "Received following data from socket: ", data

# s.send(str(1111111111)) # fuzzing input need to be bigger
payload = struct.unpack("I", data)[0]
print "Decoded ", data, " into: ", payload
s.send(str(payload))

time.sleep(1) # prevent socket from hanging
print s.recv(1024)
s.close()









import socket
import struct
import time

HOST="127.0.0.1"
PORT=2997

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

final = 0

data = s.recv(1024) # need to be big enough to properly get the full data sent from socket
print "Received following data from socket: ", data
decoded = struct.unpack("I", data)[0]
print "Decoded ", data, " into: ", decoded
final += decoded

data1 = s.recv(1024) # need to be big enough to properly get the full data sent from socket
print "Received following data1 from socket: ", data1
decoded = struct.unpack("I", data1)[0]
print "Decoded ", data1, " into: ", decoded
final += decoded

data2 = s.recv(1024) # need to be big enough to properly get the full data sent from socket
print "Received following data2 from socket: ", data2
decoded = struct.unpack("I", data2)[0]
print "Decoded ", data2, " into: ", decoded
final += decoded

data3 = s.recv(1024) # need to be big enough to properly get the full data sent from socket
print "Received following data3 from socket: ", data3
decoded = struct.unpack("I", data3)[0]
print "Decoded ", data3, " into: ", decoded
final += decoded

print "Final Payload: ", final

print "Final Payload accounting for integer overflow: ", final & 0xffffffff

payload = struct.pack("I", final & 0xffffffff)

s.send(str(payload))

data4 = s.recv(1024) # need to be big enough to properly get the full data sent from socket
print "Received following data from socket: ", data4






