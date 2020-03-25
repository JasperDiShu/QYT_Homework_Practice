#!/usr/bin/env python3
# _*_ coding=utf-8 _*_

# 2020.03.25-Homework--UDP Client

import hashlib
import pickle
import socket
import struct


def udp_send_data(ip, port, data_list):
    address = (ip, port)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    version = 1
    pkt_type = 1
    seq_id = 1
    for x in data_list:
        # ---header设计---
        # 2 字节 版本 1
        # 2 字节 类型 1 为请求 2 为响应(由于是UDP单向流量!所有此次试验只有请求)
        # 4 字节 ID号
        # 4 字节 长度

        # ---变长数据部分---
        # 使用pickle转换数据

        # ---HASH校验---
        # 16 字节 MD5值
        send_data = pickle.dumps(x)
        length = len(send_data)
        header = struct.pack('!hhii', version, pkt_type, seq_id, length)
        m = hashlib.md5()
        m.update(str(header).encode())
        md5_value = m.hexdigest().encode()
        data = struct.pack('!hhii16s228s', version, pkt_type, seq_id, length, md5_value, send_data)
        # !hhii16s228s的228是用（2048-28*8）/ 8
        # 得到的，不知道这样是否是正确的？？？
        s.sendto(data, address)
        seq_id += 1
    s.close()


if __name__ == '__main__':
    user_data = ['乾颐堂', [1, 'qytang', 3], {'qytang': 1, 'test': 3}]
    udp_send_data('192.168.200.130', 6666, user_data)
