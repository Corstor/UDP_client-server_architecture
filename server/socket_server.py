# -*- coding: utf-8 -*-
import socket as sk
import shlex
import os
import time
from os import listdir
from os.path import isfile, join

# Creiamo il socket
sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)

# associamo il socket alla porta
server_address = ('localhost', 49000)
print ('\n\r starting up on %s port %s' % server_address)
sock.bind(server_address)
BUFFER_SIZE = 4096

filesList = [f for f in listdir("./serverFiles") if isfile(join("./serverFiles", f))]

while True:
    
    print('\n\r waiting to receive message...')
    data, address = sock.recvfrom(BUFFER_SIZE)

    print('received %s bytes from %s' % (len(data), address))
    data = data.decode('utf8')
    print (data)
    if data == 'list':
        filesList = [f for f in listdir("./serverFiles") if isfile(join("./serverFiles", f))]

        if len(filesList) > 0:
            sent = sock.sendto('\n'.join(filesList).encode(), address)
        else:
            sent = sock.sendto('Files list is empty.'.encode(), address)
    else:
        if len(shlex.split(data)) < 2:
            sent = sock.sendto('Command not recognized'.encode(), address)
        elif len(shlex.split(data)) > 2:
            sent = sock.sendto('With get and put commands is required one other argument FILE_NAME'.encode(), address)
        else:
            command , fileName = shlex.split(data);
            if command == 'get':
                if fileName in filesList:
                    file_size = os.path.getsize('./serverFiles/' + fileName)#bytes inviati
                    print(file_size, "bytes")
                    with open('./serverFiles/' + fileName, 'rb') as file:
                        sent = sock.sendto('get'.encode(), address)
                        sent = sock.sendto((str(file_size)).encode(), address)
                        while True:
                            time.sleep(0.0001)
                            bytes_read = file.read(BUFFER_SIZE)
                            if not bytes_read:
                                sent = sock.sendto(''.encode(), address)
                                break # file transmitting done
                            sent = sock.sendto(bytes_read, address)
                else:
                    sent = sock.sendto('File not found'.encode(), address)
            else: 
                if command == 'put':
                    fileName = os.path.basename(fileName)
                    filesList.append(fileName)
                    with open('./serverFiles/' + fileName, 'wb') as file:
                        while True:
                            bytes_read = sock.recv(BUFFER_SIZE)
                            if not bytes_read:
                                break
                            file.write(bytes_read)
                        sent = sock.sendto(fileName.encode(), address)
                    file_size = os.path.getsize('./serverFiles/' + fileName) #bytes ricevuti
                    print(file_size, "bytes")
                    sent = sock.sendto(str(file_size).encode(), address)
                else:
                    sent = sock.sendto('Command not recognized'.encode(), address)
                