import socket
from helper import *

serverPort = 50001
ip_addr = socket.gethostbyname(socket.gethostname())
delimiter = "[]:[]"
loss_rate = 0
corruption_rate = 0

#taking the loss rate of packets as input
while True:
    print("Enter a value between 0 and 1 for loss rate:  ")
    try:
        loss_rate = float(input())
        if loss_rate > 1 or loss_rate < 0:
            print("Range is between 0 and 1!!!!")
            continue
    except:
        print("enter a valid number")
    break
# taking corruption of packets as input
while True:
    print("Enter a value between 0 and 1 for corruption rate:  ")
    try:
        corruption_rate = float(input())
        if corruption_rate > 1 or corruption_rate < 0:
            print("Range is between 0 and 1!!!!")
            continue
    except:
        print("enter a valid number")
    break

while True:
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # setting the time out
    clientSocket.settimeout(5)
    server_address = (ip_addr, serverPort)
    #Initiate the 3-way hand shaking with the server
    pkt = packet(delimiter)
    pkt.SYNbit=1 #at the start of the connection.
    #making a packet with a null data to make the connection.
    msg = pkt.makePacket('')
    clientSocket.sendto(msg.encode('utf-8'), server_address)
    try:
        response, _ = clientSocket.recvfrom(200)
        rcvPKT = packet(delimiter)
        rcvPKT.demultiplexPacket(response)
        if rcvPKT.SYNbit == 1 and rcvPKT.ACKbit == 1:
            pkt = packet(delimiter)
            pkt.ACKbit=1
    except: #couldn't connect to the server.
        print(f"Can't connect to server {server_address}")
    # asking the user to choose between a http request or random packet.
    while True:
        try:
            print("--------------------------------------------------------------------------")
            print("1- Send Http request")
            print("2- Choose a file")
            choice = int(input("Your Choice: "))
        except ValueError: #checking if the client enterd a wrong value
            print("Please enter a valid integer 1-2")
            continue
        if choice != 1 and choice != 2:
            print('Wrong choice! enter a value between: 1-2')
            continue
        break
    # client choosed http request.
    if (choice == 1):
        while True:
            Http_request = input("Please, Enter the request (GET/POST): ")
            #validate the http request.
            if Http_request != 'GET' and Http_request !='POST':
                print('Wrong answer, you need to enter GET or POST')
                continue
            break
        while True:
            file = input("Please, enter the requested file name: ")
            #validate the file input
            if len(file) < 1:
                print("You must enter a value !")
                continue
            break
        print("--------------------------------------------------------------------------")
        # concatinating the client message to send it to the server.
        message = make_http(Http_request, file, ip_addr, serverPort)
        # if GET request 1 else 0
        if (Http_request == 'GET'):
            request = 1  # Means that the server should send the file to the client
        else:
            request = 0  # Means that the client will send the file to the server.
    # client choosed a file.
    else:
        while True:
            try:
                # Checking if client wants to send or receive
                request = int(input('1- Send \n2- Recieve \nChoice: ')) - 1
            except ValueError:
                print("Please enter a valid integer 1-2")
                continue
            if request != 0 and request != 1:
                print('Wrong choice! enter a value between: 1-2')
                continue
            break
        while True:
            # taking the file name as input from the client
            file = input("Please, enter the file name: ")
            #validate the file input
            if len(file) < 1:
                print("You must enter a value !")
                continue
            break
        print("--------------------------------------------------------------------------")
        message = str(request) + ',' + file

    # sending the desired file to the server.
    msg = pkt.makePacket(message)
    clientSocket.sendto(msg.encode('utf-8'), server_address)
    seq = (int(pkt.sequenceNumber) + int(pkt.length))
    # The client choosed to recieve a file from the server or it's a GET http request.
    if (request):
        Receive_File(clientSocket, server_address, delimiter, file, check=1, loss_rate=loss_rate, corruption_rate=corruption_rate,seqn=seq)
    # The client choosed to send file to the server or it's a POST http request.
    else:
        Send_File(clientSocket, server_address, delimiter, file,seqn=seq)
