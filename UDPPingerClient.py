import time
import socket
import sys
import struct

# Function to decode ICMP error message
def decode_icmp(packet):

    # Creating a dictionary of ICMP type and code
    error_codes = {
        (3,0):"Destination Network Unreachable",
        (3,1):"Destination Host Unreachable",
        (3,2):"Destination Protocol Unreachable",
        (3,3):"Destination Port Unreachable"
    }

    # ICMP header starts after the IP header
    ## separating the icmp header from the packet received. (160 -223 bit -> 20th byte - 27th byte)
    icmp_header = packet[20:28]  
    icmp_type, code, checksum, ID, sequence = struct.unpack('bbHHh', icmp_header)
    print(f"ICMP Type: {icmp_type}, Code: {code}")

    # extracting the error message from error_codes dictionary
    if icmp_type == 3:  
        return f"ICMP Error: {error_codes[(icmp_type,code)]}"
    # Time Exceeded
    elif icmp_type == 11:  
        return "Time to Live (TTL) Expired"
    else:
        return f"Unknown ICMP Error: Type={icmp_type}, Code={code}"

# Function to ping the server N times
def udp_ping(server_address, N):

    # Creating a UDP socket for sending pings
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    client_socket.settimeout(1)  # Set 1-second timeout for responses

    # Creating an ICMP socket 
    icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)  
    icmp_socket.settimeout(1)  # Timeout to capture ICMP responses

    # initializing an empty list for storing the list of all RTTs
    list_RTT = []

    # initializing the packets_lost count to 0
    packets_lost = 0

    for i in range(1, N + 1):
        message = f"ping {i} {time.time()}"

        # implemented exception handling for handling UDP timeout
        try:
            # Send the ping message via UDP to server
            start_time = time.time()
            client_socket.sendto(message.encode(), server_address)

            # Receive the UDP response from server
            response, address = client_socket.recvfrom(1024)
            end_time = time.time()

            # Calculate RTT in milliseconds
            rtt = (end_time - start_time) * 1000
            list_RTT.append(rtt)

            # Printing the received message and RTT
            print(f"Received: {response.decode()}")
            print(f"RTT for packet {i}: {rtt:.3f} ms")

        except socket.timeout:
            # Handle timeout if no UDP response is received within 1 second
            print(f"Request timed out for packet {i}")
            packets_lost += 1

            # Incase of UDP timeout, wait for capturing ICMP packet
            ## implemented exeception handling for handling ICMP timeouts.
            try:
                # receive icmp response
                icmp_response, _ = icmp_socket.recvfrom(1024)
                icmp_error = decode_icmp(icmp_response)
                if icmp_error:
                    print(f"Received ICMP error for packet {i}: {icmp_error}")

            except socket.timeout:
                # No ICMP error message received within the timeout
                print(f"ICMP request timeout for packet {i}")


    # Print Packet statistics
    if list_RTT:
        print (f"Packet Statistics:")
        print (f"\t Packets loss percentage: {(packets_lost/N)*100:.2f}%")
        print (f"\t Average RTT: {sum(list_RTT)/len(list_RTT)}")
        print (f"\t Minimum RTT: {min(list_RTT)},\n\t Maximum RTT: {max(list_RTT)}")
    else:
        print("\nNo packets were received. All requests timed out.")

    # closing UDP and ICMP sockets
    client_socket.close()
    icmp_socket.close()

# define main function
if __name__ == "__main__":

    server_ip = input('Enter the Server IP - ')
    server_port = int(input('Enter the Server Port Number - '))

    # Taking the number of ping requests to be sent as input
    N = int(input('Enter the Number of packets to be sent - '))

    udp_ping((server_ip, server_port), N)
