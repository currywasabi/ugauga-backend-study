# 일대일 채팅 서버
# 참고문헌: https://oo7-0310.tistory.com/25 

from socket import *
from threading import *
import time

def send(sock):
    while True:
        sendData = input('')
        sock.send(sendData.encode('utf-8'))

def receive(sock):
    while True:
        recvData = sock.recv(1024)
        print(">>> ", recvData.decode('utf-8'))


HOST = '127.0.0.1'
PORT = 11111

# with문 - 블록 끝나면 자동으로 객체.close() 실행
with socket(AF_INET, SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print("채팅 서버가 열렸습니다.")
    print("접속 대기 중……")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"사용자-{client_address}와 연결되었습니다!")
        print("채팅을 시작하세요.")

        sender = Thread(target = send, args = (client_socket,))
        receiver = Thread(target = receive, args = (client_socket,))

        sender.start()
        receiver.start()

        while True:
            time.sleep(1)
            pass



        


