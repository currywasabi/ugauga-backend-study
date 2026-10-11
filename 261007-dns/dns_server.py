import socket
from dnslib import DNSRecord, RR, A

# dnslib -> 도메인 뒤에 . 추가
# 채팅 서버 IP임. 다른 컴퓨터 이용해서 실습 시 IP 바꾸기
RECORDS = {'portal.korea.ac.kr.': '127.0.0.1'} 

# IPv4, UDP 소켓 객체 생성
sock  =socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('127.0.0.1', 5354))
print("DNS 서버 대기 중... (5354번 포트)")

while True:
    # 어째서 냅다 recv?
    # dns_resolver.py에서 r.resolve('portal.korea.ac.kr', 'A')를 했다. (과정 중 sendto() 포함)
    # 연결(connect)이 필요한 TCP와 달리 UDP는 sendto()로 냅다 질의 패킷 보낸다.
    # data는 수신한 패킷 자체, address는 송신한 쪽 주소(IP와 포트 튜플)이다.
    data, address = sock.recvfrom(512)
    request = DNSRecord.parse(data) # 바이트 전체를 객체화
    name = str(request.q.qname) # 질의 패킷에서 도메인 추출. request.q에는 qname/qtype/qclass 있다.
    print(f"질의: {name} from {address}")

    # reply 객체 생성 (생성자는 아니고 새 객체 만들어 돌려주는 메소드라고 함)
    # 새로 생긴 DNSRecord는 헤더 ID요청과 동일, 플래그 '응답'으로 설정, 질문 섹션도 복사됨
    # Answer 섹션은 비어 있어서 add_answer로 레코드(RR) 추가
    reply = request.reply() 
    # 실제 있는 도메인일 경우
    if name in RECORDS:
        reply.add_answer(RR(name, rdata=A(RECORDS[name]), ttl=60))
    sock.sendto(reply.pack(), address) #.pack -> .parse 반대. 객체를 바이트화
