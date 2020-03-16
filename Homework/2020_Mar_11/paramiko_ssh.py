# 2020.03.11-Homework-paramiko ssh and ssh get route gateway

import paramiko
import os
import re


def qytang_ssh(ip, username, password, port=22, cmd='ls'):
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, port, username, password, timeout=5, compress=True)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    x = stdout.read().decode()
    return x


def ssh_get_route(ip, username, password):
    qytang_ssh(ip, username, password)
    route_n_result = os.popen('route -n').read()
    result_list = route_n_result.split('\n')
    for result in result_list:
        output = re.match('(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})\s+(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})\s+(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,'
                          '3})\s+(\w*)\s+(\d{1,4})\s+(\d{1,3})\s+(\d{1,3})\s+(\w*)', result)
        if output is not None:
            gateway_output = output.groups()[1]
            if '0.0.0.0' not in gateway_output:
                gateway = gateway_output
                return  gateway


if __name__ == '__main__':
    print(qytang_ssh('192.168.200.130', 'root', 'root'))
    print(qytang_ssh('192.168.200.130', 'root', 'root', cmd='pwd'))
    print('网关为：')
    print(ssh_get_route('192.168.200.130', 'root', 'root'))