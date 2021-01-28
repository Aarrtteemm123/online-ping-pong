import socket
import sys
import time

HOST = 'localhost'
PORT = 65432

class Client:
    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.__socket = None

    def connect(self):
        if self.__socket is not None:
            self.close()
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.connect((self.host, self.port))

    def send(self, data):
        if self.__socket is None:
            raise Exception('The client has no connection')
        else:
            try:
                self.__socket.sendall(data)
                response = self.__socket.recv(1024)
                return response
            except ConnectionResetError as e:
                print(e)
                self.close()

    def close(self):
        self.__socket.close()