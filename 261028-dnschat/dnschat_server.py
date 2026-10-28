import socket
import threading

def receive(sock):
    # 연결 종료 대비 try/finally
    try:
        while True:
            recvData = sock.recv(1024)
            # socket close 예외처리
            if recvData == b"":
                break
            else:
                # 메시지 보낸 소켓 빼고 나머지한테 메시지 돌리기
                # 다른 사람 기다릴까봐 복사만 뜨기
                with lock:
                    snapshot = list(clients)
                for s in snapshot:
                    if s != sock:
                        # .send() 실패 예외처리
                        try:
                            s.send(recvData)
                        except OSError:
                            print("Failed to send someone's messages.")
    # .recv() 실패 예외처리
    except OSError:
        print("Failed to receive someone's messages.")
    finally:
        disconnect(sock)

def disconnect(sock):
    with lock:
        clients.remove(sock)
        print("Someone left chat.")
        print(f"Current active users: {len(clients)}")
    sock.close()
    
HOST = '127.0.0.1'
PORT = 11111
# Domain = 'chatchat.chat'

clients = []
lock = threading.Lock()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print("Welcome to the chatchat.chat!")
    print("Connecting...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f'User {client_address} entered to chat.')
        print('Please Welcome!')

        with lock:
            clients.append(client_socket)
        
        threading.Thread(target = receive, args = (client_socket,), daemon=True).start()