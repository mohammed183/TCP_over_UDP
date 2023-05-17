import socket
import threading
import time
from helper import *
import signal
import sys
import os

# Global variables.
# server port
serverPort = 7000
# The ip address of the running device.
ip_addr = socket.gethostbyname(socket.gethostname())
# delimiter to be used between the header elements.
delimiter = "[]:[]"
packetLoss = False


# define a signal handler to close the socket before exit
def signal_handler(sig, frame):
    print('Closing server socket...')
    sock.close()
    sys.exit(0)


# register the signal handler for Ctrl+C
signal.signal(signal.SIGINT, signal_handler)


# function to handle the client requests.
def handle_client(address, data, serverSocket):
    # Decode Data
    data = data.decode()
    print(f'Received Data: {data}')
    if data[0] == 'G':
        time.sleep(0.5)
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # flag for http request
    http = True
    req, filename = decode_http(data)
    if req == 'GET':
        rcv = False
    else:
        rcv = True

    if rcv:
        Receive_File(serverSocket, delimiter, filename, 0, http)
    else:
        Send_File(serverSocket, address, delimiter, filename, http)


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (ip_addr, serverPort)
os.chdir('web')
print(f'Connected to: {ip_addr} , port {serverPort}')
# Bind the ip address with the socket.
sock.bind(server_address)
while True:
    print('Waiting to receive message')
    # wait for the connection and save the conn to send data if needed to the client and addr for the ip address of the client
    data, address = sock.recvfrom(2048)
    # Running multibe clients at a time..
    # connectionThread = threading.Thread(target=handle_client, args=(address, data))
    # connectionThread.start()
    handle_client(address, data, sock)
    print('Received %s bytes from %s' % (len(data), address))

