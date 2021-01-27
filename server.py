import socket
import threading
import time

from client import Client

HOST = 'localhost'
PORT = 65432 # 65432

class Server:
    def __init__(self,host, port):
        self.host = host
        self.port = port
        self.__is_running = True
        self.__connection_addr_dict = {}

    def __run(self):
        print('starting server on ', (self.host,self.port))
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            while self.__is_running:
                connection, address = s.accept()
                print('accepted connection from ', address)
                self.__connection_addr_dict[address] = b''
                connection_thread = threading.Thread(target=self.__listen_new_connection, args=(connection, address))
                connection_thread.start()
        self.__connection_addr_dict.clear()
        print('server stopping... ', (self.host, self.port))

    def close_connection(self, addr):
        if addr in self.__connection_addr_dict:
            self.__connection_addr_dict.pop(addr)

    def start(self):
        server_tread = threading.Thread(target=self.__run)
        server_tread.start()

    def stop(self):
        self.__is_running = False
        Client(self.host,self.port).send(b'')

    def __listen_new_connection(self, connection, address):
        with connection:
            print('connected by', address)
            while address in self.__connection_addr_dict:
                data = connection.recv(1024)
                print(data)
                if not data:
                    continue
                connection.sendall(data)
        self.close_connection(address)
        print('closing connection to', address)

server = Server(HOST,PORT)
server.start()
