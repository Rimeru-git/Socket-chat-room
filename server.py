import socket
import threading

class Client:
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
    nickname = ""

host = "127.0.0.1"
port = 4321

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []

def Broadcast(message, client):
    for i in clients:
        if i != client:
            i.conn.sendall(message)

def Handle(client):
    while True:
        tmp = b''
        while tmp[-2:] != b"\r\n":
            tmp += client.conn.recv(1)
        length = int(tmp, 10)
        message = b''
        while length > 0:
            chunk = client.conn.recv(1024)
            message += chunk
            length -= len(chunk)
        if message.decode() == client.nickname + ": !quit":
            ad = client.nickname + " has left the chat room!"
            print(ad)
            Broadcast((str(len(ad)) + '\r\n' + ad).encode('utf8'), client)
            client.conn.close()
            clients.remove(client)
            break
        Broadcast(tmp + message, client)

def Receive():
    while True:
        client = Client()
        client.conn, address = server.accept()
        print("Connected with " + str(address))

        client.conn.send(b'4\r\nNICK')
        tmp = b''
        while tmp[-2:] != b"\r\n":
            tmp += client.conn.recv(1)
        length = int(tmp, 10)
        message = b''
        while length > 0:
            chunk = client.conn.recv(1024)
            message += chunk
            length -= len(chunk)
        client.nickname = message.decode('utf8')
        clients.append(client)

        print("Welcome " + client.nickname + "!")
        ad = client.nickname + " joined!"
        Broadcast((str(len(ad)) + '\r\n' + ad).encode('utf8'), client)
        ad = "Connected to server!"
        client.conn.send((str(len(ad)) + '\r\n' + ad).encode('utf8'))

        thread = threading.Thread(target=Handle, args=(client,))
        thread.start()

print("Server is listening...")
Receive()