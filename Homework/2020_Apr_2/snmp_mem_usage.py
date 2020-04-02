#!/usr/bin/env python3
# _*_ coding=utf-8 _*_

# 2020.04.02-Homework--snmp mem usage

import time
import datetime
import pg8000
from pysnmp.hlapi import *
from matplotlib import pyplot as plt


plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文
plt.rcParams['font.family'] = 'sans-serif'


def snmpv2_get(ip, community, oid, port=161):
    errorIndication, errorStatus, errorindex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(community),
               UdpTransportTarget((ip, port)),
               ContextData(),
               ObjectType(ObjectIdentity(oid))
               )
    )
    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (
            errorStatus,
            errorindex and varBinds[int(errorindex) - 1][0] or '?'
        )
              )
    result = ''
    for varBind in varBinds:
        result = result + varBind.prettyPrint()
    return result.split("=")[0].strip(), result.split("=")[1].strip()


def write_memusage_todb(ip, community, seconds):
    conn = pg8000.connect(host='192.168.200.136', user='shudidbuser', password='shudidbpassword', database='shudidb')
    cursor = conn.cursor()
    cursor.execute("create table if not exists routerdb_mem(id SERIAL PRIMARY KEY, create_time timestamp default current_timestamp, "
                   "mem_percent int)")

    oid_mem_used = '1.3.6.1.4.1.9.9.109.1.1.1.1.12.7'
    oid_mem_free = '1.3.6.1.4.1.9.9.109.1.1.1.1.13.7'

    while seconds > 0:
        mem_used = snmpv2_get(ip, community, oid_mem_used, port=161)[1]
        mem_free = snmpv2_get(ip, community, oid_mem_free, port=161)[1]
        mem_percent = int(mem_used) / (int(mem_used) + int(mem_free)) * 100
        cursor.execute("insert into routerdb_mem(mem_percent) values (%d)" % mem_percent)
        # 每五秒采集一次数据
        time.sleep(5)
        seconds -= 5
        # 提交数据到数据库
        conn.commit()


def get_mem_usage_list():
    time_list = []
    mem_usage_list = []
    conn = pg8000.connect(host='192.168.200.136', user='shudidbuser', password='shudidbpassword', database='shudidb')
    cursor = conn.cursor()
    cursor.execute("select * from routerdb_mem where create_time >= current_timestamp - interval '1 min'")
    yourresults = cursor.fetchall()
    if yourresults:
        for x, y, z in yourresults:
            time_list.append(y)
            mem_usage_list.append(z)
    else:
        time_list.append(datetime.datetime.now())
        mem_usage_list.append(0)

    return time_list, mem_usage_list


def mat_line(time_list, cpu_usage_list):
    # 调节图形大小，宽，高
    fig = plt.figure(figsize=(6, 6))
    # 一共一行, 每行一图, 第一图
    ax = fig.add_subplot(111)

    # 处理X轴时间格式
    import matplotlib.dates as mdate
    # ax.xaxis.set_major_formatter(mdate.DateFormatter('%Y-%m-%d %H:%M:%S')) # 设置时间标签显示格式
    ax.xaxis.set_major_formatter(mdate.DateFormatter('%H:%M'))  # 设置时间标签显示格式

    # 处理Y轴百分比格式
    import matplotlib.ticker as mtick
    ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%d%%'))

    # 控制Y轴的取值范围
    ax.set_ylim(0, 100)

    # 添加主题和注释
    plt.title('路由器MEM利用率')
    plt.xlabel('采集时间')
    plt.ylabel('MEM利用率')

    fig.autofmt_xdate()  # 当x轴太拥挤的时候可以让他自适应

    # 实线红色
    if time_list:
        ax.plot(time_list, cpu_usage_list, linestyle='solid', color='r', label='MEM利用率')
        # 虚线黑色
        # ax.plot(x, y, linestyle='dashed', color='b', label='R1')

        # 如果你有两套数据,完全可以在一幅图中绘制双线
        # ax.plot(x2, y2, linestyle='dashed', color='b', label='R2')

        # 设置说明的位置
        ax.legend(loc='upper left')

        # 保存到图片
        plt.savefig('result4.png')
        # 绘制图形
        plt.show()


if __name__ == '__main__':
    # write_memusage_todb("192.168.200.101", "tcpipro", 60)
    get_mem_usage_list()
    mat_line(get_mem_usage_list()[0], get_mem_usage_list()[1])
