import socket
from dnslib import DNSRecord, RR, A

RECORDS = {'chatchat.chat.': '127.0.0.1'} 

# IPv4, UDP 소켓 객체 생성
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('127.0.0.1', 5354))
print("DNS 서버 대기 중... (5354번 포트)")

while True:
    data, address = sock.recvfrom(512)
    request = DNSRecord.parse(data) # 바이트 전체를 객체화
    name = str(request.q.qname) # 질의 패킷에서 도메인 추출.
    print(f"질의: {name} from {address}")

    reply = request.reply()

    if name in RECORDS:
        reply.add_answer(RR(name, rdata=A(RECORDS[name]), ttl=60))
    sock.sendto(reply.pack(), address) #.pack -> .parse 반대. 객체를 바이트화
