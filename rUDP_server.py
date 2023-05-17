import socket
import time
from helper import *

# Global variables.
# server port
serverPort = 50001
# The ip address of the running device.
ip_addr = socket.gethostbyname(socket.gethostname())
# delimiter to be used between the header elements.
delimiter = "[]:[]"

# function to handle the client requests.
def handle_client(address, data, serverSocket):
    #Making the 3-way hand_shaking with the client
    rcvPKT = packet(delimiter)
    rcvPKT.demultiplexPacket(data)
    if rcvPKT.SYNbit == 1:
        pkt = packet(delimiter)
        pkt.SYNbit=1
        pkt.ACKbit=1
        msg = pkt.makePacket('')
        serverSocket.sendto(msg.encode('utf-8'), address)   
    else:
        print(f"Can't connect to {address}")
        return
    try:
        response, _ = serverSocket.recvfrom(2048)
        rcvPKT = packet(delimiter)
        rcvPKT.demultiplexPacket(response)
        if(rcvPKT.ACKbit!=1):
            return
        print(f"connection to client {address} initiated")
        print("--------------------------------------------------------------------------")
        data = rcvPKT.message
        if (data[0] == '1' or data[0] == 'G'):
            time.sleep(0.5)
            serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # flag for http request
        http = False
        #The client wants a packet transmission.
        if data[0] == '0' or data[0] == '1':
            #The client wants to send data to the server.
            if data[0] == '0': 
                rcv = True #The server will receive data from the client
            #The client asking for data from the server.
            else: 
                rcv = False #The server will send data to the client
            #getting the file name
            data = data.split(',')
            filename = data[1]
        #The client wants Http request
        else:
            req, filename, _, _ = decode_http(data)
            http = True
            if req == 'GET':
                rcv = False #The server will send data to the client
            else:
                rcv = True #The server will receive data from the client
        ack = (rcvPKT.sequenceNumber + rcvPKT.length)
        #The client asked for sending data or Post http request.
        if rcv:
            Receive_File(serverSocket, address,delimiter, filename, 0, loss_rate=0, corruption_rate=0, http=http, ACKnum=ack)
        #The client asked for receiving data or GET http request.
        else:
            Send_File(serverSocket, address, delimiter, filename, http,ackn=ack)


    except:
        print(f"Can't connect to {address}")


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (ip_addr, serverPort)
print(f'Connected to: {ip_addr} , port {serverPort}')
# Bind the ip address with the socket.
sock.bind(server_address)
while True:
    print("--------------------------------------------------------------------------")
    print('Waiting to receive message....')
    # wait for the connection and save the conn to send data if needed to the client and addr for the ip address of the client
    data, address = sock.recvfrom(2048)
    handle_client(address, data, sock)
    print("Client served.")
    print("--------------------------------------------------------------------------")