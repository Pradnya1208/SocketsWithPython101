import socket
import pickle

HEADERSIZE = 10
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1234))

while True:

    msg_s = b''
    new_msg = True
    while True:
        msg = s.recv(16)
        if new_msg:
            print(f"length of new message is :{msg[:HEADERSIZE]}")
            msg_len = int(msg[:HEADERSIZE])
            new_msg = False

        msg_s += msg

        if len(msg_s)-HEADERSIZE == msg_len:
            print("Messgae recieved")
            print(msg_s[HEADERSIZE:])

            data = pickle.loads(msg_s[HEADERSIZE:])
            print(data)
            new_msg = True
            msg_s = b''

    print(msg_s)
