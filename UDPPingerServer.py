# UDPPingerServer.py
# We will need the following module to generate randomized lost packets
import random
from socket import *
import socket

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Assign IP address and port number to socket
serverSocket.bind(('127.0.0.1', 11045))


def handle_client(addr, serverSocket):
    print(f"Listening from {addr}")

    try:
        while True:
            # Generate a random number between 1 to 10 (both inclusive)
            rand = random.randint(1, 10)

            # Receive the client packet along with the address it is coming from
            message, address = serverSocket.recvfrom(1024)
            #print ()

            # Capitalize the message from the client
            message = message.upper()

            # If rand is greater than 8, we consider the packet lost and do not respon to the client
            if rand > 8:
               continue

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
        
        handle_client(addr,serverSocket)