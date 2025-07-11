from socket import *
import sys
import struct
import time
import select


# ICMP response types
ICMP_ECHO_REQUEST = 8
ICMP_ECHO_REPLY = 0


# ICMP general error type codes
ICMP_DEST_UNREACH = 3
ICMP_TIME_EXCEEDED = 11

# Using counter variable for packet sequence identifier
unique_id_counter = 1



# Defining cehcksum calculator here that is used JUST as a parameter in an ICMP Packet
def checksum(string):
    csum = 0
    countTo = (len(string) // 2) * 2
    count = 0

    while count < countTo:
        thisVal = string[count+1] * 256 + string[count]
        csum = csum + thisVal
        csum = csum & 0xffffffff
        count = count + 2

    if countTo < len(string):
        csum = csum + string[len(string) - 1]
        csum = csum & 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    
    return answer

def parseICMPError(type, code):
    # Error messages for ICMP Type and Code combinations for it 
    ICMP_ERRORS = {
        ICMP_DEST_UNREACH: {
            0: "Destination Network Unreachable",
            1: "Destination Host Unreachable",
            2: "Destination Protocol Unreachable",
            3: "Destination Port Unreachable",
            4: "Fragmentation Required, and DF Flag Set",
            5: "Source Route Failed",
            6: "Destination Network Unknown",
            7: "Destination Host Unknown"
        },
        ICMP_TIME_EXCEEDED: {
            0: "TTL Expired in Transit",
            1: "Fragment Reassembly Time Exceeded"
        }
    }  
    
    return ICMP_ERRORS[type][code]

def receiveOnePing(mySocket, ID, timeout, destAddr, sequence):
    timeLeft = timeout
    while 1:
        startedSelect = time.time()
        #T he socket waits for the icmpm resomponse for the timeout defined
        icmp_response = select.select([mySocket], [], [], timeLeft)
        howLongInSelect = (time.time() - startedSelect)
        if icmp_response[0] == []:  
            return None  # If packet not recieved return delay as NONE(NULL object)

        timeReceived = time.time()
        recPacket, address = mySocket.recvfrom(1024)

        # Separating the icmp header from the packet received. (160 -223 bit -> 20th byte - 27th byte)
        icmpHeader = recPacket[20:28]
        unpacked_icmp_header = struct.unpack("bbHHh", icmpHeader)
        type = unpacked_icmp_header[0]
        code = unpacked_icmp_header[1]
        packetID = unpacked_icmp_header[3]
        packetSequence = unpacked_icmp_header[4]
        # Unpacking the type,code,packetID,sequence of recieved ICMP packet
        

        # If a reply is received before timeout we calculate the RTT and return it.
        # We are strictly waiting for that packetID that is sent as we are waiting for timeout(which will be around 1 second for each packet).
        if packetID == ID and type == ICMP_ECHO_REPLY and packetSequence == sequence:
            bytesInDouble = struct.calcsize("d")
            timeSent = struct.unpack("d", recPacket[28:28 + bytesInDouble])[0]
            rtt = timeReceived - timeSent
            return rtt
        
        
        # Parsing the ICMP errors if it is present
        if type in (ICMP_DEST_UNREACH, ICMP_TIME_EXCEEDED):
            print(f"ICMP Error: {parseICMPError(type, code)}")
            return None

        #T his is done to ensure that the packet is recieved within the timeout range(0< time recieved <= timeout)
        timeLeft = timeLeft - howLongInSelect
        if timeLeft <= 0:
            return None  

        

def sendOnePing(mySocket, destAddr, ID, sequence):
    myChecksum = 0
    # Packing the icmp request based on bbHHh byte representation
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, sequence)
    data = struct.pack("d", time.time())
    myChecksum = checksum(header + data)    

    if sys.platform == 'darwin':
        myChecksum = htons(myChecksum) & 0xffff
    else:
        myChecksum = htons(myChecksum)
    # Calculating the checksum of both header and data and then repacking it
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, sequence)
    packet = header + data
    # Sending the ICMP packet through the socket
    mySocket.sendto(packet, (destAddr, 1))

def doOnePing(destAddr, timeout, sequence):
    # Finding the protocol through name 
    icmp = getprotobyname("icmp")
    mySocket = socket(AF_INET, SOCK_RAW, icmp)

    # Using counter for packet indentifier
    global unique_id_counter
    myID = unique_id_counter
    unique_id_counter += 1

    sendOnePing(mySocket, destAddr, myID, sequence)
    delay = receiveOnePing(mySocket, myID, timeout, destAddr, sequence)
    if delay is None:
        print(f"Request timed out for packet sequence {myID}")

    mySocket.close()
    return delay
    # doOnePing function finds the delay of the ICMP packet for Pinger

def ping(host, timeout=1):
    dest = gethostbyname(host)
    print(f"Pinging {dest} using Python:")

    sent_packets = 0
    received_packets = 0
    rtts = []

    sequence = 1
    try:
        while True:
            sent_packets += 1
            delay = doOnePing(dest, timeout, sequence)
            # Calculating the ping of each packet  in millisecond
            if delay is not None:
                received_packets += 1
                rtts.append(delay * 1000)  
                print(f"Reply from {dest}: time={round(delay * 1000, 4)} ms")
            sequence += 1  
            time.sleep(1)
            # Giving each ping operation a 1 second break

    except KeyboardInterrupt:
        # Ctrl+C pressed, calculating and printing statistics as based on general PINGER FUNCTION
        print ("\n Packet Statistics:")
        packets_lost = sent_packets - received_packets
        print (f"\t Packets loss percentage: {(packets_lost/sent_packets)*100:.2f}%")
        if rtts:
            print (f"\t Average RTT: {sum(rtts)/len(rtts)}")
            print (f"\t Minimum RTT: {min(rtts)},\n\t Maximum RTT: {max(rtts)}")
        sys.exit()

if __name__ == "__main__":
    url_ip = "192.168.114.218"
    ping(url_ip)
