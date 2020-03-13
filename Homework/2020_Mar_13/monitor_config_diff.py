# 2020.03.13-Homework-monitor config diff

from paramiko_ssh import qytang_ssh
import hashlib
import time


def qytang_get_config(ip, username='admin', password='Cisc0123'):
    try:
        cmd = 'show running-config | begin hostname'
        config = qytang_ssh(ip, username, password, cmd=cmd)
        return config
    except Exception:
        return


def qytang_check_diff(ip, username='admin', password='Cisc0123'):
    while True:
        before_config = qytang_get_config(ip, username, password)
        m = hashlib.md5()
        m.update(before_config.encode())
        before_md5 = m.hexdigest()

        time.sleep(5)

        new_config = qytang_get_config(ip, username, password)
        m = hashlib.md5()
        m.update(new_config.encode())
        new_md5 = m.hexdigest()

        if before_md5 == new_md5:
            print(before_md5)
            continue
        else:
            print(new_md5)
            print('MD5 value changed')
            break


if __name__ == '__main__':
    # print(qytang_get_config('192.168.200.101', 'admin', 'Cisc0123'))
    qytang_check_diff('192.168.200.101', username='admin', password='Cisc0123')

