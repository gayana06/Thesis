
import socket

def StartClient(message):
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_address=('172.31.0.124',50000)
    print('Connect to server')
    sock.connect(server_address)

    try:
        message="5,178,20,0.00572598840772,0.0262176970641,79,12,?"
        #message="5,178,2222,0.00572598840772,0.0262176970641,169,2212,?"
        #sock.sendall(bytes(message, 'UTF-8'))
        sock.sendall(message)
	# Look for the response
        #amount_received = 0
        #amount_expected = len(message)

        #while amount_received < amount_expected:
            #data = sock.recv(100)
            #amount_received += len(data)
            #print('Received = '+str(data.decode('UTF-8')))
        data = sock.recv(100)
        newquorum=data.decode('UTF-8')
	print('New Quorum = '+newquorum)
        return newquorum
    finally:
        sock.close()

StartClient('5,178,20,0.00572598840772,0.0262176970641,79,12,?')
