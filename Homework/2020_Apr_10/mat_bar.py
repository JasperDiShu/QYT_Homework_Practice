#!/usr/bin/env python3
# _*_ coding=utf-8 _*_

# 2020.04.10-Homework--Pyshark matplotlib related functions

from matplotlib import pyplot as plt


def mat_bar_mark(size_list, name_list, x_label, y_label, title):
    # 调节图形大小，宽，高
    fig = plt.figure(figsize=(6, 6))
    # 一共一行，每行一图，第一图
    ax = fig.add_subplot(111)

    fig.autofmt_xdate()  # 当x轴太拥挤的时候可以让它自适应

    ax.bar(name_list, size_list, width=0.5)

# ##########################添加注释###################################
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文
    plt.title(title)  # 主题
    plt.xlabel(x_label)  # X轴注释
    plt.ylabel(y_label)  # Y轴注释
    # ##########################添加注释###################################

    plt.show()




if __name__ == '__main__':
    pass