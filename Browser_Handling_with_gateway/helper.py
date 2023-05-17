import socket
import hashlib
from Packet import packet
import platform
import os


def Receive_File(socket, delimiter, file, check, http=False):
    f = open(file, 'w')
    try:
        connection_count = 0  # trails
        ACKnum = 0
        while True:
            print('Waiting for the server response.....')
            try:
                # getting the server response and the server address.
                data, server = socket.recvfrom(2048)
                connection_count = 0
            # if the conncection failed, try to connect again.
            except:
                connection_count += 1
                if connection_count < 4:
                    print("Connection time out, retrying again..")
                    continue
                else:
                    print("Maximum connection trials reached, please choose another request")
                    break
            rcvPKT = packet(delimiter)
            rcvPKT.demultiplexPacket(data)
            print(f"Acknolwedgement number : {ACKnum}")
            print(f"Sequence number received: {rcvPKT.sequenceNumber}")
            print(f"Message Length: {rcvPKT.length}")
            # comparing the server and the clients checksums, seqnumbers and packet length
            if rcvPKT.checksum == rcvPKT.checksum_check and ACKnum == rcvPKT.sequenceNumber:
                # couldn't find the file
                if rcvPKT.message == "ERROR 404!!! FILE NOT FOUND!!":
                    print("Requested file could not be found on the server, please choose another file")
                else:  # file found, starting writing the data
                    f.write(rcvPKT.message)
                ACKnum = rcvPKT.sequenceNumber + rcvPKT.length
                pkt = packet(delimiter)
                pkt.ACKbit = 1
                pkt.ACKnum = ACKnum
                msg = ''
                if rcvPKT.FINbit == 1:
                    pkt.FINbit = 1
                    f.close()
                    if http:
                        msg = serve_post(file)

                msg = pkt.makePacket(msg)
                # sending ack to the server..
                sent = socket.sendto(msg.encode('utf-8'), server)
                if rcvPKT.FINbit == 1:
                    break
            else:  # packets are not matching
                print("Checksum mismatch detected or dropping packet")
                continue

    finally:
        if (check == 1):
            print("Closing the socket.")
            socket.close()
        f.close()


def Send_File(serverSocket, address, delimiter, filename, http=False):
    packet_count = 0
    pkt = packet(delimiter)  # initialize the packet
    if http:
        data = serve_get(filename)
    else:
        try:
            print(f"Opening the file: {filename}")
            # open the file the client requested
            file = open(filename, 'r')
            data = file.read()  # read the file
            file.close()
        except:  # if the file the client requested couldn't be found
            message = "ERROR 404!!! FILE NOT FOUND!!"
            # making the packet.
            lastPacket = pkt.makePacket(message)
            # preparing the response of the server to be sent to the client
            serverSocket.sendto(lastPacket.encode('utf-8'), address)
            print("Requested file could not be found...")
            return
    ack_count = 0
    while True:
        packet_count += 1
        # getting 500 bytes out of the data each time.
        message = data[0:500]
        if len(data) < 501:
            pkt.FINbit = 1
        lastPacket = pkt.makePacket(message)
        print(f"Sequence Number: {pkt.sequenceNumber}")
        data = data[500:]
        sent = serverSocket.sendto(lastPacket.encode('utf-8'), address)
        print(f'Sent: {sent} bytes to {address}, and now awaiting for acknowledgment')
        # setting the time out.
        serverSocket.settimeout(2)
        try:
            # recieving the acknowledgment from the client.
            response, _ = serverSocket.recvfrom(2048)
            rcvPKT = packet(delimiter)
            rcvPKT.demultiplexPacket(response)
            seqnum = int(pkt.sequenceNumber) + int(pkt.length)
            print(f"expected acknowledgement number : {seqnum}")
            print(f"recived acknowledgement number : {rcvPKT.ACKnum}")
            print(f"recived Message: {rcvPKT.message}")
            if seqnum == rcvPKT.ACKnum and rcvPKT.checksum == rcvPKT.checksum_check:
                pkt.sequenceNumber = seqnum
                ack_count = 0
                print("Acknowledgment received succesfully")
            if rcvPKT.FINbit == 1:
                print(f"Packets served: {packet_count} ")
                break
        except:
            print(f"Time out reached, resending the last packet: {packet_count - 1} again.")
            ack_count += 1
            packet_count -= 1
            if ack_count >= 5:
                print("Connection lost because of no response")
                break
            continue

def make_http(http_req, Requested_File, host, port):
    device_description = platform.platform()
    http_header = f'{http_req} /{Requested_File} HTTP/1.1\nHost: {host}:{port}\nConnection: keep-alive\nsec-ch-ua: "Chromium";v="112", "Microsoft Edge";v="112", "Not:A-Brand";v="99"\nsec-ch-ua-mobile: ?0\nUser-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.58\n\sec-ch-ua-platform: "{device_description}"\nAccept: image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8\nSec-Fetch-Site: same-origin\nSec-Fetch-Mode: no-cors\nSec-Fetch-Dest: image\nReferer: http://127.0.0.1:8000/{Requested_File}\nAccept-Encoding: gzip, deflate, br\nAccept-Language: en-GB,en;q=0.9,en-US;q=0.8\n'
    return http_header


def decode_http(http_header):
    arr = http_header.splitlines()
    req = arr[0].split()
    req[1] = req[1][1:]
    return req[0], req[1]


def serve(fn):
    # open gateway buffer
    f = open(fn, "r")
    response = f.read()
    f.close()
    return response


def serve_get(fn):
    if len(fn) == 0:
        fn = 'index.html'

    if os.path.exists(fn):
        # open index.html
        f = open(fn, "r")
        html = f.read()
        f.close()
        response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(html)}\r\n\r\n{html}"
    else:
        response = 'HTTP/1.1 400 Bad Request\r\nContent-Type:\
		 text/html\r\n\r\n<html><body><h1>400 Bad Request</h1><p>The requested \
		 resource could not uploaded on the server.</p></body></html>'
    return response


def serve_post(fn):
    if os.path.exists(fn):
        f = open(fn, "r")
        html = f.read()
        f.close()
        response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(html)}"
    else:
        response = 'HTTP/1.1 400 Bad Request\r\nContent-Type:\
    		 text/html\r\n\r\n<html><body><h1>400 Bad Request</h1><p>The requested \
    		 resource cannot be added on the server.</p></body></html>'
    return response
