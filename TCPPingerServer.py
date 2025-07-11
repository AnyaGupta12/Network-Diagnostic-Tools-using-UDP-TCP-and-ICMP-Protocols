# importing the necessary ips
import socket
import threading
import random

# Specifying the server ip and port
IP = '192.168.114.229'
PORT = 11001
ADDR = (IP, PORT)

# defining the handle_client function, it will be called whenever a new client connects
def handle_client(conn, addr):
    try:
        print (f"[NEW CONNECTION] {addr} connected ")
        
        # till the client is connected, the server will continue to recieve requests
        connected = True
    
        while connected:

            #initializing a rondom integer variable to take values between 1 to 10
            rand = random.randint(1, 10)

            # receiving message from the client
            msg = conn.recv(1024).decode("utf-8")
            if msg == "!Disconnect":
                connected = False
            
            msg = msg.upper()
            #print (f"[{addr}],{msg}")

            # if the random integer variable is greater than 8, than there isn't any response being sent to the client.
            ## to make it seem like the packet has dropped.
            if rand > 8:
                continue

            # Sending the message back to the client in upper case
            msg = f"{msg}"
            conn.send(msg.encode("utf-8"))

    # Incase of a keyboard interrupt, the connection with the client should close
    except KeyboardInterrupt:
        print("\n Ping operation interrupted.")

    # Closing the connection
    finally:
        conn.close()    
    
        
#main function
if __name__ == "__main__":
    # creating the server socket and binding it to the port
    print (f"[SERVER STARTING] server is starting..")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)

    # listening for requests from clients
    server.listen()
    print (f"[LISTENING] server is listening on {IP}:{PORT}")
    
    try:
        while True:
            
            #accepting connection request from clients
            conn, addr = server.accept()

            # Implementing multithreading
            #creating a thread for the client and calling the handle_client function for the same
            thread = threading.Thread(target=handle_client, args=(conn,addr))
            thread.start()

    except KeyboardInterrupt:
        #closing socket incase of a keyboard interrupt
        print ("\n Keyboard interrupt: Closing connection ")
        server.close()
        

