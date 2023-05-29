import socket
import threading 
import random
import hashlib
import getpass

#This line creates a new instance of the SHA-256 hash algorithm from the hashlib module and hashes the byte string representation of the password "password". The resulting hash is then converted to a hexadecimal string using the hexdigest() method. Finally, the first five characters of the resulting string are extracted, which will be used as the password for authentication. This method is more secure than using the MD5 algorithm, as it provides a stronger and more complex hash.
password = hashlib.sha256(b"password").hexdigest()[:5]

#This line creates a UDP socket object for the client and binds it to a random port number between 34000 and 39000 on the localhost

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
client.bind(("10.35.70.19", random.randint(34000, 39000)))

print("/////////////////////////////////////////////////////////////////////////")
print("            Created by Manasvi a P2P Chat system              ")
print("                     Welcome to the client side                          ")
print("/////////////////////////////////////////////////////////////////////////")

print("Enter Password for connection: ")
passt=getpass.getpass()

#This code checks whether the password entered by the user matches the hashed password stored in the server.

if passt==password:
    name = input("Please enter your name: ")
    target_address = None
    
    # This function keeps an eye out for new messages coming in from the P2P chat server or other clients. 
    # If the message being received is a "CONNECT" message, the target client's IP address and port number are extracted,
    # and the target address variable is set. After that, it opens a new thread to accept messages from the target client 
    # and notifies them that the current client has entered the conversation. The message is simply printed out if it is not a "CONNECT" 
    # message.
    
    def receive():
        global target_address
        while True:
            try:
                message, _ = client.recvfrom(4096)
                if message.decode().startswith("CONNECT:"):
                    target_address_str = message.decode()[len("CONNECT:"):]
                    # ip = target_address_str[2:13]
                    # port =  target_address_str[16:21]
                    ip , port = target_address_str.split(':')
                    target_address = (ip, int(port))   
                    target_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    temp = (f"{name} has joined the p2p chat!").encode()
                    target_socket.sendto(temp, target_address)
                    threading.Thread(target=receive_from_target, args=(target_socket,)).start()
                else:
                    print(message.decode())
            except:
                pass

    # This function is called in the above loop so as to recieve measssages form the target address     
    
    def receive_from_target(target_socket):
        while True:
            message, _ = target_socket.recvfrom(4096)
            print(message.decode())

    t = threading.Thread (target=receive)
    t.start()

    server_address = ("10.35.70.19", 33201)
    client.sendto(f"NAME:{name}".encode(), server_address)

    #This code runs an infinite loop that waits for the user to enter a message. If the message is "!q", it closes the client 
    # and exits the program.
    
    while True:
        message = input("")
        if message == "!q":
            client.close()
            exit()
        else:
            if target_address is not None:
                client.sendto(f"CHAT:{name}: {message}".encode(), target_address)
                if message.startswith("SOS"):
                    message = "HELP WE ARE IN TROUBLE"
                    client.sendto(f"CHAT:{name}: {message}".encode(), target_address)
                elif message.startswith("MAYDAY"):
                    message = "HELP MAYDAY MAYDAY"
                    client.sendto(f"CHAT:{name}: {message}".encode(), target_address)
                elif message.startswith("FIRE"):
                    message = "FIRE IN THE HOSPITAL"
                    client.sendto(f"CHAT:{name}: {message}".encode(), target_address)
            else:
                client.sendto(f"CHAT:{name}: {message}".encode(), server_address)
                if message.startswith("SOS"):
                    message = "HELP WE ARE IN TROUBLE"
                    client.sendto(f"CHAT:{name}: {message}".encode(), server_address)
                elif message.startswith("MAYDAY"):
                    message = "HELP MAYDAY MAYDAY"
                    client.sendto(f"CHAT:{name}: {message}".encode(), server_address)
                elif message.startswith("FIRE"):
                    message = "FIRE IN THE HOSPITAL"
                    client.sendto(f"CHAT:{name}: {message}".encode(), server_address)
else:
    print("Try Reconnecting again...")
            