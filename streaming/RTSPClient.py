#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pyaudio
import time
import sys
import socket
from threading import Thread

# Format usage for pyaudio
FORMAT = pyaudio.paInt16


class RTSPClient(Thread):
    """
        This class provide py audio instance and socket via thread
    """
    def __init__(self, address, port):
        Thread.__init__(self)
        self.port = port
        self.address = address
        self.contex = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_run = False
        self.sampwidth = 0
        self.nchannels = 1
        self.framerate = 1024
        self.audio = pyaudio.PyAudio()

    def stop(self):
        """
            this method stop thread
        :return:
        """
        self.is_run = False

    def run(self):
        try:
            # try to connect
            self.contex.connect((self.address, self.port))
            print("[+][RTP][" + self.address + ":" + str(self.port) + "] Connected to server")
            self.is_run = True
            self.fist_play = False
            i = 0
            while self.is_run:
                # receive data from server
                recv = self.contex.recv(self.framerate * self.nchannels)
                if recv:
                    # if control
                    if recv.startswith(b"RTSP/1.0 200 OK"):
                        print("[CONTROL][RSTP][" + self.address + ":" + str(self.port) + "]")
                        # if have play sound
                        if self.fist_play:
                            # stop stream
                            self.stream.stop_stream()
                            # remove unused stream
                            self.stream.close()
                        else:
                            self.fist_play = True
                        # took arg of rtsp frame
                        arg = str(recv, encoding='utf8', errors='ignore').split("\n")
                        # get sample width
                        self.sample_width = int(arg[3].split(' ')[1])
                        # get number channel
                        self.nchannels = int(arg[4].split(' ')[1])
                        # get frames rate
                        self.framerate = int(arg[5].split(' ')[1])
                        # allocate new stream
                        self.stream = self.audio.open(format=FORMAT, channels=self.nchannels, rate=self.framerate,
                                                      input=False,
                                                      output=True, frames_per_buffer=self.framerate)
                    # write chunk to stream
                    self.stream.write(recv, exception_on_underflow=False)

            print("[-][RTP][" + self.address + ":" + str(self.port) + "] Disconnected to server")
            self.contex.close()
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()

        except Exception as err:
            print("[x][RTP][" + self.address + ":" + str(self.port) + "] Fail To Connect")
            self.audio.terminate()
            self.stop()


if __name__ == '__main__':

    address = '127.0.0.1'
    port = 7801
    if len(sys.argv) >= 3:
        address = sys.argv[1]
        port = sys.argv[2]
        print(address,port)


    try:
        # Start RTSPClient
        thread = RTSPClient(address,port)
        thread.start()
        while 1:
            time.sleep(0.1)

    except KeyboardInterrupt:
        thread.stop()
        thread.join()
