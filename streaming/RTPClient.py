#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import pyaudio
import time
import sys
import socket
from threading import Thread

# Format usage for pyaudio
FORMAT = pyaudio.paInt16


class RTPClient(Thread):
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
        self.is_run = False

    def run(self):
        try:
            self.contex.connect((self.address, self.port))
            print("[+][RTP][" + self.address + ":" + str(self.port) + "] Connected to server")
            self.is_run = True
            self.fist_play = False
            i = 0
            while self.is_run:

                recv = self.contex.recv(self.framerate * self.nchannels)
                if recv:
                    if recv.startswith(b"RTSP/1.0 200 OK"):
                        print("[CONTROL][RSTP][" + self.address + ":" + str(self.port) + "]")

                        if self.fist_play:
                            self.stream.stop_stream()
                            self.stream.close()
                        else:
                            self.fist_play = True

                        arg = str(recv, encoding='utf8', errors='ignore').split("\n")
                        self.sample_width = int(arg[3].split(' ')[1])
                        self.nchannels = int(arg[4].split(' ')[1])
                        self.framerate = int(arg[5].split(' ')[1])
                        self.stream = self.audio.open(format=FORMAT, channels=self.nchannels, rate=self.framerate,
                                                      input=False,
                                                      output=True, frames_per_buffer=self.framerate)
                    self.stream.write(recv, exception_on_underflow=False)

            print("[-][RTP][" + self.address + ":" + str(self.port) + "] Disconnected to server")
            self.contex.close()
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()

        except Exception as err:
            print("[-][RTP][" + self.address + ":" + str(self.port) + "] Disconnected to server")
            sys.exit(-1)


if __name__ == '__main__':

    address = '127.0.0.1'
    port = 7801
    if len(sys.argv) == 2:
        address = sys.argv[1]
        port = sys.argv[2]
        print(address,port)


try:
    thread = RTPClient(address,port)
    thread.start()
    while 1:
        time.sleep(0.1)
except KeyboardInterrupt:
    thread.stop()
    thread.join()
