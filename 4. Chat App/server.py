import socket
import select

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((IP, PORT))
server.listen()

socket_list = [server]
clients = {}


def receive(client):
    try:
        message_header = client.recv(HEADER_LENGTH)
        if not len(message_header):
            return False
        message_length = int(message_header.decode("utf-8").strip())
        return {"header": message_header, "data": client.recv(message_length)}
    except:
        return False


while True:
    read_sockets, _, exception_sockets = select.select(socket_list, [], socket_list)
    for s in read_sockets:
        if s == server:
            client, client_address = server.accept()

            user = receive(client)
            if user is False:
                continue
            socket_list.append(client)

            clients[client] = user

            print(
                f"Accepted new connection from {client_address[0]}:{client_address[1]} username: {user['data'].decode('utf-8')}")
        else:
            message = receive(s)

            if message is False:
                print(f"Closed connection from {clients[s]['data'].decode('utf-8')}")
                socket_list.remove(s)
                del clients[s]
                continue

            user = clients[s]
            print(f"Received message from {user['data'].decode('utf-8')} : {message['data'].decode('utf-8')}")
            if client in clients:
                if client is s:
                    client.send(user['header'] + user['data'] + message['header'] + message['data'])
    for s in exception_sockets:
        socket_list.remove(s)
        del clients[s]
