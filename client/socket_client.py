# -*- coding: utf-8 -*-
import socket as sk

BUFFER_SIZE = 4096

while True:
    # Creiamo il socket UDP
    socket = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
    
    server_address = ('localhost', 51000)

    command = input('\n You can choose between:\n \
    -list: see the list of all the files on the server\n \
    -get FILE_NAME: get a file from the server\n \
    -put FILE_PATH/FILE_NAME: put a file into the server\n\n')
    
    try:
        print ('sending ', command)
        sent = socket.sendto(command.encode(), server_address)
        
        if len(command.split()) == 2:
            command , fileName = command.split(' ', 1);
            if command == 'put':
                with open(fileName, 'rb') as file:
                    while True:
                        bytes_read = file.read(BUFFER_SIZE)
                        if not bytes_read:
                            sent = socket.sendto(''.encode(), server_address)
                            break # file transmitting done
                        sent = socket.sendto(bytes_read, server_address)
                
            # Ricevete la risposta dal server
            print('\nwaiting to receive from')
            data, server = socket.recvfrom(BUFFER_SIZE)
            data = data.decode('utf8')
            if data == 'get':
                #command, fileName = command.split(' ', 1)
                with open(fileName, 'wb') as file:
                    while True:
                        bytes_read = socket.recv(BUFFER_SIZE)
                        if not bytes_read:
                            break
                        file.write(bytes_read)        
            #print(server)
            print ('received message "%s"' % data)
    except Exception as info:
        print(info)
    finally:
        print ('closing socket')
        socket.close()

