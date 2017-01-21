'''
Created on Jan 21, 2017

@author: sonu
'''
import socket


class Classifier():

    def classify(self, message):
        self.server_address = '/tmp/daemon-nbm.sock'
        # Create a UDS socket to our classifier server
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            sock.connect(self.server_address)
        except socket.error, msg:
            return None
        try:
            sock.sendall(message)
            data = sock.recv(1024)
        finally:
            sock.close()
        return data
