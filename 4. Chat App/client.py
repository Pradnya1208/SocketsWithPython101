import socket
import select
import errno
import sys

HEADER_LENGTH =10
IP = "127.0.0.1"
PORT=1234

username = input("Username: ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))
client.setblocking(False)

user_name = username.encode("utf-8")
username_header = f"{len(user_name):<{HEADER_LENGTH}}".encode("utf-8")
client.send(username_header + user_name)

while True:
    message = input(f"{username} > ")
#    message = ""
    if message:
        message = message.encode("utf-8")
        message_header = f"{len(message) :< {HEADER_LENGTH}}".encode("utf-8")
        client.send(message_header + message)
    try:
        while True:
            username_header = client.recv(HEADER_LENGTH)
            if not len(username_header):
                print ("connection closed by the server")
                sys.exit()
            username_length = int(username_header.decode("utf-8").strip())
            user_name = client.recv(username_length).decode("utf-8")
            message_header = client.recv(HEADER_LENGTH)
            message_lenght = int(message_header.decode("utf-8").strip())
            message = client.recv(message_lenght).decode("utf-8")

            print(f"{user_name} > {message}")

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('reading error',str(e))
            sys.exit()
            continue


    except Exception as e:
        print('general error',str(e))
        sys.exit()













