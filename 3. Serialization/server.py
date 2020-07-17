import socket
import pickle




HEADERSIZE = 10
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(),1234))
s.listen(5)

while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established")
    data = {1: "Murakami", 2:"Kafka on the shore"}
    msg = pickle.dumps(data)
    msg = bytes(f'{len(msg):<{HEADERSIZE}}',"utf-8") + msg
    
    clientsocket.send(bytes(msg))



