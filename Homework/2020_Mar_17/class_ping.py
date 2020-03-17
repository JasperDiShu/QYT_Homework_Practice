#!/usr/bin/env python3
# _*_ coding=utf-8 _*_

# 2020.03.17-Homework-class ping

from kamene.all import *
from kamene.layers.inet import IP, ICMP

logging.getLogger("kamene.runtime").setLevel(logging.ERROR)


class QYTPING:
    def __init__(self, ip):
        self.ip = ip
        self.srcip = None
        self.length = 100
        self.pkt = IP(dst=self.ip, src=self.srcip) / ICMP() / (b'v' * self.length)

    def one(self):
        result = sr1(self.pkt, timeout=1, verbose=False)
        if result:
            print(self.ip, '可达！')
        else:
            print(self.ip, '不可达！')

    def ping(self):
        self.pkt = IP(dst=self.ip, src=self.srcip) / ICMP() / (b'v' * self.length)  #
        # 在ping的方法中，如果不加上这句让src获取到新赋的值，在调用这个ping时，src始终用的还是构造方法里的none，不知道为什么会这样？
        for i in range(5):
            result = sr1(self.pkt, timeout=1, verbose=False)
            if result:
                print('!', end='', flush=True)
            else:
                print('.', end='', flush=True)
        print()

    def __str__(self):
        if not self.srcip:
            return f'<{self.__class__.__name__} => dstip: {self.ip} size: {self.length}>'
        else:
            return f'<{self.__class__.__name__} => srcip: {self.srcip} => dstip: {self.ip} size: {self.length}>'


class NewPing(QYTPING):
    def ping(self):
        self.pkt = IP(dst=self.ip, src=self.srcip) / ICMP() / (b'v' * self.length)
        for i in range(5):
            result = sr1(self.pkt, timeout=1, verbose=False)
            if result:
                print('+', end='', flush=True)
            else:
                print('?', end='', flush=True)
        print()

    def __str__(self):
        if not self.srcip:
            return f'<{self.__class__.__name__} => dstip: {self.ip} size: {self.length}>'
        else:
            return f'<{self.__class__.__name__} => srcip: {self.srcip} => dstip: {self.ip} size: {self.length}>'


if __name__ == '__main__':
    ping = QYTPING('192.168.200.101')
    total_len = 70

    def print_new(word, s='-'):
        print('{0}{1}{2}'.format(s * int((70 - len(word))/2), word, s * int((70 - len(word))/2)))
    print_new('print class')
    print(ping)  # 打印类
    print_new('ping one for sure reachable')
    ping.one()   # Ping一个包判断可达性
    print_new('ping five')
    ping.ping()  # 模拟正常ping程序ping五个包，'！'表示通，'.'表示不通
    print_new('set payload length')
    ping.length = 200  # 设置负载长度
    print(ping)  # 打印类
    ping.ping()  # 使用修改长度的包进行ping测试
    print_new('set ping src ip address')
    ping.srcip = '192.168.1.123'  # 修改源IP地址
    print(ping)  # 打印类
    ping.ping()  # 使用修改长度又修改源的包进行ping测试
    print_new('new class NewPing', '=')
    newping = NewPing('192.168.200.101')  # 使用新的类NewPing(通过继承QYTPING类产生)产生实例！
    newping.length = 300
    print(newping)  # 打印类
    newping.ping()  # NewPing类自定义过ping()这个方法， '+'表示通， '?'表示不通
