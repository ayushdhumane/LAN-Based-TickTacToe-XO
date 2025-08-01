import socket
import threading

def receive_messages(sock):
    while True:
        data = sock.recv(1024).decode()
        if not data:
            break
        print(data)

server_ip = input("Enter server IP: ")
client = socket.socket()#socket.AF_INET, socket.SOCK_STREAM
client.connect((server_ip, 9812))

threading.Thread(target=receive_messages, args=(client,), daemon=True).start()

while True:
    try:
        message = input()
        client.send(message.encode())
    except:
        break
