#!/usr/bin/env python3
# _*_ coding=utf-8 _*_

# 2020.04.07-Homework--write info to mongo db, search last 2 minutes record, and show in matplot line chart.

from pysnmp.hlapi import *
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pymongo import *
import numpy as np
import pprint
from datetime import datetime, timedelta
from matplotlib import pyplot as plt

client = MongoClient('mongodb://qytangadmin:Cisc0123@192.168.200.135:27017/qytang')

db = client['qytang']


# see video copy teacher's code.
def get_all_info(ip, ro):
    # 接口名称
    if_name_list = [x[1] for x in snmpv2_getbulk(ip, ro, "1.3.6.1.2.1.2.2.1.2", count=25, port=161)]

    # 接口速率
    if_speed_list = [x[1] for x in snmpv2_getbulk(ip, ro, "1.3.6.1.2.1.2.2.1.5", port=161)]

    # 进接口字节数
    if_in_bytes_list = [x[1] for x in snmpv2_getbulk(ip, ro, "1.3.6.1.2.1.2.2.1.10", port=161)]

    # 出接口字节数
    if_out_bytes_list = [x[1] for x in snmpv2_getbulk(ip, ro, "1.3.6.1.2.1.2.2.1.16", port=161)]

    name_speed_in_out_list = zip(if_name_list, if_speed_list, if_in_bytes_list, if_out_bytes_list)

    all_info_dict = {}
    if_name_list = []

    for x in name_speed_in_out_list:
        if 'Ethernet' in x[0]:
            all_info_dict[x[0] + '_' + 'speed'] = x[1]
            all_info_dict[x[0] + '_' + 'in_bytes'] = int(x[2])
            all_info_dict[x[0] + '_' + 'out_bytes'] = int(x[3])
            if_name_list.append(x[0])
    all_info_dict.update({'if_name_list': if_name_list})

    # cpmCPUTotal5sec
    cpu_5s = int(snmpv2_get(ip, ro, '1.3.6.1.4.1.9.9.109.1.1.1.1.3.7', port=161)[1])
    # cpmCPUMemoryUsed
    mem_u = int(snmpv2_get(ip, ro, '1.3.6.1.4.1.9.9.109.1.1.1.1.12.7', port=161)[1])
    # cpmCPUMemoryFree
    mem_f = int(snmpv2_get(ip, ro,  '1.3.6.1.4.1.9.9.109.1.1.1.1.13.7', port=161)[1])

    all_info_dict['ip'] = ip
    all_info_dict['cpu_5s'] = cpu_5s
    all_info_dict['mem_u'] = mem_u
    all_info_dict['mem_f'] = mem_f
    all_info_dict['record_time'] = datetime.now()

    return all_info_dict


def write_info_to_mongodb(device_info_dict):
    # 写入单条数据
    db.deviceinfo.insert_one(device_info_dict)

    # 查看并打印deviceinfo中的所有数据
    for obj in db.deviceinfo.find():
        pprint.pprint(obj, indent=4)


def search_info_from_mongodb(ifname, direction, last_mins):
    if_bytes_list = []
    record_time_list = []
    for obj in db.deviceinfo.find({'record_time': {'$gte': datetime.now() - timedelta(minutes=last_mins)}}):
        if_bytes_list.append(obj[ifname + '_' + direction + '_bytes'])
        record_time_list.append(obj['record_time'])

    # numpy的diff计算列表的差值
    # np.diff([x for x in range(5)])
    # array([1, 1, 1, 1])
    diff_if_bytes_list = list(np.diff(if_bytes_list))

    # 计算两次时间对象的秒数的差值
    diff_record_time_list = [x.seconds for x in np.diff(record_time_list)]

    # 计算速率
    # * 8 得到bit数
    # /1000 计算kb
    # / x[1] 计算kbps
    # round(x, 2) 保留两位小数
    # zip把字节差列表 和 时间列表 压在一起
    speed_list = list(map(lambda x: round(((x[0] * 8) / (1000 * x[1])), 2), zip(diff_if_bytes_list, diff_record_time_list)))
    record_time_list = record_time_list[1:]
    return record_time_list, speed_list


def mat_line(record_time_list, speed_list):
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
    # ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%d%%'))
    ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%d'))

    # 控制Y轴的取值范围
    # ax.set_ylim(0, 100)
    ax.set_ylim(auto=True)

    # 添加主题和注释
    plt.title('路由器GigabitEthernet3接口，in向，2分钟速率')
    plt.xlabel('采集时间')
    plt.ylabel('速率kbps')

    fig.autofmt_xdate()  # 当x轴太拥挤的时候可以让他自适应

    # 实线红色
    if record_time_list:
        ax.plot(record_time_list, speed_list, linestyle='solid', color='r', label='R1')
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


def delete_all():
    db.deviceinfo.remove()


def snmpv2_get(ip, community, oid, port=161):
    # varBinds是列表，列表中的每个元素的类型是ObjectType（该类型的对象表示MIB variable）
    error_indication, error_status, error_index, var_binds = next(
        getCmd(SnmpEngine(),
               CommunityData(community),  # 配置community
               UdpTransportTarget((ip, port)),  # 配置目的地址和端口号
               ContextData(),
               ObjectType(ObjectIdentity(oid))  # 读取的OID
               )
    )
    # 错误处理
    if error_indication:
        print(error_indication)
    elif error_status:
        print('%s at %s' % (
            error_status,
            error_index and var_binds[int(error_index) - 1][0] or '?'
        )
              )
    # 如果返回结果有多行,需要拼接后返回
    result = ""

    for varBind in var_binds:

        result = result + varBind.prettyPrint() # 返回结果！

    return result.split("=")[0].strip(), result.split("=")[1].strip()


def snmpv2_getbulk(ip, community, oid, count=25, port=161):
    cmd_gen = cmdgen.CommandGenerator()

    error_indication, error_status, error_index, var_bind_table = cmd_gen.bulkCmd(
        cmdgen.CommunityData(community),  # 配置community
        cmdgen.UdpTransportTarget((ip, port)),  # 配置IP地址和端口号
        0, count,  # 0为non-repeaters 和  25为max-repetitions(一个数据包中最多25个条目，和显示无关)
        oid,  # OID
    )

    # 错误处理
    if error_indication:
        print(error_indication)
    elif error_status:
        print(error_status)

    result = []
    # varBindTable是个list，元素的个数可能有好多个。它的元素也是list，这个list里的元素是ObjectType，个数只有1个。
    for var_bind_table_row in var_bind_table:
        for item in var_bind_table_row:
            result.append((item.prettyPrint().split("=")[0].strip(), item.prettyPrint().split("=")[1].strip()))
    return result


if __name__ == '__main__':
    write_info_to_mongodb(get_all_info('192.168.200.101', 'tcpipro'))
    search_info_from_mongodb('GigabitEthernet3', 'in', 2)
    mat_line(search_info_from_mongodb('GigabitEthernet3', 'in', 2)[0], search_info_from_mongodb('GigabitEthernet3', 'in', 2)[1])
    # delete_all()

    # ###############################################################################################
    # temp = get_all_info('192.168.200.101', 'tcpipro')
    # print(temp)

    # # cpmCPUTotal5sec
    # print(snmpv2_get("192.168.200.101", "tcpipro", "1.3.6.1.4.1.9.9.109.1.1.1.1.3.7", port=161)[1])
    # # cpmCPUMemoryUsed
    # print(snmpv2_get("192.168.200.101", "tcpipro", "1.3.6.1.4.1.9.9.109.1.1.1.1.12.7", port=161)[1])
    # # cpmCPUMemoryFree
    # print(snmpv2_get("192.168.200.101", "tcpipro", "1.3.6.1.4.1.9.9.109.1.1.1.1.13.7", port=161)[1])
    #
    # # 虽然count=25,但是脚本会自动过滤只显示主ID内的内容
    # print(snmpv2_getbulk("192.168.200.101", "tcpipro", "1.3.6.1.2.1.2.2.1.2", count=25, port=161)[1])
    #
    # for x in snmpv2_getbulk("192.168.200.101", "tcpipro", "1.3.6.1.2.1.2.2.1.2", count=25, port=161):
    #     print(x)
    # # 接口速率1.3.6.1.2.1.2.2.1.5
    # print(snmpv2_getbulk("192.168.200.101", "tcpipro", "1.3.6.1.2.1.2.2.1.5", port=161))
    #
    # # 进接口字节数
    # print(snmpv2_getbulk("192.168.200.101", "tcpipro", "1.3.6.1.2.1.2.2.1.10", port=161))
    #
    # # 出接口字节数
    # print(snmpv2_getbulk("192.168.200.101", "tcpipro", "1.3.6.1.2.1.2.2.1.16", port=161))
