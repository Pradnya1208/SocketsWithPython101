import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(),1234))

msg_s = ''
while True:
    msg = s.recv(1020)
    if len(msg) <=0:
        break
    msg_s += msg.decode("utf-8")

print(msg_s)
