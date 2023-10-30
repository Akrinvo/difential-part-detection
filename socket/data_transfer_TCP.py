import socket

server_ip = "192.168.1.181"
port = 5004

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP CONNECTION

server_socket.bind((server_ip, port))

server_socket.listen()

client_socket, client_address = server_socket.accept()


while True:

    

    print("DATA SENT")

    recieved_data = client_socket.recv(1024).decode()

    print("Recieved Data : ",recieved_data)
    recieved_data=recieved_data.replace("}","").replace("{",'').split(":")[-1]
    client_socket.sendall(str(recieved_data).encode())
    