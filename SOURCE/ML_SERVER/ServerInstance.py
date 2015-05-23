__author__ = 'Gayana'
import socket
import ctypes
from ctypes import *


def ServerStart():
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_address=('172.31.0.124',50000)
    sock.bind(server_address)
    print('Bind the socket to ')
    sock.listen(1)
    while True:
        print('Waiting for a connection')
        connection, client_address=sock.accept()
        try:
            print('Client connected ')
            while True:
                data=connection.recv(100)
                print('received "%s"' % data.decode('UTF-8'))
                if data:
                    newquorum=QueryML(data.decode('UTF-8'))
                    connection.sendall(newquorum)
                else:
                    print('no more data')
                    break
        finally:
            connection.close()

def QueryML(query):
    loaded=True
    print('query is '+query)
    libtest=ctypes.CDLL('/home/ubuntu/ML_SERVER/libsee5.so')
    libtest.initiateSee5withTrees('/home/ubuntu/ML_SERVER/oracle_twitter')
    print('Tree loaded '+query)
    #query="5,2178,2220,0.00572598840772,0.0262176970641,1179,2212,?"
    quorum=ctypes.c_char_p(libtest.getPrediction(query))
    print('New Quorum='+quorum)
    return quorum.value



ServerStart()




