#!/usr/bin/env python3
# _*_ coding=utf-8 _*_

# 2020.03.30-Homework--matplotlib bar

from matplotlib import pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文
plt.rcParams['font.family'] = 'sans-serif'
colorlist = ['r', 'b', 'g', 'y']


def mat_zhu(size_list, name_list):
    # 调节图形大小，宽，高
    plt.figure(figsize=(6, 6))

    # 横向柱状图
    # plt.barh(name_list, size_list, height=0.5, color=colorlist)

    # 竖向柱状图
    plt.bar(name_list, size_list, width=0.5, color=colorlist)

    # 添加主题和注释
    plt.title('协议与带宽分布')  # 主题
    plt.xlabel('带宽（M/s）')  # X轴注释
    plt.ylabel('协议')  # Y轴注释

    # 保存到图片
    plt.savefig('result1.png')
    # 绘制图形
    plt.show()


if __name__ == '__main__':
    counters = [30, 53, 12, 45]
    protocols = ['http协议', 'ftp协议', 'rdp协议', 'qq协议']
    mat_zhu(counters, protocols)
