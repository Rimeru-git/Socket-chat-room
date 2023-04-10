import socket
import threading

state = threading.Event()
state.set()

def Send(client):
    while state.is_set(): 
        try:
            message = nickname + ": " + input()
            length = len(message)
            client.sendall((str(length) + '\r\n' + message).encode("utf8"))
            if message == nickname + ": !quit":
                state.clear()
                client.close()
                print("Closing connection!")
                break
        except BlockingIOError:
            pass

def Receive(client):
    while state.is_set(): 
        try:
            tmp = b''
            while tmp[-2:] != b"\r\n":
                tmp += client.recv(1)
            length = int(tmp, 10)
            message = b''
            while length > 0:
                chunk = client.recv(1024)
                message += chunk
                length -= len(chunk)
            if message == b'NICK':
                client.send((str(len(nickname)) + '\r\n' + nickname).encode('utf8'))
            else:
                print(message.decode())
        except BlockingIOError:
            pass
        except:
            state.clear()
            print("An error occurred!")
            client.close()   
            break

nickname = input("Choose your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 4321))
client.setblocking(False)

receiveThread = threading.Thread(target=Receive, args=(client,))
sendThread = threading.Thread(target=Send, args=(client,))

receiveThread.start()
sendThread.start()

receiveThread.join()
sendThread.join()
