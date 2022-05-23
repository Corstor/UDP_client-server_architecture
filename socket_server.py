# -*- coding: utf-8 -*-
import socket as sk
import time

# Creiamo il socket
sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)

# associamo il socket alla porta
server_address = ('localhost', 54000)
print ('\n\r starting up on %s port %s' % server_address)
sock.bind(server_address)
filesList = []

while True:
    print('\n\r waiting to receive message...')
    data, address = sock.recvfrom(4096)

    print('received %s bytes from %s' % (len(data), address))
    data = data.decode('utf8')
    print (data)
    
    if data == 'list':
        time.sleep(2)
        if len(filesList) > 0:
            sent = sock.sendto(' '.join(filesList).encode(), address)
        else:
            sent = sock.sendto('errore'.encode(), address)
    else:
        if len(data.split()) != 2:
            sent = sock.sendto('errore'.encode(), address)
        else:
            data1 , data2 = data.split(' ', 1);
            time.sleep(2)
            
            if data1 == 'get':
                sent = sock.sendto(data2.encode(), address)
                print(data2)
            else: 
                if data1 == 'put':
                    sent = sock.sendto(data2.encode(), address)
                    print(data2)
                else:
                    sent = sock.sendto('errore'.encode(), address)
    