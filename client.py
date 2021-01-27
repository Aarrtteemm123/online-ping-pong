import socket
import time

HOST = 'localhost'
PORT = 65432

class Client:
    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.__socket = None
        self.__close_msg = b'closing connection'

    def connect(self):
        if self.__socket is not None:
            self.close()
        else:
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__socket.connect((self.host, self.port))

    def send(self, data):
        if data == self.__close_msg:
            raise Exception('It\'s reserved message')
        elif self.__socket is None:
            raise Exception('The client has no connection')
        else:
            self.__socket.sendall(data)
            response = self.__socket.recv(1024)
            return response

    def close(self):
        self.__socket.sendall(self.__close_msg)
        self.__socket.close()


if __name__ == '__main__':
    for i in range(1):
        print(i)
        client = Client(HOST,PORT)
        print(client.send(b'Hello network'+bytes(str(i),'utf-8')))