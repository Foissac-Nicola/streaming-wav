#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket


class RTPClient:
    """
        This class is rtp client for rtp server
    """

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
        """
            This generic method for send comment to rtsp server
        :param message: command for server
        :param message_error: error for command
        :return: None
        """
        try:
            self.__contex.send(message.encode("Utf8"))
            print("[COMMEND][RTP]",message)
            print("[-][RTP][" + self.__address + ":" + str(self.__port) + "] Disconnected to server")
        except socket.error as error:
            print(message_error+" - Error:", error)


    def send_pause(self,path,token):
        """
            This method send pause command
        :param path: file
        :param token: uuid
        :return: None
        """
        self.__send_commend("PAUSE "+path+" RTP/1.0 200 "+token,"Pause music failed")

    def send_replay(self,path,token):
        """
            This method send replay command
        :param path: file
        :param token: uuid
        :return: None
        """
        self.__send_commend("REPLAY "+path+" RTP/1.0 200 "+token,"Play music failed")

    def send_play(self,path,token):
        """
            This method send play command
        :param path: file
        :param token: uuid
        :return: None
        """
        self.__send_commend("PLAY "+path+" RTP/1.0 200 "+token,"Play music failed")

    def send_quit(self,path,token):
        """
            This method send quit command
        :param path: file
        :param token: uuid
        :return: None
        """
        self.__send_commend("QUIT "+path+" RTP/1.0 200 "+token,"Play music failed")

