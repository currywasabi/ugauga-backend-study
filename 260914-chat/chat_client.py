from socket import *
from threading import *
import time

def send(sock):
    while True:
        sendData = input('')
        sock.send(sendData.encode('utf-8'))
        if sendData == "Q":
            client_socket.close()
            print("채팅방에서 나가셨습니다.")

def receive(sock):
    while True:
        recvData = sock.recv(1024)
        print(">>> ", recvData.decode('utf-8'))


HOST = '127.0.0.1'
PORT = 11111

# with문 - 블록 끝나면 자동으로 객체.close() 실행
with socket(AF_INET, SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))

    print("채팅 서버에 접속했습니다.")
    print("채팅을 시작하세요.")

    sender = Thread(target = send, args = (client_socket,))
    receiver = Thread(target = receive, args = (client_socket,))

    sender.start()
    receiver.start()

    while True:
        time.sleep(1)
        pass



        


