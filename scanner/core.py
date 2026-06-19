import socket

sock = socket.socket()
sock.settimeout(1)

target = input("Enter your target: ")
port = int(input("Enter your port: "))
try:
    sock.connect((target, port))
except OSError:
    status = "closed"
else:
    status = "open"

print(status)