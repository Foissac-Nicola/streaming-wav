#-*- coding: utf-8 -*-

import socket, sys

HOST = '127.0.0.1'
PORT = 7800

# 1) creation of a socket :
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 2) try to connect to the server:
try:
    mySocket.connect((HOST, PORT))

except socket.error as err:
    print(err)
    sys.exit()    
print("Connected to the server.")


# 3) Interacts with the server:
msgClient = "OPTIONS rtsp:/home/nfoissac/Bureau/dcn_alter/streaming-wav/streamapp/static/media/wav/treize.wav RTSP/1.0\nCSeq: 1"
mySocket.send(msgClient.encode("Utf8"))



while 1:
    msgServeur = mySocket.recv(1024)
    if not msgServeur:
        break
    print(msgServeur)
 
# 4) Closing connexion :
print("\n Connexion closed.")
mySocket.close()

        
        

