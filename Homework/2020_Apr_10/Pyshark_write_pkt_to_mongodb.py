#!/usr/bin/env python3
# _*_ coding=utf-8 _*_

# 2020.04.10-Homework--Pyshark write packet to mongodb

import pyshark
import pprint
from pyshark_pcap_dir import pcap_data_dir
from pymongo import *
from matplotlib import pyplot as plt

client = MongoClient('mongodb://qytangadmin:Cisc0123@192.168.200.135:27017/qytang')

db = client['qytang']

# reference solution part code***
# *******************************


def write_pkt_mongodb(pkt):
    pkt_dict = {}
    for layer in pkt.__dict__.get('layers'):
        pkt_dict.update(layer.__dict__.get('_all_fields'))
    pkt_dict_final = {}
    for key, value in pkt_dict.items():
        pkt_dict_final[key.replace('.', '_')] = value
    print(pkt_dict_final)
    db.packetinfo.insert_one(pkt_dict_final)


def delete_all():
    db.packetinfo.remove()

# *******************************

# ####################最原始操作,信息过量#####################
# cap = pyshark.FileCapture(pcap_data_dir + 'dos.pcap')
#
# for pkt in cap:
#     pkt_dict = {}
#     for layer in pkt.__dict__.get('layers'):
#         pkt_dict.update(layer.__dict__.get('_all_fields'))
#
#     print(pkt_dict)
#
#     print(pkt.highest_layer)

# ####################传一个函数,对pkt进行处理#####################
# cap = pyshark.FileCapture(pcap_data_dir + 'dos.pcap', keep_packets=False)  # 读取pcap文件,数据包被读取后,不在内存中保存!节约内存!

# pkt_list = []

# 把函数应用到数据包
# cap.apply_on_packets(get_highest_layer_pkt_dict)


# The following part just for practice, not really useful value!!! ********************************
def get_info_from_mongodb():
    # 查看并打印packetinfo中的所有数据
    # for obj in db.packetinfo.find({}, {'_id': 0, 'ip_src': 1, 'ip_dst': 1, 'tcp_dstport': 1}):
    #     pprint.pprint(obj, indent=4)
        # print(obj.get('ip_src'), obj.get('ip_dst'), obj.get('tcp_dstport'))

    # count
    # count1 = db.packetinfo.find().count()
    # print(count1)

    # distinct
    # tmp = db.packetinfo.distinct('ip_src')
    # print(tmp)

    # 3 element to form tuple
    dos_dict = {}  # 最后的结果写入dos_dict,格式为{('196.21.5.12', '196.21.5.254', 5000): 36}!利用字典键值的唯一性
    result = db.packetinfo.find({}, {'_id': 0, 'ip_src': 1, 'ip_dst': 1, 'tcp_dstport': 1})
    for obj in result:
        try:
            if obj.get('ip_src') and obj.get('ip_dst') and obj.get('tcp_dstport'):
                conn = obj.get('ip_src'), obj.get('ip_dst'), obj.get('tcp_dstport')
                conn_counts = dos_dict.get(conn, 0)  # 判断是否有这个键值, 没有就返回0
                dos_dict[conn] = conn_counts + 1  # 在返回值的基础上加1
        except Exception:
            pass
    # print(dos_dict)

    return dos_dict


def mat_bar(result_dict):
    from matplotlib import pyplot as plt
    conn_list = []
    num_list = []
    for connection, num in result_dict.items():  # 提取字典内容并且打印
        if num > 5:
            conn_list.append(str(connection))
            num_list.append(num)
    conn_num_list = sorted(zip(conn_list, num_list), key=lambda x: x[1], reverse=True)
    conn_list = []
    num_list = []
    for c, n in conn_num_list:
        conn_list.append(c)
        num_list.append(n)
    conn_list = conn_list[:5]
    num_list = num_list[:5]
    conn_list_with_name = []
    for x in conn_list:
        src_ip = x.split(',')[0][2:-1]
        dst_ip = x.split(',')[1][1:-1]
        port = x.split(',')[2][1:-2]
        new_label = 'SRC:' + src_ip + ' DST:' + dst_ip + ' PORT:' + port
        conn_list_with_name.append(new_label)
    # print(conn_list_with_name)
    plt.barh(conn_list_with_name, num_list, height=0.5)

    # ##########################添加注释###################################
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文
    plt.title('连接会话数')  # 主题
    plt.xlabel('会话数')  # X轴注释
    plt.ylabel('源目地址 端口号 三元组')  # Y轴注释
    # ##########################添加注释###################################
    plt.show()
# End for the practice part ****************************************************


if __name__ == '__main__':
    cap = pyshark.FileCapture(pcap_data_dir + 'dos.pcap', keep_packets=False)
    cap.apply_on_packets(write_pkt_mongodb)

    # delete_all()
