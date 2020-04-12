#!/usr/bin/env python3
# _*_ coding=utf-8 _*_

# 2020.04.10-Homework--Pyshark read info from mongodb

from pymongo import *
from mat_bar import mat_bar_mark


client = MongoClient('mongodb://qytangadmin:Cisc0123@192.168.200.135:27017/qytang')

db = client['qytang']

syn_pkt = db.packetinfo.find({'tcp_flags': '2'})

dos_dict = {}
for x in syn_pkt:
    conn = x.get('ip_src'), x.get('ip_dst'), x.get('tcp_dstport')
    counts = dos_dict.get(conn, 0)
    dos_dict[conn] = counts + 1

sorted_dict_key = sorted(dos_dict.keys(), key=lambda k: dos_dict[k], reverse=True)[:5]

sorted_dict_key_top5 = [f'SRC: {x[0]} DST: {x[1]} PORT: {x[2]}' for x in sorted_dict_key]

sorted_counts = [dos_dict[x] for x in sorted_dict_key]

mat_bar_mark(sorted_counts, sorted_dict_key_top5, '源目地址 端口号 三元组', '会话数', '连接会话数')


if __name__ == '__main__':
    pass
