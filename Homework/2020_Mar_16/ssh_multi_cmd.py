#!/usr/bin/env python3
# _*_ coding=utf-8 _*_

# 2020.03.16-Homework-ssh multi commands

import paramiko
import time


def qytang_multicmd(ip, username, password, cmd_list, enable='Cisc0123', wait_time=2, verbose=True):
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, port=22, username=username, password=password, timeout=5, compress=False)
    chan = ssh.invoke_shell()
    time.sleep(1)
    login_mode = chan.recv(2048).decode()
    if '>' in login_mode:
        chan.send("enable\n".encode())
        time.sleep(1)
        en_password = enable + '\n'
        chan.send(en_password)
         
    for cmd in cmd_list:
        chan.send(b'\n')
        chan.send(cmd.encode())
        chan.send(b'\n')
        x = chan.recv(2048).decode()
        if verbose:
            print(x)
        time.sleep(wait_time)


if __name__ == '__main__':
    cmdlist = ['terminal length 0', 'show version', 'configure terminal', 'router ospf 1', 'network 1.1.1.1 0.0.0.0 area 0',
               'end'] # 最后要多加一个命令，才会显示出network那条命令，不知道为啥？？？
    # qytang_multicmd('192.168.200.101', 'test1', 'test1', cmdlist)        # level 1 user login
    # qytang_multicmd('192.168.200.101', 'admin', 'Cisc0123', cmdlist, verbose=False)     # level 15 user login, 并且不打印网络设备返回信息
    qytang_multicmd('192.168.200.101', 'admin', 'Cisc0123', cmdlist)     # level 15 user login