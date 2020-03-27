#!/usr/bin/env python3
# _*_ coding=utf-8 _*_

# 2020.03.27-Homework--Netflow Matplotlib

import re
import paramiko
from matplotlib import pyplot as plt
import matplotlib
print(matplotlib.matplotlib_fname())
plt.rcParams['font.sans-serif'] = ['SimHei'] # 设置中文
plt.rcParams['font.family'] = 'sans-serif'


def qytang_ssh(ip, username, password, port=22, cmd='pwd'):
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, port, username, password, timeout=5, compress=True)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    x = stdout.read().decode()
    return x


def get_netflow_counters(ip, username, password):
    counters = [0, 0]
    cmd = 'show flow monitor name qytang-monitor cache format table'
    cmd_output = qytang_ssh(ip, username, password, cmd=cmd)
    line_result = cmd_output.split('\n')
    for result in line_result:
        if 'ssh' in result:
            ssh_counter = re.findall(r'\d{1,5}', result)
            counters[0] = int(ssh_counter[0])
        elif 'telnet' in result:
            telnet_counter = re.findall(r'\d{1,5}', result)
            counters[1] = int(telnet_counter[0])
        else:
            continue
    print(counters)
    return counters


def mat_bing(size_list, name_list):
    # 调节图形大小，宽，高
    plt.figure(figsize=(6, 6))

    # 将某部分爆炸出来，使用括号，将第一块分隔出来，数值的大小是分割出来的与其他两块的间隙

    patches, label_text, percent_text = plt.pie(size_list,
                                                # explode=explode,
                                                labels=name_list,
                                                labeldistance=1.1,
                                                autopct='%3.1f%%',
                                                shadow=False,
                                                startangle=90,
                                                pctdistance=0.6)

    for l in label_text:
        l.set_size = 30
    for p in percent_text:
        p.set_size = 20

    plt.axis('equal')
    plt.legend(loc=2)  # https://www.cnblogs.com/IvyWong/p/9916791.html     调整matplotlib的图例legend的位置
    plt.show()


if __name__ == '__main__':
    counters = get_netflow_counters('192.168.200.101', 'admin', 'Cisc0123')
    protocols = ['ssh', 'telnet']
    mat_bing(counters, protocols)
