# -*- coding: utf-8 -*-
import socket as sk
import time

BUFFER_SIZE = 4096

while True:
    # Creiamo il socket UDP
    socket = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
    
    server_address = ('localhost', 54000)

    print('\n You can choose between:\n')
    print('-list: see the list of all the files on the server\n')
    print('-get FILE_NAME: get a file from the server\n')
    print('-put FILE_PATH/FILE_NAME: put a file into the server\n')
    command = input()
    
    try:
        # invia il messaggio
        print ('sending "%s"' % command)
        time.sleep(1)
        sent = socket.sendto(command.encode(), server_address)
        
        # Ricevete la risposta dal server
        print('\nwaiting to receive from')
        time.sleep(1)
        data, server = socket.recvfrom(BUFFER_SIZE)
        data = data.decode('utf8')
        if data == 'get':
            command, fileName = command.split(' ', 1)
            with open(fileName, 'wb') as file:
                while True:
                    time.sleep(1)
                    bytes_read = socket.recv(BUFFER_SIZE)
                    if not bytes_read:
                        break
                    print (bytes_read)
                    file.write(bytes_read)
                    print("ciao")
        
        #print(server)
        print ('received message "%s"' % data)
    except Exception as info:
        print(info)
    finally:
        print ('closing socket')
        socket.close()

