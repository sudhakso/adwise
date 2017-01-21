import socket
import sys

# Create a UDS socket
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = '/tmp/daemon-nbm.sock'
print >>sys.stderr, 'connecting to classifier %s' % server_address

message = sys.argv[1]
try:
    sock.connect(server_address)
except socket.error, msg:
    print >>sys.stderr, msg
    sys.exit(1)
try:
    sock.sendall(message)
    amount_received = 0
    data = sock.recv(1024)
    amount_received = len(data)
    print >>sys.stderr, 'received: "%s"' % data
finally:
    sock.close()
