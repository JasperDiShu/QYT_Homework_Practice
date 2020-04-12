#!/usr/bin/env python3
# _*_ coding=utf-8 _*_

# 2020.04.08-Homework--TCP Socket Client

import json
from socket import *
import base64
import os


def Client_JSON(ip, port, obj):
    # 创建TCP Socket并连接
    sockobj = socket(AF_INET, SOCK_STREAM)
    sockobj.connect((ip, port))

    if 'exec_cmd' in obj:
        send_obj = obj
    elif 'upload_file' in obj:
        send_obj = obj
        file_name = send_obj.get('upload_file')
        with open(file_name, 'rb', 1024) as f:
            file_data = base64.b64encode(f.read())
        send_obj.update({'file-bit': file_data.decode()})
        # send_obj.update({'message': base64.b64encode(file_data)})
        # print('client sent data to server!')

    elif 'download_file' in obj:
        send_obj = obj

    # 把obj转换为JSON字节字符串
    send_message = json.dumps(send_obj).encode()
    # 读取1024字节长度的数据，准备发送数据分片
    send_message_fragment = send_message[:1024]
    # 剩余部分数据
    send_message = send_message[1024:]

    while send_message_fragment:
        sockobj.send(send_message_fragment)  # 发送数据分片（如果分片的话）
        send_message_fragment = send_message[:1024]
        send_message = send_message[1024:]

    received_message = b''  # 预定义接收信息变量
    received_message_fragment = sockobj.recv(1024)  # 读取接收到的信息，写入到接收到信息分片

    while received_message_fragment:
        received_message = received_message + received_message_fragment  # 把所有接收到信息分片重组装
        received_message_fragment = sockobj.recv(1024)

    return_data = json.loads(received_message.decode())

    if 'download_file' not in return_data.keys():
        print('收到确认数据：', return_data)
    else:
        print('收到确认数据：', return_data)
        # 应该考虑写入下载的文件名！但是由于实验室相同目录测试！所以使用了'download_file.py'
        data = return_data.get('file-bit')
        byte_data = base64.b64decode(data)
        new_file = open('download_file.py', 'wb')
        new_file.write(byte_data)
        new_file.close()
        print('下载文件{0}保存成功！'.format(obj.get('download_file')))
        sockobj.close()


if __name__ == '__main__':
    port = 6666
    exec_cmd = {'exec_cmd': 'pwd'}
    Client_JSON('192.168.200.130', port, exec_cmd)
    upload_file = {'upload_file': 'snmp_get.py'}
    Client_JSON('192.168.200.130', port, upload_file)
    download_file = {'download_file': 'snmp_get.py'}
    Client_JSON('192.168.200.130', port, download_file)
