# -*- coding: utf-8 -*-
import socket as sk
import shlex
import os
import time
from os import listdir
from os.path import isfile, join

BUFFER_SIZE = 4096
ADDRESS = ('localhost', 49000)

def get(fileName, filesList):
    print("Received command get")
    if fileName in filesList:
        file_size = os.path.getsize('./serverFiles/' + fileName)#bytes inviati
        with open('./serverFiles/' + fileName, 'rb') as file:
            sock.sendto('1'.encode(), ADDRESS)
            sock.sendto((str(file_size)).encode(), ADDRESS)
            while True:
                time.sleep(0.0001)
                bytes_read = file.read(BUFFER_SIZE)
                if not bytes_read:
                    sock.sendto(''.encode(), ADDRESS)
                    break # file transmitting done
                sock.sendto(bytes_read, ADDRESS)
        print("File downloaded")
    else:
        #ERROR
        #When the file does not exist
        print("Error")
        sock.sendto('0'.encode(), ADDRESS)
        
def put(fileName, filesList):
    print("Received command put")
    fileName = os.path.basename(fileName)
    filesList.append(fileName)
    with open('./serverFiles/' + fileName, 'wb') as file:
        while True:
            bytes_read = sock.recv(BUFFER_SIZE)
            if not bytes_read:
                break
            file.write(bytes_read)
    file_size = os.path.getsize('./serverFiles/' + fileName) #bytes ricevuti
    sock.sendto(str(file_size).encode(), ADDRESS)
    print("File uploaded")

# Socket creation
sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)

# Binding the socket to the port
sock.bind(ADDRESS)
print ('\n\rstarting up on %s port %s' % ADDRESS)

filesList = [f for f in listdir("./serverFiles") if isfile(join("./serverFiles", f))]

while True:
    
    print('\n\rWaiting to receive message...')
    data, ADDRESS = sock.recvfrom(BUFFER_SIZE)
    filesList = [f for f in listdir("./serverFiles") if isfile(join("./serverFiles", f))]
    data = data.decode('utf8')
    if data == 'list':
        if len(filesList) > 0:
            sock.sendto('\n'.join(filesList).encode(), ADDRESS)
            print("Files list sent")
        else:
            #There are no files in the server files
            print("Error")
            sock.sendto('Files list is empty.'.encode(), ADDRESS)
    else:
        if len(shlex.split(data)) < 2:
            #ERROR
            #When the command is not supported
            sock.sendto('Command not recognized'.encode(), ADDRESS)
        elif len(shlex.split(data)) > 2:
            #ERROR
            #When the command is not complete
            print("Error")
            sock.sendto('With get and put commands is required one argument: FILE_NAME'.encode(), ADDRESS)
        else:
            command , fileName = shlex.split(data);
            if command == 'get':
                get(fileName, filesList)
            elif command == 'put':
                put(fileName, filesList)
            else:
                #ERROR
                #When the command is not supported
                print("Error")
                sock.sendto('Command not recognized'.encode(), ADDRESS)
                