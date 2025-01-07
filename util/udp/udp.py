# Communicate over UDP to Mik's Music Detection Sys
from socket import socket

class UDP:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sock = socket()
        self.sock.connect((self.ip, self.port))
        self.data_received = False
        self.latest_data = None

    def receive(self, stop):
        while not stop():
            data = self.sock.recv(512)

            if data:
                self.data_received = True
                self.latest_data = data

    def close(self):
        self.sock.close()
