# Network-Diagnostic-Tools-using-UDP-TCP-and-ICMP-Protocols
## TASK 1: UDP Pinger
These python files  consists of two main components:

1. **UDP Ping Client**: A client that sends UDP ping requests to a server and measures round-trip time (RTT). If a request times out, it attempts to capture and decode ICMP error messages.
2. **UDP Ping Server**: A server that responds to UDP ping requests from the client and randomly drops some packets to simulate packet loss.

## Overview

### 1. UDP Ping Client

**File**: `udp_ping_client.py`

This script sends a specified number of UDP ping requests to a server and measures the round-trip time (RTT) for each request. It handles timeouts and attempts to decode ICMP error messages if a UDP response is not received.
(Therefore acts as a Pinger function using UDP Protocol).

**Key Functions**:
- `decode_icmp(packet)`: Decodes ICMP error messages.
- `udp_ping(server_address, N)`: Sends UDP pings to the server and calculates RTTs.

### 2. UDP Ping Server

**File**: `UDPPingerServer.py`

This script listens for incoming UDP ping requests and responds with the capitalized version of the received message. It randomly drops some packets to simulate packet loss.

**Key Functions**:
- `handle_client(addr, serverSocket)`: Handles incoming UDP requests and responds accordingly.

The UDP Pinger Client and Server are implemented in the filename UDPPingerCLient.py and UDPPingerServer.py respectively. These can be executed through the following commands - 

## Steps to execute the files -

#### Starting the UDP Server
```bash
python3 UDPPingerServer.py
```

#### Starting the UDP Client
```bash
python3 UDPPingerClient.py
```

Multithreading has been implemented in the Server code. Therefore, multiple clients can be connected to the same server.
Once the Client socket is created, it prompts for a value of N. N signifies the no. of ping messages to be sent.

The output displays the message sent from the server, RTT for each packet and the Packet statistics at the end of the execution.

### For Modified UDP Server

In this case, we will be simulating the packet loss at NIC level using the tc (traffic control) utility in linux.

#### Injecting 20% loss at the server end
```bash
sudo tc qdisc add dev <interface-name-eg-wlo1> root netem loss 20%
```
#### Command to view if packet loss enabled
```bash
tc qdisc show dev wlo1
```
#### running the UDP modified server
```bash
python3 UDPPingerModifiedServer.py
```
#### then starting the UDP Client
```bash
python3 UDPPingerClient.py
```
Make sure to disable the packet loss, post execution.
```bash
sudo tc qdisc del dev <interface-name-eg-wlo1> root netem
```

For simulating UDP packet loss and receive so icmp response, we can use the following command to explicity drop udp packets at the server side
```bash
sudo iptables -A INPUT -s <source_ip_address> -p udp -j REJECT --reject-with <error_response>
```

## TASK 2: TCP Pinger

The files consists of a TCP client and server designed to simulate a network ping operation using TCP connections. The client sends multiple packets to the server, measures the Round-Trip Time (RTT) for each packet, and reports on packet loss and RTT statistics. The server handles incoming connections and simulates packet loss to provide a realistic ping experience.

## Overview

- **Client**: Sends TCP packets to the server, measures RTT for each packet, and displays packet loss and RTT statistics.
- **Server**: Receives TCP packets from the client, optionally drops packets based on a random chance, and responds with the message it received.

## Features

- **Client**:
  - Connects to the server and sends a series of packets.
  - Measures and reports RTT for each packet.
  - Calculates and displays packet loss percentage, average RTT, minimum RTT, and maximum RTT.

- **Server**:
  - Receives messages from clients and sends back responses.
  - Simulates packet loss by occasionally not responding to messages.
  
## Steps to execute the files -
The TCP Pinger Client and Server are implemented in the filename TCPPingerClient.py and TCPPingerServer.py respectively. These can be executed through the following commands - 

Similar to the UDP Pinger, these can be executed using the following commands

```bash
# Starting server
python3 TCPPingerServer.py

# Starting Client
python3 TCPPingerClient.py
```

For executing the modified TCP server, similar to UDP 20% packet loss needs to be injected at the NIC level.
```bash
# injecting packet loss
sudo tc qdisc add dev <interface-name-eg-wlo1> root netem loss 20%

# verifying the configuration
tc qdisc show dev wlo1

# Starting the modified
python3 TCPPingerModifiedServer.py

# Starting Client
python3 TCPPingerClient.py

# Disabling the packet loss
sudo tc qdisc del dev <interface-name-eg-wlo1> root netem
```
For simulating TCP packet loss and receive so icmp response, we can use the following command to explicity drop udp packets at the server side
```bash
sudo iptables -A INPUT -s <source_ip_address> -p tcp -j REJECT --reject-with <error_response>
```


## TASK 3: ICMP Pinger

The ICMP Pinger Client is implemented in the file named - ICMPPingerClient.py


## Features

- **ICMP Ping**: Sends ICMP Echo Request packets to a specified IP address or hostname and measures the RTT.
- **Error Handling**: Displays error messages for common ICMP errors like destination unreachable and time exceeded.
- **Statistics**: Provides statistics on packet loss, average RTT, minimum RTT, and maximum RTT.
- **Cross-Platform**: Works on different platforms, including Windows and macOS.

**Parameters:**
- `host` (str): The hostname or IP address of the target machine.
- `timeout` (int, optional): The timeout period (in seconds) to wait for a response. Default is 1 second.

## Steps to execute the files -

Inorder to execute, update the destination ip in the main function of the code file and then run the following command- 

```bash
python3 ICMPPingerClient.py
```
For simulating packet loss- configure iptables rule on the destination machine, to reject any icmp packets from the source machine with a specific error code.
```bash
sudo iptables -A INPUT -s <source_ip_address> -p icmp -j REJECT --reject-with <error_response>
```

Error response code could be - 
- icmp-host-unreachable
- icmp-port-unreachable 


To clear all iptables rule
```bash
sudo iptables -F
```
