# 구현하고 싶은 것: 초간단 DNS (Domain Name System)

# DNS 왜씀?
# 원하는 서버에 접속하고 싶은데 IP를 일일이 어떻게 외우나. 더 semantic한 정보 = 도메인으로 대체
# 이름-주소 연결뿐만 아니라 이름-이름 연결, 이름 하나에 주소 여러 개 연결, 이름 여러 개에 주소 하나 연결(CNAME) 등 활용법 무궁무진

# 어떤 식으로 씀?
# 클라이언트는 도메인은 알지만 IP 주소를 모른다. 따라서 도메인을 IP로 해석(resolve) 해야 한다.
# 따라서 클라이언트는 DNS 서버한테 특정 도메인을 IP로 resolve 해달라고 요청을 보낸다. (by UDP)
# (왜 UDP? 1. 오버헤드 작고 2. DNS 패킷은 어차피 페이로드 작으므로(심지어 질-답 1회면 끝) UDP로 하는 편이 효율적이라)
# resolve 요청을 보내는 클라이언트측 컴포넌트 = resolver이다.

# 실습할 문제 정의: 도메인 'www.koreauniv.official'의 IP 요청하면 127.0.0.1 반환
# dnspython 라이브러리 안 쓰고 구현하려면 직접 DNS 패킷 바이트 단위로 조립해야 함 (엄...) 예시 코드 봤는데 난리다.
# dnspython을 쓰자!

import dns.resolver

# Resolver 클래스 생성자로 객체 생성
r = dns.resolver.Resolver(configure=False)
# # DNS 서버 IP 등록 / 왜 리스트임? nameserver's'라서?
r.nameservers = ['127.0.0.1']
# # DNS 서버 포트 등록(UDP 기반, 원래는 53. 지금은 개발용 임의 IP)
r.port = 5353

# 테스트용 구글 DNS
# r.nameservers = ['8.8.8.8']
# r.port = 53

# arg1: qname, arg2: record type
# qname이란? 사용자가 찾고자 하는 도메인 이름
# record type이란? 해당 도메인의 무슨 정보를 원하는지
# ex) A -> IPv4 주소, AAAA -> IPv6 주소, CNAME -> 해당 도메인의 별칭Alias
# *www, http/https, 슬래쉬는 프로토콜이나 경로 표시지 도메인이 아님. resolve 시 제외
answer = r.resolve('portal.korea.ac.kr', 'A')
print(answer)
print(answer[0])
print(answer[0].address)