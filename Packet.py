import hashlib

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
        chksum_data = str(self.sequenceNumber) + self.delimiter + str(self.length) + self.delimiter + str(self.ACKnum)\
                    + self.delimiter + str(self.SYNbit) + self.delimiter + str(self.FINbit) + self.delimiter + str(self.ACKbit) 
        if (http):
            chksum_data += self.delimiter + self.http_header
        self.checksum = hashlib.sha1(chksum_data.encode('utf-8')).hexdigest()

        # Construct the packet
        x = str(self.checksum) + self.delimiter + str(self.sequenceNumber) + self.delimiter + str(self.length) + self.delimiter +\
            str(self.ACKnum) + self.delimiter + str(self.SYNbit) + self.delimiter + str(self.FINbit) + self.delimiter + str(self.ACKbit) 
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
        chksum_data =  str(self.sequenceNumber) + self.delimiter + str(self.length) + self.delimiter + str(self.ACKnum)\
                    + self.delimiter + str(self.SYNbit) + self.delimiter + str(self.FINbit) + self.delimiter + str(self.ACKbit) 
        self.checksum_check = hashlib.sha1(chksum_data.encode('utf-8')).hexdigest()