# 2020.03.13-Homework-monitor config diff

from paramiko_ssh import qytang_ssh
import hashlib
import time
import re


def qytang_get_config(ip, username='admin', password='Cisc0123'):
    try:
        device_config_raw = qytang_ssh(ip, username, password, cmd='show run')
        split_result = re.split(r'\r\nhostname \S+\r\n', device_config_raw)
        device_config = device_config_raw.replace(split_result[0], '').strip()
        return device_config
        # cmd = 'show running-config | begin hostname'  # 教主的re，是为了用正则表达式去获取这个命令的输出内容吗？
        # config = qytang_ssh(ip, username, password, cmd=cmd)
        # return config

    except Exception:
        return


def qytang_check_diff(ip, username='admin', password='Cisc0123'):
    # while True:
    #     before_config = qytang_get_config(ip, username, password)
    #     m = hashlib.md5()
    #     m.update(before_config.encode())
    #     before_md5 = m.hexdigest()
    #
    #     time.sleep(5)
    #
    #     new_config = qytang_get_config(ip, username, password)
    #     m = hashlib.md5()
    #     m.update(new_config.encode())
    #     new_md5 = m.hexdigest()
    #
    #     if before_md5 == new_md5:
    #         print(before_md5)
    #         continue
    #     else:
    #         print(new_md5)
    #         print('MD5 value changed')
    #         break

    # 优化代码，之前的方法是每循环一次，先获取一次配置，间隔5秒后，再获取一次配置，作比较。现在的方法是每次循环只读取一次配置。
    before_md5 = ''
    while True:
        if before_md5 == '':
            before_config = qytang_get_config(ip, username, password)
            m = hashlib.md5()
            m.update(before_config.encode())
            before_md5 = m.hexdigest()
        else:
            new_config = qytang_get_config(ip, username, password)
            m = hashlib.md5()
            m.update(new_config.encode())
            new_md5 = m.hexdigest()
            if before_md5 == new_md5:
                print(before_md5)
            else:
                print(new_md5)
                print('MD5 value changed')
                break
        time.sleep(5)


if __name__ == '__main__':
    # print(qytang_get_config('192.168.200.101', 'admin', 'Cisc0123'))
    qytang_check_diff('192.168.200.101', username='admin', password='Cisc0123')

