import socket
import threading
import queue 

print("/////////////////////////////////////////////////////////////////////////")
print("            Created by Manasvi a P2P Chat system              ")
print("                     Welcome to the server side                          ")
print("/////////////////////////////////////////////////////////////////////////")

#Creates a Queue object to store incoming messages.

messages = queue.Queue()

#This function listens for incoming messages from clients on the server socket and adds them to the messages queue.

def receive():
    while True:
        try:
            message, addr = server.recvfrom(4096) 
            messages.put((message, addr))
        except:
            pass

#With the exception of the sender, this function monitors the messages queue for new messages and broadcasts them to all connected clients. 
# The client's name and address are added to the client addresses dictionary if the client provides a "NAME:" message. A new thread is 
# initiated to establish peer-to-peer connections if there are many connected clients. A client's address is deleted from the client 
# addresses dictionary if it cannot be reached

def broadcast():
    while True:
        while not messages.empty():
            message, addr = messages.get()

            if message.decode().startswith("NAME:"):
                name = message.decode() [message.decode().index(":")+1:]
                print(f"{name} joined the server!")
                client_addresses[name] = addr
                if len(client_addresses) > 1:
                    threading.Thread(target=establish_p2p_connections).start()
            for client in client_addresses:
                try:
                    if message.decode().startswith("CHAT:"):
                        server.sendto(message, client_addresses[client])
                except:
                    del client_addresses[client]

# Peer-to-peer connections are made between clients using these features. connect to client() creates a direct connection by sending a 
# "CONNECT:" message to a client along with the address of another client. Every client in client addresses is iterated through by 
# establish p2p connections(), if the coonnection is not already made the connection is then established.

def connect_to_client(client_address, target_address):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = (f"CONNECT:{target_address}").encode()
    client_socket.sendto(message, client_address)
    client_socket.close()

def establish_p2p_connections():
    for name in client_addresses:
        for peer in client_addresses:
            if peer != name:
                connect_to_client(client_addresses[name], client_addresses[peer])
                
# This step configures the server and launches two threads—one for message reception and the other for message broadcasting. The server 
# socket is constructed and tied to this address, and the server address is set to "10.35.70.19" on port 33201. The receive() and broadcast() 
# methods are launched as two separate threads. Using start, these threads are launched ().

client_addresses = {}
server_address = ("10.35.70.19", 33201)
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(server_address)

t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=broadcast)

t1.start()
t2.start()