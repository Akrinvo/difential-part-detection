import socket

sender_ip = "192.168.1.181"
port = 5002

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP CONNECTION

server_socket.bind((sender_ip, port))

server_socket.listen()

client_socket, client_address = server_socket.accept()

print("Connected")

def send(message):
    
    # message, type: string, any data to be sent to client

    client_socket.sendall(message.encode())

    print("Data Sent")

message = "Hi Buddy."

send(message)

client_socket.close()
server_socket.close()
