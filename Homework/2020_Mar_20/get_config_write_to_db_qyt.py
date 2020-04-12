#!/usr/bin/env python3
# _*_ coding=utf-8 _*_

# 2020.03.20-Homework--get running config and write md5 to db---jiaozhu solution

import paramiko
import hashlib
import re
import sqlite3

# 设备清单
device_list = ['192.168.200.101']
# 用户名和密码
username = 'admin'
password = 'Cisc0123'


def qytang_ssh(ip, username, password, port=22, cmd='pwd'):
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, port, username, password, timeout=5, compress=True)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    x = stdout.read().decode()
    return x


def get_config_md5(ip, username, password):
    try:
        cmd = 'show run'
        run_config_raw = qytang_ssh(ip, username, password, cmd=cmd)
        split_result = re.split(r'\r\nhostname \S+\r\n', run_config_raw)
        run_config = run_config_raw.replace(split_result[0], '').strip()

        # 计算获取配置的MD5值
        m = hashlib.md5()
        m.update(run_config.encode())
        md5_value = m.hexdigest()
        return run_config, md5_value
    except Exception:
        return


def write_config_md5_to_db():
    conn = sqlite3.connect('qytangconfig.sqlite')
    cursor = conn.cursor()
    # 逐个迭代设备，写入数据库！
    for device in device_list:
        config_and_md5 = get_config_md5(device, username, password)
        # print(config_and_md5[1])
        # print(type(config_and_md5[1]))
        cursor.execute("select * from config_md5 where ip=?", (device, ))
        md5_results = cursor.fetchall()
        # print(md5_results)
        # print(type(md5_results[-1][0]))
        if not md5_results:
            # 如果设备的数据库条目不存在，就写入
            cursor.execute("insert into config_md5(ip, config, md5) values (?, ?, ?)", (device, config_and_md5[0], config_and_md5[1]))
            conn.commit()
        else:
            # 如果之前备份的MD5值与当前获取的MD5值不匹配！就更新条目
            if config_and_md5[1] != md5_results[0][2]:
                cursor.execute("update config_md5 set config=?, md5=? where ip=?", (config_and_md5[0], config_and_md5[1], device))
                conn.commit()
            else:  # 如果之前备份的MD5值与当前获取的MD5值匹配！就跳过
                continue

    cursor.execute("select * from config_md5")
    all_result = cursor.fetchall()
    # 打印查看IP和MD5值
    for x in all_result:
        print(x[0], x[2])

    conn.close()


def delete_all_from_db():
    conn = sqlite3.connect('qytangconfig.sqlite')
    cursor = conn.cursor()
    cursor.execute("delete from config_md5")
    conn.commit()
    conn.close()


if __name__ == '__main__':
    # print(get_config_md5('192.168.200.101', username, password))
    write_config_md5_to_db()
    # delete_all_from_db()

