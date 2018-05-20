#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import queue
import sys
import wave
import pyaudio
import base64
import time
from threading import Thread , Lock , Semaphore
from time import sleep


IP_SERVER = "127.0.0.1"
VIDEO_SERVER_PORT = 7800
OUT_SERVER_PORT = 7801
MAX_NUM_CONNECTIONS_LISTENER = 20

test = queue.Queue()

class ThreadSafeDict:

    def __init__(self) -> None:
        self.__dictionairy = { }
        self.__lock = Semaphore()


    def set(self,key,value):
        self.__lock.acquire()
        self.__dictionairy[key]=value
        #print(self.__dictionairy)
        self.__lock.release()

    def get (self, key):
        self.__lock.acquire()
        value = {}
        if key in self.__dictionairy:
            value = self.__dictionairy[key]
        self.__lock.release()
        return value

    def try_bind(self,port):
        self.__lock.acquire()
        ret = False
        uuid = 0
        for key, value in self.__dictionairy.items():
            if value['bind'] == 0 :
                self.__dictionairy[key]['bind'] = port
                ret=True
                uuid= key
        self.__lock.release()
        return ret,str(uuid)

    def update_chunk(self,key):
        self.__lock.acquire()
        if key in self.__dictionairy:
            self.__dictionairy[key]['chunk'] = self.__dictionairy[key]['chunk'] + 1
        self.__lock.release()

    def update_status(self, key):
            self.__lock.acquire()
            if key in self.__dictionairy:
                self.__dictionairy[key]['new_status'] = 0
            self.__lock.release()

    def exist_key(self, key):
        self.__lock.acquire()
        ret = key in self.__dictionairy
        self.__lock.release()
        return ret



liste = ThreadSafeDict()


class RTPPoolServer(Thread):

    def __init__(self, address, port, contex):
        Thread.__init__(self)
        self.address = address
        self.port = port
        self.contex = contex
        self.contex_state = True
        print( "[+][RTP]["+self.address + ":" + str(self.port)+"] Connected")

    def run(self):
        try:
            while self.contex_state:
                data = self.contex.recv(1024)
                if (data.find(b" RTP/1.0") == -1):
                    print("[-][RTP][" + self.address + ":" + str(self.port) + "] Disconnected")
                    self.contex_state = False
                    self.contex.close()
                    break

                if data.startswith(b'PLAY'):
                    split= str(data).split(' ')
                    uuid = split[4]
                    link = split[1]
                    commend= split[0]
                    print("["+commend[2:]+"][RTP][" + self.address + ":" + str(self.port) + "] " +link+":"+ uuid)
                    if not liste.exist_key(uuid):
                        liste.set(uuid,{'cmd':commend,'link':link , 'bind':0 , 'chunk':0 , 'new_status':0 })
                    else:
                        current=liste.get(uuid)
                        if current :
                            if current['link'] != link:
                                liste.set(uuid,{'cmd':commend,'link':link , 'bind':0 , 'chunk':0 , 'new_status':1 })
                                print(liste.get(uuid))


        except Exception as err:
            print(err)
            self.contex.close()



class RTSPPoolServer(Thread):
    def __init__(self, ip, port, conn):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.conn = conn
        self.bind = False
        self.uuid = 0
        self.file_open = False
        self.file = None
        self.sampwidth = 0
        self.nchannels = 0
        self.framerate = 0
        print("[+][RTSP][" + self.ip + ":" + str(self.port) + "] Connected")

    def __send_rstp_describe(self,path):
        ret = self.__get_wave_info(path=path)
        data = '''RTSP/1.0 200 OK\nServer: RSTP\nCseq: 2\nSample-width: '''+str(self.sampwidth)+'''\nChannels: '''+str(self.nchannels)+'''\nFramerate: '''+str(self.framerate)+'''\n\n'''
        self.conn.sendall(bytes(data,'utf8'))

    def __get_wave_info(self,path):
        file = wave.open(path,'rb')
        self.sampwidth = file.getsampwidth()
        self.nchannels = file.getnchannels()
        self.framerate = file.getframerate()
        file.close()


    def run(self):
        try:
            while True:
                time.sleep(0.5)
                if not self.bind:
                    print('bind',self.port)
                    self.bind , self.uuid = liste.try_bind(self.port)
                else:
                    #l = liste.get(str(self.uuid))
                    # print(l)

                    if not self.file_open:
                        self.file = open(liste.get(self.uuid)['link'],'rb')
                        self.file_open = True
                        self.__send_rstp_describe(liste.get(self.uuid)['link'])

                    else :
                        if liste.get(self.uuid)['new_status'] != 0:
                            print("ok")
                            self.file.close()
                            self.file = open(liste.get(str(self.uuid))['link'], 'rb')
                            self.__send_rstp_describe(liste.get(self.uuid)['link'])
                            liste.update_status(self.uuid)

                        else:
                            data = self.file.read(self.framerate*self.nchannels)
                            self.conn.send(data)
                            liste.update_chunk(self.uuid)
        except Exception as e:
            print(e)
            print("[+][RTSP][" + self.ip + ":" + str(self.port) + "] Disconnected")
            self.conn.close()

    def send_options_responce(self):
        self.conn.send(b"RTSP/1.0 200 OK")



def receiv(s) :
    run = True
    while run :
        try:
            data = s.recv(1024)
            print(data)
            if (data.find(b" RTSP/1.0") == -1):
                break
            if data.startswith(b'OPTIONS'):
                link = str(data)
                test.put({'command':1 , 'link':link.split(' ')[1] ,'seq':data[data.find(b"CSeq:"):]})
        except Exception as err:
            print(err)
            run = False


def rtp_server(adress,port):
    try:
        print('Start RTP Server')
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        connection.bind((adress, port))
        connection.listen(MAX_NUM_CONNECTIONS_LISTENER)
        while True:
            (conn, (ip, port)) = connection.accept()
            thread = RTPPoolServer(ip, port, conn)
            thread.start()
    except(KeyboardInterrupt, SystemExit) as err:
        print(err)


def tcp_video_thread():
    try:
        print('Start RTSP Server')
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        connection.bind((IP_SERVER, OUT_SERVER_PORT))
        connection.listen(MAX_NUM_CONNECTIONS_LISTENER)
        while True:
            (conn, (ip, port)) = connection.accept()
            thread = RTSPPoolServer(ip, port, conn)
            thread.start()
            #Thread(target=receiv(conn)).start()
    except(KeyboardInterrupt, SystemExit) as err:
        print(err)


try:
    print( "Starting...")
    thread_video = Thread(target=rtp_server , args=("127.0.0.1",7800))
    thread_video2 = Thread(target=tcp_video_thread)

    thread_video2.start()
    thread_video.start()


except (KeyboardInterrupt, SystemExit) as err :
    print(err)
    sys.exit(-1)

# RTPPoolServer()