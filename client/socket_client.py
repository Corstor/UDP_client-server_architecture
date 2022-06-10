# -*- coding: utf-8 -*-
import socket as sk
import os
import shlex
import time

BUFFER_SIZE = 4096
SERVER_ADDRESS = ('localhost', 49000)


def get(command, fileName):
    
    # Send command to server
    socket.sendto((command + ' "' + fileName + '"').encode(), SERVER_ADDRESS)
    
    # Response from the server to start the operation
    received, server = socket.recvfrom(BUFFER_SIZE)
    
    # Receive file size from the server
    if (int(received.decode('utf8')) == 1):
        origin_file_size, server = socket.recvfrom(BUFFER_SIZE)
        origin_file_size = int(origin_file_size.decode('utf8'))
        
        print ('\nDownloading' + ' ' + fileName + ' ' + str(origin_file_size) + ' bytes')
        
        # Receive bytes of the file
        with open(fileName, 'wb') as file:
            while True:
                bytes_read = socket.recv(BUFFER_SIZE)
                
                # File transmitting done
                if not bytes_read:
                    break
                
                # Write bytes on file
                file.write(bytes_read)  
                
        # Bytes received
        file_size = os.path.getsize(fileName)
        
        # Check for error
        if file_size != origin_file_size:
            print('\nERROR\n')
            print(str(origin_file_size - file_size) + ' bytes lost\n')
        else:
            print("\nFile downloaded correctly")
            
    else:
        print('\nERROR\n')
        print("The file is not in the server")
        
        
def put(command, fileName):
    
    with open(fileName, 'rb') as file:

        # Bytes to send
        file_size = os.path.getsize(fileName)
        print ('\nUploading' + ' ' + fileName + ' ' + str(file_size) + ' bytes')
        socket.sendto((command + ' "' + fileName + '"').encode(), SERVER_ADDRESS)
        
        # Send bytes
        while True:
            time.sleep(0.0001)
            bytes_read = file.read(BUFFER_SIZE)
            
            # File transmitting done
            if not bytes_read:
                socket.sendto(''.encode(), SERVER_ADDRESS)
                break
                
            socket.sendto(bytes_read, SERVER_ADDRESS)
            
    # Receive file size from the server
    received_file_size, server = socket.recvfrom(BUFFER_SIZE)
    received_file_size = int(received_file_size.decode('utf8'))
    
    # Check for error
    if file_size != received_file_size:
        print('\nERROR\n')
        print(str(file_size - received_file_size) + ' bytes lost\n')
    else:
        print("\nFile uploaded correctly")


while True:
    
    # Socket creation
    socket = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
        
    command = input('\nYou can choose between:\n \
    list: see the list of all the files on the server\n \
    get FILE_NAME: get a file from the server\n \
    put (FILE_PATH)/FILE_NAME: put a file into the server\n\n')
    
    try:
        if len(shlex.split(command)) == 2:
            command , fileName = shlex.split(command);
            
            if command == 'put':
                put(command, fileName)
            elif command == 'get':
                get(command, fileName)
            else:
                data = "Error".encode()
                print("The command is not supported")
        else:
            if command == "get":
                print("The get command expects the FILE_NAME as a parameter")
            else:
                if command == "put":
                    print("The put command expects a (FILE_PATH)/FILE_NAME as a parameter")
                else:
                    #Send command to the server
                    socket.sendto(command.encode(), SERVER_ADDRESS)
                    data, server = socket.recvfrom(BUFFER_SIZE)
                    
                    #Print server response
                    print ('\n%s\n' % data.decode('utf8'))
        
        
    except Exception as info:
        print(info)
