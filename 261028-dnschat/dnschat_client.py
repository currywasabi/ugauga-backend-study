import socket
import threading
import dns.resolver

def send(sock):
    while True:
        sendData = input('')
        if sendData == "Q":
            sock.shutdown(socket.SHUT_RDWR)
            sock.close()
            break
        else:
            sock.send(sendData.encode('utf-8'))
    print("채팅방에서 나가셨습니다.")

def receive(sock):
    while True:
        recvData = sock.recv(1024)
        # 서버 종료(b"" 반환) 예외처리
        if not recvData:
            break
        else:
            print(">>> ", recvData.decode('utf-8'))
    print("서버가 종료되었습니다.")
    print("엔터를 눌러 프로그램을 종료하세요.")

r = dns.resolver.Resolver(configure=False)
r.nameservers = ['127.0.0.1']
r.port = 5354

print("접속하고자 하는 사이트의 도메인을 입력해 주세요.")
print("다대다 채팅방 도메인 - chatchat.chat")

while True:
    domain = input(">>> ")
    try:
        answer = r.resolve(domain, 'A')
        break
    except Exception:
        print("입력한 도메인이 잘못되었거나 DNS 연결이 실패하였습니다.")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((answer[0].address, 11111))

    print("채팅 서버에 접속했습니다.")
    print("채팅을 시작하세요. (나가기: Q)")

    sender = threading.Thread(target = send, args = (client_socket,), daemon=True)
    receiver = threading.Thread(target = receive, args = (client_socket,), daemon=True)

    sender.start()
    receiver.start()

    # 우아한 프로그램 종료 처리. 함수 내 while break되면 끝
    sender.join()