# -*- coding: utf-8 -*-
import socket as sk
import os
import shlex
import time

BUFFER_SIZE = 4096

while True:
    # Creiamo il socket UDP
    socket = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
    
    server_address = ('localhost', 49000)

    command = input('\n You can choose between:\n \
    -list: see the list of all the files on the server\n \
    -get FILE_NAME: get a file from the server\n \
    -put FILE_PATH/FILE_NAME: put a file into the server\n\n')
    
    try:
        
        if command == 'list':
            sent = socket.sendto(command.encode(), server_address)
            data, server = socket.recvfrom(BUFFER_SIZE)
        else:
            if len(shlex.split(command)) == 2:
                command , fileName = shlex.split(command);
                if command == 'put':
                    with open(fileName, 'rb') as file:
                        print("1")
                        file_size = os.path.getsize(fileName)#bytes inviati
                        print ('sending ', command + ' ' + fileName + ' ' + file_size + 'bytes')
                        sent = socket.sendto((command + ' "' + fileName + '"').encode(), server_address)
                        sent = socket.sendto((str(file_size)).encode(), server_address)
                        while True:
                            time.sleep(0.0005)
                            bytes_read = file.read(BUFFER_SIZE)
                            if not bytes_read:
                                sent = socket.sendto(''.encode(), server_address)
                                break # file transmitting done
                            sent = socket.sendto(bytes_read, server_address)
                    data, server = socket.recvfrom(BUFFER_SIZE)
                else:
                    sent = socket.sendto((command + ' "' + fileName + '"').encode(), server_address)
                    # Ricevete la risposta dal server
                    print('\nwaiting to receive from')
                    data, server = socket.recvfrom(BUFFER_SIZE)
                    data = data.decode('utf8')
                    if data == 'get':
                        data = data.encode()
                        origin_file_size, server = socket.recvfrom(BUFFER_SIZE)
                        origin_file_size = int(origin_file_size.decode('utf8'))
                        print(origin_file_size)
                        with open(fileName, 'wb') as file:
                            while True:
                                bytes_read = socket.recv(BUFFER_SIZE)
                                if not bytes_read:
                                    break
                                file.write(bytes_read)  
                        file_size = os.path.getsize(fileName) #bytes ricevuti
                        print(file_size, "bytes")
                        if file_size != origin_file_size:
                            print('Some packets may lost')
        print ('received message "%s"' % data.decode('utf8'))
    except Exception as info:
        print(info)
    finally:
        print ('closing socket')
        socket.close()

