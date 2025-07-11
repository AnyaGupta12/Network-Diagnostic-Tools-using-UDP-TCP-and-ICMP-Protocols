import errno
import socket
import time
import os

# Function to ping the server N times using TCP
def tcp_ping_client(server_ip, server_port, N):

    # initializing an empty list for storing the list of all RTTs
    list_RTT = []

    # initializing the packets_lost count to 0
    packets_lost = 0

    # Create a raw socket for ICMP error handling
    icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    icmp_socket.settimeout(1)  # Set 1-second timeout for ICMP responses

    for i in range(1, N + 1):

        # creating a separate TCP connection for each ping message
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

        # implementing exception handling for handling TCP socket timeout 
        try:

            # Record the start time
            start_time = time.time()

            # Connecting to the TCP server
            client_socket.connect((server_ip, server_port))
            client_socket.settimeout(1)  # Set a timeout for the TCP connection

            # Sending ping message to server
            message = f"ping {i} {time.time()}"
            client_socket.send(message.encode())  

            # Try to receive a TCP response
            response = client_socket.recv(1024)

            # record time when TCP response is received
            end_time = time.time()

            # Calculate RTT in milliseconds
            rtt = (end_time - start_time) * 1000
            list_RTT.append(rtt)
            print(f"Received: {response.decode()}")
            print(f"RTT for packet {i}: {rtt:.3f} ms")

        except socket.timeout:
            # If TCP request times out, check for ICMP error
            print(f"Request timed out for packet {i}")
            packets_lost += 1

        # If TCP connection is not established, the intermediate routers would send an OS error
        except OSError as e:
            if e.errno == 113:
                print(f"Destination Host unreachable for packet {i}")
            elif e.errno == 111:
                print(f"Destination Port unreachable for packet {i}")
            else:
                print(f"Error {e.errno}: {os.strerror(e.errno)} for packet {i}")
            continue

        # Closing the client socket
        finally:
            client_socket.close()  

    # Print packet statistics
    if list_RTT:
        print (f"Packet Statistics:")
        print (f"\t Packets loss percentage: {(packets_lost/N)*100:.2f}%")
        print (f"\t Average RTT: {sum(list_RTT)/len(list_RTT)}")
        print (f"\t Minimum RTT: {min(list_RTT)},\n\t Maximum RTT: {max(list_RTT)}")
    else:
        print("\nNo packets were received. All requests timed out.")

    icmp_socket.close()

# Defining the main function
if __name__ == "__main__":
    server_ip = input('Enter the Server IP - ')
    server_port = int(input('Enter the Server Port Number - '))
    N = int(input('Enter the Number of packets to be sent - '))

    tcp_ping_client(server_ip, server_port, N)
