import socket

#현재 기기 로컬 IP 주소. localhost와 같다 (완전히 같은 개념은 아닌듯)
HOST = '127.0.0.1'
#IP 주소 내 포트. 1~1023까지는 well-known Port로 이미 용도가 정해져 있다고 한다.
PORT = 65432

#소켓 객체 생성. 각각 IPV4 / TCP 의미
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#소켓 객체에 주소, 포트 할당 .bind(IP, 포트)
server_socket.bind((HOST, PORT))
#소켓 연결 시도 듣기. parameter는 최대 연결 수
server_socket.listen()

print("서버 ON")

try:
    while True:
        # 연결 수락. 반환값은 튜플 (소켓 객체, 주소)
        #얘 동기synchronous임
        client_socket, client_address = server_socket.accept()
        print(f"연결 성공 - {client_address}와 연결됨!")

        while True:
            # 데이터 수신 (최대 바이트 사이즈)
            data = client_socket.recv(1024)
            if not data:
                break
            # echo (.sendall 도 있음)
            client_socket.send(data)
        client_socket.close()
finally:
    server_socket.close()




