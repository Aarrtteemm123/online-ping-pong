import socket
import threading
import time

HOST = 'localhost'
PORT = 65432

class Client:
    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.__response = None
        self.__socket = None

    @property
    def data(self):
        print(self.__response)
        return self.__response

    def connect(self):
        if self.__socket is not None:
            self.disconnect()
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.connect((self.host, self.port))

    def is_connected(self):
        return self.__socket is not None

    def send(self, data):
        if self.__socket is None:
            raise Exception('The client has no connection')
        else:
            try:
                self.__socket.sendall(data)
                self.__response = self.__socket.recv(1024)
                return self.__response
            except ConnectionResetError as e:
                print(e)
                self.disconnect()

    def disconnect(self):
        self.__socket.close()
        self.__socket = None

