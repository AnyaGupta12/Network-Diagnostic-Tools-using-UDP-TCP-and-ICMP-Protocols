# UDPPingerModifiedServer.py
# will be stimulating packet loss using the tc (traffic control) utility in Linux

import random
from socket import *
import threading

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)
# Assign IP address and port number to socket
serverSocket.bind(('192.168.114.229', 11030))


def handle_client(addr, serverSocket):
    print(f"Listening from {addr}")

    try:
        while True:

            # Receive the client packet along with the address it is coming from
            message, address = serverSocket.recvfrom(1024)
            #print ()

            # Capitalize the message from the client
            message = message.upper()
            
            # Otherwise, the server response
            serverSocket.sendto(message, address)

    except KeyboardInterrupt:

        #closing the server socket in case of a keyboard interrupt
        print("\nPing operation interrupted.")
        serverSocket.close()


# defining the main function
if __name__ == "__main__":

    while True:

        # Receiving message from the client
        message, addr = serverSocket.recvfrom(1024)
    
        handle_client(addr, serverSocket)