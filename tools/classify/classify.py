import sys
import os
import socket
import time
from daemon import Daemon
from nb_classifier import ClassifierController

DATA_DIR = '/home/ubuntu/expooh/repo/adwise-userprofile-mgr/tools/examples'


class NBClassifierDaemon(Daemon):

    def run(self):
        # Prepare the UNIX socket
        self.server_address = '/tmp/daemon-nbm.sock'
        # Make sure the socket does not already exist
        try:
            os.unlink(self.server_address)
        except OSError:
            if os.path.exists(self.server_address):
                print >>sys.stderr, 'Error: Cannot remove the file %s' % (
                                                    self.server_address)
                raise
        # Create a UDS socket
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.bind(self.server_address)
        # Get the controller
        cc = ClassifierController('%s/%s' % (DATA_DIR,
                                             'sampleTexts.csv'),
                                  '%s/%s' % (DATA_DIR,
                                             'nbpicke'),
                                  DATA_DIR)
        nb = cc.getNBClassifier()
        self.sock.listen(5)
        while True:
            connection, client_address = self.sock.accept()
            try:
                print >>sys.stderr, 'Info: Connection from', client_address
                # Receive the data in small chunks and retransmit it
                while True:
                    data = connection.recv(1024)
                    # Test the classifier
                    print >>sys.stderr, 'Info: Query = "%s"' % data
                    testTweet = data
                    classified_data = nb.classify(testTweet)
                    print >>sys.stderr, "Info: Classified = %s\n" % classified_data
                    if data:
                        connection.sendall(classified_data)
                    else:
                        break
            finally:
                # Clean up the connection
                connection.close()

if __name__ == "__main__":
        daemon = NBClassifierDaemon('/tmp/daemon-nbm.pid')
        if len(sys.argv) == 2:
                if 'start' == sys.argv[1]:
                    try:
                        daemon.start()
                    except Exception as e:
                        print >>sys.stderr, "Error: Exception = %s" % (e)
                        sys.exit(2)
                elif 'stop' == sys.argv[1]:
                        daemon.stop()
                elif 'restart' == sys.argv[1]:
                        daemon.restart()
                elif 'status' == sys.argv[1]:
                        daemon.status()
                else:
                        print "Unknown command"
                        sys.exit(2)
                sys.exit(0)
        else:
                print "usage: %s start|stop|restart|status" % sys.argv[0]
                sys.exit(2)
