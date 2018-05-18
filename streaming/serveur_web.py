#-*- coding: utf-8 -*-

import socket, sys

HOST, PORT = '127.0.0.1', 7800
WEBROOT =  "./webroot" # the web server's root directory

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    listen_socket.bind((HOST, PORT))
except socket.error:
    print("Socket binding to given adress has failed.")
    sys.exit

listen_socket.listen(1)


print('Serving HTTP on port %s ...' % PORT)
while True:
    client_connection, client_address = listen_socket.accept()
    request = client_connection.recv(1024)
    print(request)
    valid=False

    if ( request.find(" HTTP/") == -1) : #// then this isn't valid HTTP
        print(" NOT HTTP!\n")
        break
    else:
        print(" HTTP request\n")
        if request.startswith('HEAD '):
            ptr = request[request.find("HEAD ")+len("HEAD "):] # start the buffer at the begining of the URL
            print("HEAD request: {0}\n ".format(ptr))
            client_connection.sendall("HEAD request:"+ptr+"\n")
            valid=True
          
        elif request.startswith('GET '):
            print("GET request \n")
            # PUT YOUR CODE HERE (1)

        if ( valid == False ):    
            print("UNKNOWN REQUEST!!")
            break
        else: # valid request, with ptr pointing to the resource name
            ptr = ptr[:ptr.find('HTTP/')-1] # terminate the buffer at the end of the URL
            if (ptr[-1] == '/'):  # for resources ending with '/'
                ptr+="index.html"     # add 'index.html' to the end
            resource= WEBROOT+ptr     # begin resource with web root path and join it with resource path
            try:
                file = open(resource, "r")
            except IOError as e:
                print("I/O error({0}): {1}".format(e.errno, e.strerror)) #file is not found
                break
            
            print("200 OK \n Opening ressource: {0}\n ".format(resource)) # serve up the file
            http_response = "HTTP/1.0 200 OK \nServer: Tiny webserver \n\n"
            client_connection.sendall(http_response)
            if request.startswith('GET '): #this is a GET request
                buffer = file.read() # read the file into memory
                # PUT YOUR CODE HERE (2) : test if buffer not empty and send it to socket
            
            file.close()            
    client_connection.close()
    ch = input("<S>tart again <F>inish ? ")
    if ch.upper() =='F':
        break
        
