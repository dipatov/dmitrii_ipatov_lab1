import socket
import random

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind(('192.168.8.112', 6121))

client = []

mis = 1

def change_letter(word, let, i):
    return word[:i] + let + word[i + 1:]

def correct_mist(word, ind):
    corr = b'0'
    if word[ind] == b'0':
        corr = b'1'
    return change_letter(word, corr, ind)

print ('Start Server')
try:
    while 1:
             data , address = sock.recvfrom(1024)
             if  address not in client:
                     client.append(address)

             if address == ('192.168.8.112', 12451):
                 if data != b'':
                     for i in range(random.randint(0,mis)):
                         data = correct_mist(data, random.randint(0,len(data) - 1))

             for clients in client:
                     if clients == address :
                         continue
                     sock.sendto(data,clients)

finally:
    sock.close()
