import socket

def StartClient(ip):
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_address=(ip,20000)
    print('Connect to server')
    sock.connect(server_address)

    try:
        message="START\r\n'"
        sock.send(message.encode('UTF-8'))
        print('Done')
    finally:
        sock.close()


ip_list=["172.31.0.106","172.31.0.163","172.31.0.168","172.31.0.170","172.31.0.171","172.31.0.172","172.31.0.173","172.31.0.174","172.31.0.5","172.31.0.169"]
for ip in ip_list:
    print("Connecting to "+ip)
    StartClient(ip)
