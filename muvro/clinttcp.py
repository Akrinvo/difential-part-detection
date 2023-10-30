import threading
import socket

nickname=input("nickname: ")
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip="192.168.1.180"
port=55556
s.connect((ip, port))

def ricezione():
    while True:
        message=s.recv(4096).decode("utf-8")
        if message=="NICK":
            s.send(nickname.encode("utf-8"))
        else:
            print(message)

def scrittura():
    while True:
        message=f'{nickname}: {input("")}'
        s.send(message.encode("utf-8"))
        if message.find("\esc")!=-1:
            s.close()
            exit()

threadR=threading.Thread(target=ricezione)
threadR.start()

threadW=threading.Thread(target=scrittura)
threadW.start()