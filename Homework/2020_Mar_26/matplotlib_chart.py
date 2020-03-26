#!/usr/bin/env python3
# _*_ coding=utf-8 _*_

# 2020.03.26-Homework--Matplotlib chart

from matplotlib import pyplot as plt
import matplotlib
print(matplotlib.matplotlib_fname())
plt.rcParams['font.sans-serif'] = ['SimHei'] # 设置中文
plt.rcParams['font.family'] = 'sans-serif'


def mat_bing(size_list, name_list):
    # 调节图形大小，宽，高
    plt.figure(figsize=(6, 6))

    # 将某部分爆炸出来，使用括号，将第一块分隔出来，数值的大小是分割出来的与其他两块的间隙

    patches, label_text, percent_text = plt.pie(size_list,
                                                # explode=explode,
                                                labels=name_list,
                                                labeldistance=1.1,
                                                autopct='%3.1f%%',
                                                shadow=False,
                                                startangle=90,
                                                pctdistance=0.6)

    for l in label_text:
        l.set_size = 30
    for p in percent_text:
        p.set_size = 20

    plt.axis('equal')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    counters = [30, 53, 12, 45]
    protocols = ['http协议', 'ftp协议', 'rdp协议', 'qq协议']
    mat_bing(counters, protocols)
