**Assumptions:** 

Reliable UDP using Python Socket Programming: 

UDP on its own is unreliable as none of the datagrams sent back and forth between the server and client are acknowledged. This makes it difficult for the sender to verify whether the recipient has received the packet or not. Therefore, by taking inspiration from TCP, we decided to improve the reliability of UDP in the following ways: 

Sequencing of packets: The client sends the packet number along with the packet itself; this allows the server to recognise un-ordered or missing packets. 

Stop-and-wait: After sending all the packets in a given window, the client waits for the server's acknowledgment before sending the remaining packets. The server. 

Retransmission of lost packets (selective-repeat): The server requests the client to re- transmit one or more missing packets. 

Retransmission of lost ACK packets 

Client authentication "3-way hand shaking": The client must first establish a connection with the server before it is able to send files. 

Bonus: 

In the bonus part we need to use a proxy server or gateway to connect the TCP based browser to the our TCP over UDP server. There are two established connections that can be shown later in the wire shark snapshot, one on port 7000 (UDP) and the other on port 8000 (TCP). The browser is connected with gateway and the gateway is then connected to the TCP over UDP server. Each request by the browser is sent to the gateway and the gateway sends it as TCP over UDP packets to the server. The server sends response to gateway in packets and the gateway buffers the data until complete then sends response to server. 

**Files:** 

**Packet.py:**

The Packet.py file contains the packet class which is used to create and parse packets for use in a reliable UDP protocol implementation. The packet class has attributes such as sequenceNumber, ACKbit, SYNbit, FINbit, length, and data which are used to encode and decode packets. The class also contains methods to create packets from input data, and to parse received packets into their respective attributes. 

**helper.py:**

The helper.py file contains several functions that are used by both the rUDP\_server.py and rUDP\_client.py files to perform various tasks. The functions include make\_http which takes HTTP request parameters and returns a formatted HTTP request message, checksum which is used to calculate the checksum for a given data string, and the most 2 important functions are send and receive files. 

**rUDP\_server.py:**

The rUDP\_server.py file contains the server implementation for the reliable UDP protocol. It uses the socket module to create a UDP socket which listens for incoming connections from clients. Once a client is connected, the server performs a 3-way handshake to establish a connection. The server then waits for incoming packets from the client and uses ACKs and retransmissions to ensure reliable transmission. When a file is requested by the client, the server sends the requested file to the client using packets. 

**rUDP\_client.py:**

The rUDP\_client.py file contains the client implementation for the reliable UDP protocol. It also uses the socket module to create a UDP socket which connects to the server. The client performs a 3-way handshake with the server to establish a connection. The client then prompts the user to choose between sending an HTTP request or a file transfer. If an HTTP request is chosen, the client prompts the user for the request parameters and sends the request to the server. If a file transfer is chosen, the client prompts the user to choose between sending or receiving a file, and then prompts the user for the file name. The client then sends the desired file to the server or receives the file from the server using packets. 

**The server should start before the client and has no actions. Client:** 

1. The client is asked to choose lose rate and corruption rate (to test the connection): 

![](\assets\5.png)

2. Then asked if want a HTTP request or to transmit file: 

![](\assets\6.png)

3. File                                                                  HTTP 

![](\assets\7.png) 							![](\assets\8.png)

4. After entering the file name, the 3-way handshake is completed and then the packets is sent either from server to client or from client to server and the following are some test cases  

**HTTP GET request:** 

![](\assets\9.jpeg)

**HTTP POST request:** 

![](\assets\10.jpeg)

**Client sending file:** 

![](\assets\11.jpeg)

**Client receiving file:** 

![](\assets\12.jpeg)

**Bonus:** 

Web page that can upload or download using GET and POST HTTP requests, the requests are printed in the terminals of gateway and server. 

![](\assets\13.jpeg)

Wire shark screenshot shows how connection is established between gateway, browser, and server. And how data is sent and received. 

![](\assets\14.jpeg)

Example of terminal output while running server and gateway: 

![](\assets\15.jpeg)
