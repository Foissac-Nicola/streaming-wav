#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import sys
import wave
import time
from threading import Thread, Semaphore
from time import sleep


class ThreadSafeDict:
    """
        This class define thread safe dict.
        This use semaphore to lock memory access.
    """
    def __init__(self) -> None:
        self.__dictionairy = {}
        self.__lock = Semaphore()

    def set(self, key, value):
        """
            This method set new value in the dict.
        :param key: uuid
        :param value: dict {'cmd': X, 'link': X, 'bind': X, 'chunk': X, 'status': X, "state": X})
        :return: None
        """
        self.__lock.acquire()
        self.__dictionairy[key] = value
        self.__lock.release()

    def get(self, key):
        """
            This method get value in dict
        :param key: uuid
        :return: value of uuid key.
        """
        self.__lock.acquire()
        value = {}
        if key in self.__dictionairy:
            value = self.__dictionairy[key]
        self.__lock.release()
        return value

    def try_bind(self, port):
        """
            This method try to bind somme client whit server.
        :param port: socket connection port
        :return: ret: true if bind otherwise false , uuid
        """
        self.__lock.acquire()
        ret = False
        uuid = 0
        for key, value in self.__dictionairy.items():
            if value['bind'] == 0:
                self.__dictionairy[key]['bind'] = port
                ret = True
                uuid = key
        self.__lock.release()
        return ret, str(uuid)

    def update_chunk(self, key):
        """
            This method update chunk one by one of client
        :param key: uuid
        :return: None
        """
        self.__lock.acquire()
        if key in self.__dictionairy:
            self.__dictionairy[key]['chunk'] = self.__dictionairy[key]['chunk'] + 1
        self.__lock.release()

    def update_status(self, key, value):
        """
            This method update status of client
        :param key: uuid
        :param value: new status
        :return: None
        """
        self.__lock.acquire()
        if key in self.__dictionairy:
            self.__dictionairy[key]['status'] = value
        self.__lock.release()

    def exist_key(self, key):
        """
            This method check if key exist
        :param key: uuid
        :return: false if no exist otherwise true
        """
        self.__lock.acquire()
        ret = key in self.__dictionairy
        self.__lock.release()
        return ret


liste = ThreadSafeDict()


class RTPPoolServer(Thread):
    """
        This class provide threaded interface for socket connection.
        This class parse all frame and check is rtp friendly.
    """
    def __init__(self, address, port, contex):
        Thread.__init__(self)
        self.address = address
        self.port = port
        self.contex = contex
        self.contex_state = True
        print("[+][RTP][" + self.address + ":" + str(self.port) + "] Connected")

    def run(self):
        try:
            while self.contex_state:
                data = self.contex.recv(1024)
                # check is rtp protocol
                if (data.find(b" RTP/1.0") == -1):
                    print("[-][RTP][" + self.address + ":" + str(self.port) + "] Disconnected")
                    self.contex_state = False
                    self.contex.close()
                    break
                # check is rtp play
                if data.startswith(b'PLAY'):
                    split = str(data).split(' ')
                    uuid = split[4]
                    link = split[1]
                    commend = split[0]
                    # is first command play
                    if not liste.exist_key(uuid):
                        liste.set(uuid,
                                  {'cmd': commend, 'link': link, 'bind': 0, 'chunk': 0, 'status': -1, "state": False})
                    else:
                        current = liste.get(uuid)
                        if current:
                            # is change music
                            if current['link'] != link and current['status'] == 0:
                                liste.set(uuid, {'cmd': commend, 'link': link, 'bind': 0, 'chunk': 0, 'status': 1,
                                                 "state": False})
                            # is un pause
                            if current['status'] == 0 and current['link'] == link and current['state'] == True:
                                liste.set(uuid, {'cmd': commend, 'link': link, 'bind': 0, 'chunk': 0, 'status': 3,
                                                 "state": False})
                # check is trp replay
                if data.startswith(b'REPLAY'):
                    split = str(data).split(' ')
                    uuid = split[4]
                    link = split[1]
                    commend = split[0]
                    current = liste.get(uuid)
                    if current:
                        # is replay
                        if current['link'] == link:
                            liste.set(uuid, {'cmd': commend, 'link': link, 'bind': 0, 'chunk': 0, 'status': 2,
                                         "state": False})
                # check is rtp pause
                if data.startswith(b'PAUSE'):
                    split = str(data).split(' ')
                    uuid = split[4]
                    link = split[1]
                    commend = split[0]
                    current = liste.get(uuid)
                    if current:
                        # is pause
                        if current['link'] == link:
                            liste.set(uuid,
                                      {'cmd': commend, 'link': link, 'bind': 0, 'chunk': 0, 'status': 5, "state": True})
        except Exception as err:
            print(err)
            self.contex.close()


class RTSPPoolServer(Thread):
    """
        This class provide threaded interface for socket connection.
        This class send data to rtsp client.
    """
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
        self.is_run = False
        self.is_pause = False
        print("[+][RTSP][" + self.ip + ":" + str(self.port) + "] Connected")

    def __send_rstp_describe(self, path):
        """
            This method send description of wave file.
        :param path: path of file.
        :return: None
        """
        ret = self.__get_wave_info(path=path)
        data = '''RTSP/1.0 200 OK\nServer: RSTP\nCseq: 2\nSample-width: ''' + str(
            self.sampwidth) + '''\nChannels: ''' + str(self.nchannels) + '''\nFramerate: ''' + str(
            self.framerate) + '''\n\n'''
        self.conn.sendall(bytes(data, 'utf8'))

    def __get_wave_info(self, path):
        """
            This method get some detail of wave file like sample width , number of channel and frame rate.
        :param path: path of file
        :return: None
        """
        file = wave.open(path, 'rb')
        self.sampwidth = file.getsampwidth()
        self.nchannels = file.getnchannels()
        self.framerate = file.getframerate()
        file.close()

    def run(self):
        try:
            self.is_run = True
            while self.is_run:
                time.sleep(0.5)
                # is bind
                if not self.bind:
                    self.bind, self.uuid = liste.try_bind(self.port)
                else:
                    # fist play
                    if not self.file_open:
                        self.file = open(liste.get(self.uuid)['link'], 'rb')
                        self.file_open = True
                        self.__send_rstp_describe(liste.get(self.uuid)['link'])
                        liste.update_status(self.uuid, 0)
                        print("[FIRST PLAY][RTSP][" + self.ip + ":" + str(self.port) + "] Receive")

                    else:
                        # change
                        if liste.get(self.uuid)['status'] == 1:
                            print("[CHANGE][RTSP][" + self.ip + ":" + str(self.port) + "] Receive")
                            self.file.close()
                            self.file = open(liste.get(str(self.uuid))['link'], 'rb')
                            self.__send_rstp_describe(liste.get(self.uuid)['link'])
                            liste.update_status(self.uuid, 0)
                            self.is_pause = False

                        # replay
                        if liste.get(self.uuid)['status'] == 2:
                            print("[REPLAY][RTSP][" + self.ip + ":" + str(self.port) + "] Receive")
                            self.file.close()
                            self.file = open(liste.get(str(self.uuid))['link'], 'rb')
                            self.__send_rstp_describe(liste.get(self.uuid)['link'])
                            liste.update_status(self.uuid, 0)
                            self.is_pause = False

                        # stop pause
                        if liste.get(self.uuid)['status'] == 3:
                            print("[PLAY][RTSP][" + self.ip + ":" + str(self.port) + "] Receive")
                            self.is_pause = False
                            liste.update_status(self.uuid, 0)

                        # start pause
                        if liste.get(self.uuid)['status'] == 5:
                            print("[PAUSE][RTSP][" + self.ip + ":" + str(self.port) + "] Receive")
                            self.is_pause = True
                            liste.update_status(self.uuid, 0)

                        else:
                            # if is pause
                            if self.is_pause:
                                pass
                            else:
                                # read of file and send to client
                                data = self.file.read(self.framerate * self.nchannels)
                                self.conn.send(data)
                                liste.update_chunk(self.uuid)
        except Exception as e:
            print("[+][RTSP][" + self.ip + ":" + str(self.port) + "] Disconnected")
            self.conn.close()


ip_server = "127.0.0.1"
rtp_server_port = 7800
rtsp_server_port = 7801
max_pool_server = 20


def rtp_server(address, port, pool):
    """
        This function start rtp server.
        For each connection we start threaded rtp server.
    :param address: address for rtp server
    :param port: port for rtp server
    :param pool: number of max of simultaneous connection
    :return: None
    """
    print('Start RTP Server [' + address + ':' + str(port) + ']')
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection.bind((address, port))
    connection.listen(pool)
    while True:
        (conn, (ip, port)) = connection.accept()
        thread = RTPPoolServer(ip, port, conn)
        thread.start()


def rtsp_server(address, port, pool):
    """
        This function start rtsp server.
        For each connection we start threaded rtsp server.
    :param address: address for rtp server
    :param port: port for rtp server
    :param pool: number of max of simultaneous connection
    :return: None
    """
    print('Start RTSP Server [' + address + ':' + str(port) + ']')
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection.bind((address, port))
    connection.listen(pool)
    while True:
        (conn, (ip, port)) = connection.accept()
        thread = RTSPPoolServer(ip, port, conn)
        thread.start()

if __name__ == '__main__':

    try:
        print("Starting...")
        # instantiate rtp and rtps pooling server.
        thread_rtp = Thread(target=rtp_server, args=(ip_server, rtp_server_port, max_pool_server))
        thread_rtsp = Thread(target=rtsp_server, args=(ip_server, rtsp_server_port, max_pool_server))

        # start rtp and rtps pooling server.
        thread_rtp.start()
        thread_rtsp.start()

        while 1:
            sleep(0.1)


    except (KeyboardInterrupt, SystemExit) as err:
        print(err)
        sys.exit(-1)
