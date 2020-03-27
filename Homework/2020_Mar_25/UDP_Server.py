#!/usr/bin/env python3
# _*_ coding=utf-8 _*_

# 2020.03.25-Homework--UDP Server
import hashlib
import pickle
import struct
import sys
import socket

address = ('192.168.200.130', 6666)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(address)

print('UDP服务器就绪！等待客户数据！')
while True:
    try:
        # 接收UDP套接字的数据，2048为接收的最大数据量，多的直接丢弃！
        # 不推荐使用UDP传大量数据
        recv_source_data = s.recvfrom(2048)

        # My solution
        # get_result, addr = recv_source_data
        # values = struct.unpack('!hhii16s228s', get_result)
        # # !hhii16s228s的228是用（2048-28*8）/ 8
        # # 得到的，不知道这样是否是正确的？？？
        #
        # version = values[0]
        # pkt_type = values[1]
        # seq_id = values[2]
        # length = values[3]
        # md5_recv = values[4]
        # data = values[5]
        #
        # header = struct.pack('!hhii', version, pkt_type, seq_id, length)
        # m = hashlib.md5()
        # m.update(str(header).encode())
        # md5_value = m.hexdigest()[0:16]

        # Reference solution
        rdata, addr = recv_source_data
        header = rdata[:12]
        unpack_header = struct.unpack('>HHLL', header)
        version = unpack_header[0]
        pkt_type = unpack_header[1]
        seq_id = unpack_header[2]
        length = unpack_header[3]

        rdata = rdata[12:]
        data = rdata[:length]
        md5_recv = rdata[length:]

        m = hashlib.md5()
        m.update(header + data)
        md5_value = m.digest()

        # if md5_recv == md5_value.encode():
        if md5_recv == md5_value:
            print('=' * 80)
            print("{0:<30}:{1:<30}".format("数据来自于", str(addr)))
            print("{0:<30}:{1:<30}".format("数据序号为", seq_id))
            print("{0:<30}:{1:<30}".format("数据长度为", length))
            print("{0:<30}:{1:<30}".format("数据内容为", str(pickle.loads(data))))

    except KeyboardInterrupt:
        sys.exit()


if __name__ == '__main__':
    pass