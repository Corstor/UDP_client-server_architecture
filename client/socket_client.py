# -*- coding: utf-8 -*-
import socket as sk
import os
import shlex
import time

BUFFER_SIZE = 4096
SERVER_ADDRESS = ('localhost', 49000)

def get(fileName):
    socket.sendto((command + ' "' + fileName + '"').encode(), SERVER_ADDRESS)
    data = str(fileName).encode()
    received, server = socket.recvfrom(BUFFER_SIZE)
    if (int(received.decode('utf8')) == 1):
        origin_file_size, server = socket.recvfrom(BUFFER_SIZE)
        origin_file_size = int(origin_file_size.decode('utf8'))
        with open(fileName, 'wb') as file:
            while True:
                bytes_read = socket.recv(BUFFER_SIZE)
                if not bytes_read:
                    break
                file.write(bytes_read)  
        file_size = os.path.getsize(fileName) #bytes ricevuti
        if file_size != origin_file_size:
            print('\nERROR\n')
            print(str(origin_file_size - file_size) + ' bytes lost\n')
        else:
            print("\nThe file has been received correctly")
    else:
        print('\nERROR\n')
        print("The file is not in the server")
    return data
        
def put(fileName):
    with open(fileName, 'rb') as file:
        file_size = os.path.getsize(fileName)#bytes inviati
        print ('sending', command + ' ' + fileName + ' ' + str(file_size) + ' bytes')
        socket.sendto((command + ' "' + fileName + '"').encode(), SERVER_ADDRESS)
        while True:
            time.sleep(0.0001)
            bytes_read = file.read(BUFFER_SIZE)
            if not bytes_read:
                socket.sendto(''.encode(), SERVER_ADDRESS)
                break # file transmitting done
            socket.sendto(bytes_read, SERVER_ADDRESS)
    data, server = socket.recvfrom(BUFFER_SIZE)
    received_file_size, server = socket.recvfrom(BUFFER_SIZE)
    received_file_size = int(received_file_size.decode('utf8'))
    if file_size != received_file_size:
        print('\nERROR\n')
        print(str(file_size - received_file_size) + ' bytes lost\n')
    return data

while True:
    # Creiamo il socket UDP
    socket = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
        
    command = input('\nYou can choose between:\n \
    list: see the list of all the files on the server\n \
    get FILE_NAME: get a file from the server\n \
    put FILE_PATH/FILE_NAME: put a file into the server\n\n')
    
    try:
        if len(shlex.split(command)) == 2:
            command , fileName = shlex.split(command);
            if command == 'put':
                data = put(fileName)
            else:
                if command == 'get':
                    data = get(fileName)
                else:
                    data = "Error".encode()
                    print("The command is not supported")
        else:
            socket.sendto(command.encode(), SERVER_ADDRESS)
            data, server = socket.recvfrom(BUFFER_SIZE)
            
        print ('\n%s\n' % data.decode('utf8'))
        
    except Exception as info:
        print(info)
    finally:
        print ('closing socket')
        socket.close()

