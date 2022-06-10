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
        # Bytes to send
        file_size = os.path.getsize('./serverFiles/' + fileName)
        
        with open('./serverFiles/' + fileName, 'rb') as file:
            
            # Message to the client to start the operation
            sock.sendto('1'.encode(), ADDRESS)
            
            # Send file size
            sock.sendto((str(file_size)).encode(), ADDRESS)

            # Send bytes
            while True:
                time.sleep(0.0001)
                bytes_read = file.read(BUFFER_SIZE)
                
                # File transmitting done
                if not bytes_read:
                    sock.sendto(''.encode(), ADDRESS)
                    break
                    
                sock.sendto(bytes_read, ADDRESS)
                
        print("File downloaded")
        
    else:
        # ERROR
        # When the file does not exist
        print("Error")
        sock.sendto('0'.encode(), ADDRESS)
        
        
def put(fileName, filesList):
    
    print("Received command put")
    
    # Add file to files list
    fileName = os.path.basename(fileName)
    filesList.append(fileName)
    
    # Receive bytes of the file
    with open('./serverFiles/' + fileName, 'wb') as file:
        while True:
            bytes_read = sock.recv(BUFFER_SIZE)
            
            # File transmitting done
            if not bytes_read:
                break
            
            # Write bytes on file
            file.write(bytes_read)
    
    # Bytes received
    file_size = os.path.getsize('./serverFiles/' + fileName)
    sock.sendto(str(file_size).encode(), ADDRESS)
    
    print("File uploaded")
    

# Socket creation
sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)

# Binding the socket to the port
sock.bind(ADDRESS)
print ('\n\rstarting up on %s port %s' % ADDRESS)

# List that contains the files
filesList = [f for f in listdir("./serverFiles") if isfile(join("./serverFiles", f))]

while True:
    
    print('\n\rWaiting to receive message...')
    
    # Update files list
    data, ADDRESS = sock.recvfrom(BUFFER_SIZE)
    filesList = [f for f in listdir("./serverFiles") if isfile(join("./serverFiles", f))]
    data = data.decode('utf8')
    
    if data == 'list':
        if len(filesList) > 0:
            sock.sendto('\n'.join(filesList).encode(), ADDRESS)
            print("Files list sent")
        else:
            # There are no files in the server files
            print("Error")
            sock.sendto('Files list is empty.'.encode(), ADDRESS)
            
    else:
        if len(shlex.split(data)) < 2:
            # ERROR
            # When the command is not supported
            sock.sendto('Command not recognized'.encode(), ADDRESS)
        elif len(shlex.split(data)) > 2:
            # ERROR
            # When the command is not complete
            print("Error")
            sock.sendto('With get and put commands is required one argument: FILE_NAME'.encode(), ADDRESS)
        else:
            command , fileName = shlex.split(data);
            if command == 'get':
                get(fileName, filesList)
            elif command == 'put':
                put(fileName, filesList)
            else:
                # ERROR
                # When the command is not supported
                print("Error")
                sock.sendto('Command not recognized'.encode(), ADDRESS)
                