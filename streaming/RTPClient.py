
import socket


class RTPClient:

    def __init__(self,address,port) -> None:
        self.__port = port
        self.__address = address
        self.__contex = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.__contex.connect((self.__address, self.__port))
            print("[+][RTP][" + self.__address + ":" + str(self.__port) + "] Connected to server")
        except socket.error:
            print("[x][RTP][" + self.__address + ":" + str(self.__port) + "] Connection Failed to server")


    def __send_commend(self,message,message_error):
        try:
            self.__contex.send(message.encode("Utf8"))
            print("[COMMEND][RTP]",message)
            print("[-][RTP][" + self.__address + ":" + str(self.__port) + "] Disconnected to server")
        except socket.error as error:
            print(message_error+" - Error:", error)


    def send_pause(self,path,token):
        self.__send_commend("PAUSE "+path+" RTP/1.0 200 "+token,"Pause music failed")

    def send_play(self,path,token):
        self.__send_commend("PLAY "+path+" RTP/1.0 200 "+token,"Play music failed")

