import socket
import signal
import sys
from helper import *

# TCP server settings
TCP_HOST = socket.gethostbyname(socket.gethostname())
TCP_PORT = 8000

print(socket.gethostbyname(socket.gethostname()))

# UDP server settings
UDP_HOST = socket.gethostbyname(socket.gethostname())
UDP_PORT = 7000

# Delimiter
delimiter = "[]:[]"

# create a TCP socket object
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#tcp_socket.close()
# bind the socket object to a specified address and port
tcp_socket.bind((TCP_HOST, TCP_PORT))

# start listening for incoming connections
tcp_socket.listen()

print(f"Gateway listening on port {TCP_PORT}")

# create a UDP socket object
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# define a signal handler to close the socket before exit
def signal_handler(sig, frame):
    print('Closing server socket...')
    # close the sockets
    tcp_socket.close()
    udp_socket.close()
    sys.exit(0)

# register the signal handler for Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

while True:
    # wait for incoming connection
    client_socket, client_address = tcp_socket.accept()

    # receive the data from the client
    request_data = client_socket.recv(2048).decode()

    # print the request data
    print(f"Received request:\n{request_data}")

    # send the request data to the UDP server
    udp_socket.sendto(request_data.encode('utf-8'), (UDP_HOST, UDP_PORT))
    (req, filename) = decode_http(request_data)
    print(f'Request: {req}, Filename: {filename}')
    file = 'buffer.txt'
    if req == 'GET':
        # receive the response from the UDP server
        Receive_File(udp_socket, delimiter, file, 0, http=True)
        # Get response from file in Proxy
        f = open(file, "r")
        response_data = f.read()
        f.close()
    else:
        create_post(file, request_data)
        response_data = Send_POST(udp_socket, (UDP_HOST, UDP_PORT), delimiter, file, http=True)

    # print the response data
    print(f"Received response:\n{response_data}")

    # send the response data back to the client
    client_socket.sendall(response_data.encode())

    # close the client socket
    client_socket.close()

# close the sockets
tcp_socket.close()
udp_socket.close()