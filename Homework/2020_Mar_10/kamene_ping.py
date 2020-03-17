# 2020.03.10-Homework-kamene ping
from kamene.all import *
from kamene.layers.inet import IP, ICMP
import logging

logging.getLogger('kamene.runtime').setLevel(logging.ERROR)


def qytang_ping(ip):
    ping_pkt = IP(dst=ip) / ICMP()
    ping_result = sr1(ping_pkt, timeout=2, verbose=False)

    if ping_result:
        return ip, 1
    else:
        return ip, 0


if __name__ == '__main__':
    result = qytang_ping('192.168.200.3')  # Linux VM， ping自己的ip地址就不通，shell是可以通的，不知道是为啥？？？
    if result[1]:
        print(result[0], '通')
    else:
        print(result[0], '不通')
