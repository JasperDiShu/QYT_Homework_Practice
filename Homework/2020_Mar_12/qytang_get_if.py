# 2020.03.12-Homework-get if

from kamene_ping import qytang_ping
from paramiko_ssh import qytang_ssh
import re
import pprint


def qytang_get_if(*ips, username='admin', password='Cisc0123'):
    device_if_dict = {}
    for ip in ips:
        single_device_dict = {}  # put in the correct location.
        ping_result = qytang_ping(ip)
        if ping_result[1]:
            ssh_get_result = qytang_ssh(ip, username, password, cmd='show ip interface brief')
            items = ssh_get_result.split('\n')
            for item in items:
                re_result = re.match('(\w*)\s+(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})\s+(\w*)\s+(\w*)\s+(\w*)\s+(\w*)', item)
                if re_result:
                    if_name = re_result.groups()[0]
                    if_ip = re_result.groups()[1]
                    single_if_dict = {if_name: if_ip}
                    single_device_dict.update(single_if_dict)
        device_if_dict.update({ip: single_device_dict})
    return device_if_dict


if __name__ == '__main__':
    pprint.pprint(qytang_get_if('192.168.200.101', '192.168.200.102', '192.168.200.103', username='admin', password='Cisc0123'), indent=4)
