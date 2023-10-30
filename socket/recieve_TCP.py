import socket

server_ip = "0.0.0.0"
port = 5003

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP CONNECTION

server_socket.bind((server_ip, port))

server_socket.listen()

client_socket, client_address = server_socket.accept()

print("Connected")

def recieve():
    
    # message, type: string, any data to be sent to client

    return client_socket.recv(1024).decode()

recieved_message = recieve()

print("Recived Message :", recieved_message)

client_socket.close()
server_socket.close()
