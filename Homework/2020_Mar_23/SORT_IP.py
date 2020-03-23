#!/usr/bin/env python3
# _*_ coding=utf-8 _*_

# 2020.03.23-Homework--SORT IP

from socket import inet_aton
import struct
import ipaddress

IP_LIST = ['172.16.12.123',
           '172.16.12.3',
           '172.16.12.234',
           '172.16.12.12',
           '172.16.12.23',
           ]


def sort_ip(ips):
    # inet_aton(ip) 转换IP到直接字符串
    # >>> inet_aton("172.16.1.1")
    # b'\xac\x10\x01\x01'
    # 了解struct https://docs.python.org/2/library/struct.html
    # struct.unpack("!L", inet_aton(ip))[0] 把直接字符串转换为整数
    # >>> struct.unpack("!L", inet_aton("172.16.1.1"))
    # (2886729985,)
    # >>> struct.unpack("!L", inet_aton("172.16.1.1"))[0]
    # 2886729985
    # 根据整数排序,然后返回排序后的ips列表
    # return sorted(ips, key=lambda ip: struct.unpack("!L", inet_aton(ip))[0])
    return sorted(ips, key=lambda ip: ipaddress.ip_address(ip))


if __name__ == "__main__":
    print(sort_ip(IP_LIST))
