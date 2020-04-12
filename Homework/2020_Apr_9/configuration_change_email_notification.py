#!/usr/bin/env python3
# _*_ coding=utf-8 _*_

# 2020.04.09-Homework--configuration change email notification

import datetime
import time
import pg8000
import paramiko
import hashlib
import re
from difflib import Differ
import smtplib, email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText


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
    cmd = 'show run'
    run_config_raw = qytang_ssh(ip, username, password, cmd=cmd)
    split_result = re.split(r'\r\nhostname \S+\r\n', run_config_raw)
    run_config = run_config_raw.replace(split_result[0], '').strip()

    # 计算获取配置的MD5值
    m = hashlib.md5()
    m.update(run_config.encode())
    md5_value = m.hexdigest()

    return ip, run_config, md5_value


def diff_txt(txt1, txt2):
    txt1_list = txt1.split('\n')
    txt2_list = txt2.split('\n')
    result = Differ().compare(txt1_list, txt2_list)
    return_result = '\n'.join(list(result))
    return return_result


def create_config_md5_table():
    conn = pg8000.connect(host='192.168.200.136', user='shudidbuser', password='shudidbpassword', database='shudidb')
    cursor = conn.cursor()
    # 创建数据库
    cursor.execute("create table if not exists config_md5 (id SERIAL PRIMARY KEY, ip varchar(40), config varchar(99999), "
                   "md5_config varchar(9999), create_time timestamp default current_timestamp)")

    # cursor.execute("create table config_md5 (ip varchar(40), config varchar(99999), md5 varchar(999))")
    conn.commit()


def write_config_md5_to_db():
    conn = pg8000.connect(host='192.168.200.136', user='shudidbuser', password='shudidbpassword', database='shudidb')
    cursor = conn.cursor()
    # 逐个迭代设备，写入数据库！
    for device in device_list:
        config_and_md5 = get_config_md5(device, username, password)
        # print(config_and_md5[1])
        # print(type(config_and_md5[1]))
        cursor.execute("select * from config_md5 where ip='{0}'".format(device))
        md5_results = cursor.fetchall()
        # print(md5_results)
        # print(type(md5_results[-1][0]))
        if not md5_results:
            # 如果设备的数据库条目不存在，就写入
            cursor.execute("insert into config_md5(ip, config, md5_config) values ('%s', '%s', '%s')" % (device, config_and_md5[1],
                                                                                                        config_and_md5[2]))
            conn.commit()
        else:
            # 如果之前备份的MD5值与当前获取的MD5值不匹配！就更新条目
            if config_and_md5[1] != md5_results[0][2]:
                cursor.execute("update config_md5 set config='{0}', md5_config='{1}', create_time='{2}' where ip='{3}'".format(
                    config_and_md5[1], config_and_md5[2],
                    datetime.datetime.now(), device))
                compare_two_config_changed_sendmail(md5_results[0][2], config_and_md5[1])
                conn.commit()
            else:  # 如果之前备份的MD5值与当前获取的MD5值匹配！就跳过
                continue

    # cursor.execute("select * from config_md5")
    # all_result = cursor.fetchall()
    # # 打印查看IP和MD5值
    # for x in all_result:
    #     print(x[0], x[2])

    conn.close()


def get_last_config_from_db():
    conn = pg8000.connect(host='192.168.200.136', user='shudidbuser', password='shudidbpassword', database='shudidb')
    cursor = conn.cursor()
    cursor.execute("select config from config_md5 order by id desc limit 1")
    result = cursor.fetchall()
    return result[0][0]


def compare_two_config_changed_sendmail(result1, result2):
    # write_config_md5_to_db()
    # result1 = get_last_config_from_db()
    # time.sleep(60)
    # write_config_md5_to_db()
    # result2 = get_last_config_from_db()
    # print(diff_txt(result1, result2))

    if result1 != result2:
        ip = device_list[0]
        mailserver = 'smtp.qq.com'
        mailusername = '578225736@qq.com'
        mailpassword = 'password of this account'  # 先隐藏，用时再修改成正确的
        From = '578225736@qq.com'
        Tos = '578225736@qq.com'
        Subj = '路由器' + ip + '配置变更'

        shudi_smtp_attachment(mailserver=mailserver, username=mailusername, password=mailpassword, From=From, To=Tos, Subj=Subj,
                              Main_Body=diff_txt(result1, result2))


def shudi_smtp_attachment(mailserver, username, password, From, To, Subj, Main_Body, files=None):
    Tos = To.split(';')
    Date = email.utils.formatdate()
    msg = MIMEMultipart()
    msg['Subject'] = Subj
    msg['From'] = From
    msg['To'] = To
    msg['Date'] = Date

    part = MIMEText(Main_Body)
    msg.attach(part)

    if files:
        for file in files:
            # MIMEXXX决定了什么类型 MIMEApplication为二进制文件
            # 添加二进制文件
            part = MIMEApplication(open(file, 'rb').read())
            # 添加头部信息, 说明此文件为附件,并且添加文件名
            part.add_header('Content-Disposition', 'attachment', filename=file)
            # 把这个部分内容添加到MIMEMultipart()中
            msg.attach(part)

    server = smtplib.SMTP_SSL(mailserver, 465)
    server.login(username, password)
    failed = server.sendmail(From, Tos, msg.as_string())
    server.quit()
    if failed:
        print('Failed recipients:', failed)
    else:
        print('邮件已经成功发出！')


if __name__ == '__main__':
    create_config_md5_table()
    write_config_md5_to_db()
    # compare_two_config_changed_sendmail()
