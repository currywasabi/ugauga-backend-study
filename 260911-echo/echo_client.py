import socket

HOST_TARGET = '127.0.0.1'
PORT_TARGET = 65432

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.connect((HOST_TARGET, PORT_TARGET))

server_socket.send(input("송신할 내용 입력: ").encode('utf-8'))
data = server_socket.recv(1024)

print('received data: ', repr(data.decode('utf-8')))