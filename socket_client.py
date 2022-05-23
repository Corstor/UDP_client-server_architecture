# -*- coding: utf-8 -*-
import socket as sk
import time

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
        time.sleep(2) #attende 2 secondi prima di inviare la richiesta
        sent = socket.sendto(command.encode(), server_address)
        
        # Ricevete la risposta dal server
        print('\nwaiting to receive from')
        data, server = socket.recvfrom(4096)
        #print(server)
        time.sleep(2)
        print ('received message "%s"' % data.decode('utf8'))
    except Exception as info:
        print(info)
    finally:
        print ('closing socket')
        socket.close()

