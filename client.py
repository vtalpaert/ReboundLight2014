'''
Created on 7 mai 2014

@author: victor-clevo
'''
import socket, sys, time

HOST, PORT = '127.0.0.1', 233
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

for i in range(5):
    print i
    sock.sendall("%d\n" % i)
    time.sleep(1)
print 'Closing socket'
sock.close()
