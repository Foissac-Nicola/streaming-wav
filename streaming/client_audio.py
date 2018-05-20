"""PyAudio Example: Play a wave file (callback version)."""

import pyaudio
import wave
import time
import sys
import socket
import queue
from threading import Thread

# if len(sys.argv) < 2:
#     print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
#     sys.exit(-1)

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100


class RTPClient(Thread):


    def __init__(self,address,port):
        Thread.__init__(self)
        self.port = port
        self.address = address
        self.contex = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_run = False
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=False, output=True, frames_per_buffer=CHUNK )

    def run(self):
        try:
            self.contex.connect((self.address, self.port))
            print("[+][RTP]["+self.address + ":" + str(self.port)+"] Connected to server")
            self.is_run = True
            i = 0
            while self.is_run :

                recv = self.contex.recv(44100*2)
                if recv :
                    if recv.startswith(b"RTSP/1.0 200 OK"):
                        print(recv)
                    self.stream.write(recv,exception_on_underflow=False)
                # else:
                #     print("[-][RTP][" + self.address + ":" + str(self.port) + "] Disconnected to server")
                #     self.is_run = False
                #     #self.audio.close()
                #     self.audio.terminate()
        except socket.error as err:
            #     print("[-][RTP][" + self.address + ":" + str(self.port) + "] Disconnected to server")
            #     self.is_run = False
            #     #self.audio.close()
            #     self.audio.terminate()
            print(err, HOST, PORT)
            sys.exit()




HOST = '127.0.0.1'
PORT = 7801

thread = RTPClient(HOST,PORT)
thread.start()

thread.join()


#
# d = queue.Queue()
#
#
#
# def parse_rtsp_describe(message, stream):
#     # stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)
#     print(str(msgServeur, encoding='utf8', errors='ignore').split("\n"))
#     # .split('\\n'))
#
#
#
#
# # wf = wave.open(sys.argv[1], 'rb')
# #
# # # instantiate PyAudio (1)
# # p = pyaudio.PyAudio()
# #
# # # define callback (2)
#
# mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# # 2) try to connect to the server:
# try:
#     a = mySocket.connect((HOST, PORT))
#     print(a)
#
# except socket.error as err:
#     print(err, HOST, PORT)
#     sys.exit()
# print("Connected to the server.")
#
#
# def callback(in_data, frame_count, time_info, status):
#     in_data= mySocket.recv(1025)
#     if len(in_data) < frame_count:
#         print('error')
#         print(len(in_data))
#         print(frame_count)
#         return (in_data, pyaudio.paComplete)
#     print(len(in_data))
#     return (in_data, pyaudio.paContinue)
#
#
# audio = pyaudio.PyAudio()
#
#
# stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=False, output=True, frames_per_buffer=CHUNK,
#                     stream_callback=callback)
# # # open stream using callback (3)
# # stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
# #                 channels=wf.getnchannels(),
# #                 rate=wf.getframerate(),
# #                 output=True,
# #                 stream_callback=callback)
#
#
# # while 1:
# #
# #         data = mySocket.recv(1024)
# #         if len(data) > 0 :
# #             d.put(data)
# # print(len(data))
# # if msgServeur.find(b"RTSP/1.0") == -1:
# #     stream.write(msgServeur)
# # else:
# #     print(msgServeur)
# #     stream.write(msgServeur)
# # print(msgServeur)
#
#
#
#
#
#
#
#
#
# stream.start_stream()
#
# # wait for stream to finish (5)
# while stream.is_active():
#     time.sleep(5)
#
# # stop stream (6)
# stream.stop_stream()
# stream.close()
#
#
# # close PyAudio (7)
