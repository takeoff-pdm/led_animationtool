# Communicate over UDP to Mik's Music Detection Sys
from socket import socket, AF_INET, SOCK_DGRAM

class UDP:
    def __init__(self, ip, port): # ip and port useless
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.bind(("", 33333))
        self.data_received = False
        self.latest_data = None

    def receive(self, stop, set_data):
        while not stop():
            data = self.sock.recv(512)

            if data:
                set_data(data)

    def close(self):
        self.sock.close()
