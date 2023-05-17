import hashlib
import platform


class packet():
    def __init__(self,d):
        self.checksum = 0
        self.sequenceNumber = 0
        self.length = 0
        self.message = 0
        self.ACKnum = 0
        self.SYNbit = 0
        self.FINbit = 0
        self.ACKbit = 0
        self.http_header = ''
        self.delimiter = d
        self.checksum_check = 0

    #To make the packet.
    def makePacket(self, data, http=False):
        #getting the message length
        self.length = str(len(data))
        self.message = data
        #getting the checksum in a hexdigest format
        chksum_data = str(self.sequenceNumber) + self.delimiter + str(self.length) + self.delimiter + str(self.ACKnum) + self.delimiter + str(self.SYNbit) + self.delimiter + str(self.FINbit) + self.delimiter + str(self.ACKbit) 
        if (http):
            chksum_data += self.delimiter + self.http_header
        self.checksum = hashlib.sha1(chksum_data.encode('utf-8')).hexdigest()

        # Construct the packet
        x = str(self.checksum) + self.delimiter + str(self.sequenceNumber) + self.delimiter + str(self.length) + self.delimiter + str(self.ACKnum) + self.delimiter + str(self.SYNbit) + self.delimiter + str(self.FINbit) + self.delimiter + str(self.ACKbit) 
        if (http):
            x += self.delimiter + self.http_header
        x += self.delimiter + self.message
        return x      
    
    def demultiplexPacket(self, pkt):
        messages = pkt.decode().split(self.delimiter)
        self.checksum =           messages[0]
        self.sequenceNumber = int(messages[1])
        self.length =         int(messages[2])
        self.message =            messages[7]
        self.ACKnum =         int(messages[3])
        self.SYNbit =         int(messages[4])
        self.FINbit =         int(messages[5])
        self.ACKbit =         int(messages[6])
        chksum_data =  str(self.sequenceNumber) + self.delimiter + str(self.length) + self.delimiter + str(self.ACKnum) + self.delimiter + str(self.SYNbit) + self.delimiter + str(self.FINbit) + self.delimiter + str(self.ACKbit) 
        #if (choice == 1):
            #checksum += self.delimiter + self.http_header
        self.checksum_check = hashlib.sha1(chksum_data.encode('utf-8')).hexdigest()



"""
HTTP/1.1 Request format:
{http_req} /{Requested_File} HTTP/1.1\n
Host: {host}:{port}\n
Connection: keep-alive\n
sec-ch-ua: "Chromium";v="112", "Microsoft Edge";v="112", "Not:A-Brand";v="99"\n
sec-ch-ua-mobile: ?0\n
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.58\n
sec-ch-ua-platform: "{device_description}"\n
Accept: image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8\n
Sec-Fetch-Site: same-origin\n
Sec-Fetch-Mode: no-cors\n
Sec-Fetch-Dest: image\n
Referer: http://127.0.0.1:8000/{filename}\n
Accept-Encoding: gzip, deflate, br\n
Accept-Language: en-GB,en;q=0.9,en-US;q=0.8\n
"""
