#-*- coding: utf-8 -*-

import socket as sock
import os
import fcntl
from time import sleep
import sys
from threading import Thread as thread , RLock as lock

mutex = lock()
chunk = 1024

# émision -> 7801
# reception -> 7800

class STRMServersend(thread):
    def __init__(self, address, port):
        thread.__init__(self)
        self.address = address
        self.port = port
        self.connection = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        self.connection.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)
        #fcntl.fcntl(self.connection, fcntl.F_SETFL, os.O_NONBLOCK)
        self.connection.bind((address, port))

        self.connection.listen(50)
        print("[+][streaming] New server started on " + address + ":" + str(port))

    def run(self):
        while True:
            print("&")
            client_connection, client_address = self.connection.accept()
            print(client_address)
            print(client_connection)
            request = client_connection.recv(1024)
            print(request)
            f = open('/home/nfoissac/Bureau/dcn_alter/streaming-wav/streamapp/static/media/wav/treize.wav', 'rb')
            # st = os.fstat(f.fileno())
            # length = st.st_size
            try:
                data = f.read(chunk)
                client_connection.send(data)
                while data:
                    data = f.read(chunk)
                    client_connection.send(data)
            except:
                break
            #self.conn.recv(1024)
        self.connection.close()

def tcp_video_thread():
    camera = cv2.VideoCapture(VIDEO_CAM_INDEX)
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection.bind((IP_SERVER, VIDEO_SERVER_PORT))
    connection.listen(MAX_NUM_CONNECTIONS_LISTENER)
    while True:
        (conn, (ip, port)) = connection.accept()
        thread = ConnectionPoolVideo(ip, port, conn, camera)
        thread.start()


STRMServersend("127.0.0.1",7800).start()

# class STRMServer:
#
#     def __init__(self,host="127.0.0.1",port=[7801,7800]) -> None:
#
#         self.host = host
#         self.port = port
#
#         self.socket_send = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
#         self.socket_send.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)
#
#
#         self.socket_recv = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
#         self.socket_recv.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)
#
#         try:
#             self.socket_send.bind((self.host, self.port[1]))
#             self.socket_recv.bind((self.host, self.port[0]))
#         except sock.error:
#             print("Socket binding to given adress has failed.")
#             sys.exit
#         self.socket_recv.listen(1)
#         self.socket_send.listen(1)
#         print('Sock recv on port %s ...' % self.port[1])
#         print('Sock send on port %s ...' % self.port[0])
#         self.__listeneur()
#
#
#     def __listeneur(self):
#         while True:
#             client_connection, client_address = self.socket_send.accept()
#             fcntl.fcntl(self.socket_send, fcntl.F_SETFL, os.O_NONBLOCK)
#             request = client_connection.recv(1024)
#             print(request)
#             f = open('/home/nfoissac/Bureau/dcn_alter/streaming-wav/streamapp/static/media/wav/treize.wav', 'rb')
#             # st = os.fstat(f.fileno())
#             # length = st.st_size
#
#             data = f.read(chunk)
#             client_connection.send(data)
#             while data:
#                 data = f.read(chunk)
#                 client_connection.send(data)
#             valid=False

    # def __listeneur(self):
    #     while True:
    #         try:
    #             msg = self.socket_recv.recv(4096)
    #         except sock.timeout as err:
    #             # this next if/else is a bit redundant, but illustrates how the
    #             # timeout exception is setup
    #             if err == 'timed out':
    #                 sleep(1)
    #                 print('recv timed out, retry later')
    #                 continue
    #             else:
    #                 print(err)
    #                 sys.exit(1)
    #         except sock.error as err:
    #             # Something else happened, handle error, exit, etc.
    #             print(err)
    #             sys.exit(1)
    #         else:
    #             if len(msg) == 0:
    #                 print('orderly shutdown on server end')
    #                 sys.exit(0)
    #             else:
    #                 pass

            # got a message do something :)





#a = STRMServer()


# print('Serving HTTP on port %s ...' % PORT)
# while True:
#     client_connection, client_address = listen_socket.accept()
#     request = client_connection.recv(1024)
#     print(request)
#     valid=False
#
#     if ( request.find(" HTTP/") == -1) : #// then this isn't valid HTTP
#         print(" NOT HTTP!\n")
#         break
#     else:
#         print(" HTTP request\n")
#         if request.startswith('HEAD '):
#             ptr = request[request.find("HEAD ")+len("HEAD "):] # start the buffer at the begining of the URL
#             print("HEAD request: {0}\n ".format(ptr))
#             client_connection.sendall("HEAD request:"+ptr+"\n")
#             valid=True
#
#         elif request.startswith('GET '):
#             print("GET request \n")
#             # PUT YOUR CODE HERE (1)
#
#         if ( valid == False ):
#             print("UNKNOWN REQUEST!!")
#             break
#         else: # valid request, with ptr pointing to the resource name
#             ptr = ptr[:ptr.find('HTTP/')-1] # terminate the buffer at the end of the URL
#             if (ptr[-1] == '/'):  # for resources ending with '/'
#                 ptr+="index.html"     # add 'index.html' to the end
#             resource= WEBROOT+ptr     # begin resource with web root path and join it with resource path
#             try:
#                 file = open(resource, "r")
#             except IOError as e:
#                 print("I/O error({0}): {1}".format(e.errno, e.strerror)) #file is not found
#                 break
#
#             print("200 OK \n Opening ressource: {0}\n ".format(resource)) # serve up the file
#             http_response = "HTTP/1.0 200 OK \nServer: Tiny webserver \n\n"
#             client_connection.sendall(http_response)
#             if request.startswith('GET '): #this is a GET request
#                 buffer = file.read() # read the file into memory
#                 # PUT YOUR CODE HERE (2) : test if buffer not empty and send it to socket
#
#             file.close()
#     client_connection.close()
#     ch = input("<S>tart again <F>inish ? ")
#     if ch.upper() =='F':
#         break
#
