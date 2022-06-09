def get(fileName, filesList, address, BUFFER_SIZE):
    
    print("Received command get")
    if fileName in filesList:
        file_size = os.path.getsize('./serverFiles/' + fileName)#bytes inviati
        with open('./serverFiles/' + fileName, 'rb') as file:
            sock.sendto('1'.encode(), address)
            sock.sendto((str(file_size)).encode(), address)
            while True:
                time.sleep(0.0001)
                bytes_read = file.read(BUFFER_SIZE)
                if not bytes_read:
                    sock.sendto('File downloaded correctly'.encode(), address)
                    break # file transmitting done
                sock.sendto(bytes_read, address)
        print("File downloaded")
    else:
        #ERROR
        #When the file does not exist
        print("Error")
        sock.sendto('0'.encode(), address)
        
def put(fileName, filesList, address, BUFFER_SIZE):
    print("Received command put")
    fileName = os.path.basename(fileName)
    filesList.append(fileName)
    with open('./serverFiles/' + fileName, 'wb') as file:
        while True:
            bytes_read = sock.recv(BUFFER_SIZE)
            if not bytes_read:
                break
            file.write(bytes_read)
        sock.sendto('File uploaded correctly'.encode(), address)
    file_size = os.path.getsize('./serverFiles/' + fileName) #bytes ricevuti
    sock.sendto(str(file_size).encode(), address)
    print("File uploaded")

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
print ('\n\rstarting up on %s port %s' % server_address)
sock.bind(server_address)
BUFFER_SIZE = 4096

filesList = [f for f in listdir("./serverFiles") if isfile(join("./serverFiles", f))]

while True:
    
    print('\n\rWaiting to receive message...')
    data, address = sock.recvfrom(BUFFER_SIZE)
    filesList = [f for f in listdir("./serverFiles") if isfile(join("./serverFiles", f))]
    data = data.decode('utf8')
    if data == 'list':
        if len(filesList) > 0:
            sock.sendto('\n'.join(filesList).encode(), address)
            print("Files list sent")
        else:
            #There are no files in the server files
            print("Error")
            sock.sendto('Files list is empty.'.encode(), address)
    else:
        if len(shlex.split(data)) < 2:
            #ERROR
            #When the command is not supported
            sock.sendto('Command not recognized'.encode(), address)
        elif len(shlex.split(data)) > 2:
            #ERROR
            #When the command is not complete
            print("Error")
            sock.sendto('With get and put commands is required one argument: FILE_NAME'.encode(), address)
        else:
            command , fileName = shlex.split(data);
            if command == 'get':
                get(fileName, filesList, address, BUFFER_SIZE)
            elif command == 'put':
                put(fileName, filesList, address, BUFFER_SIZE)
            else:
                #ERROR
                #When the command is not supported
                print("Error")
                sock.sendto('Command not recognized'.encode(), address)
                