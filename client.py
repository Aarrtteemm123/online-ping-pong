import socket

HOST = 'localhost'
PORT = 65432

class Client:
    def __init__(self,host,port):
        self.host = host
        self.port = port

    def send(self,data):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(data)
            response = s.recv(1024)
        return response

client = Client(HOST,PORT)
res = client.send(b'Hello network!')
print(res)