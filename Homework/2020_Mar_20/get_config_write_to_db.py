#!/usr/bin/env python3
# _*_ coding=utf-8 _*_

# 2020.03.20-Homework--get running config and write md5 to db

from Simple_SSH_Client import qytang_ssh
import hashlib
import re
import sqlite3

# 设备清单
device_list = ['192.168.200.101']
# 用户名和密码
username = 'admin'
password = 'Cisc0123'


def get_config_md5(ip, username, password):
    cmd = 'show run'
    run_config_raw = qytang_ssh(ip, username, password, cmd=cmd)
    split_result = re.split(r'\r\nhostname \S+\r\n', run_config_raw)
    run_config = run_config_raw.replace(split_result[0], '').strip()

    # 计算获取配置的MD5值
    m = hashlib.md5()
    m.update(run_config.encode())
    md5_value = m.hexdigest()

    return run_config, md5_value


def write_config_md5_to_db():
    conn = sqlite3.connect('qytangconfig.sqlite')
    cursor = conn.cursor()
    # 逐个迭代设备，写入数据库！
    for device in device_list:
        config_and_md5 = get_config_md5(device, username, password)
        # print(config_and_md5[1])
        # print(type(config_and_md5[1]))
        cursor.execute("select md5 from config_md5 where ip='{0}'".format(device))
        md5_results = cursor.fetchall()
        # print(md5_results)
        # print(type(md5_results[-1][0]))
        if not md5_results:
            # 如果设备的数据库条目不存在，就写入
            cursor.execute("insert into config_md5 values ('%s', '%s', '%s')" % (device, config_and_md5[0], config_and_md5[1]))
        else:
            # 如果之前备份的MD5值与当前获取的MD5值不匹配！就更新条目
            if config_and_md5[1] != md5_results[-1][0]:
                cursor.execute("insert into config_md5 values ('%s', '%s', '%s')" % (device, config_and_md5[0], config_and_md5[1]))
            else:  # 如果之前备份的MD5值与当前获取的MD5值匹配！就跳过
                continue

    cursor.execute("select * from config_md5")
    all_result = cursor.fetchall()
    # 打印查看IP和MD5值
    for x in all_result:
        print(x[0], x[2])

    conn.commit()


if __name__ == '__main__':
    # print(get_config_md5('192.168.200.101', username, password))
    write_config_md5_to_db()

