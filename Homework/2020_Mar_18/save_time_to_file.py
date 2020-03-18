#!/usr/bin/env python3
# _*_ coding=utf-8 _*_

# 2020.03.18-Homework--save time to file

import datetime

now = datetime.datetime.now()
now_str = now.strftime('%Y-%m-%d_%H-%M-%S')
five_days_ago = (datetime.datetime.now() - datetime.timedelta(days=5))
file_name = 'save_fivedayago_time_' + now_str + '.txt'
time_file = open(file_name, 'w')
time_file.write(str(five_days_ago))
time_file.close()


if __name__ == '__main__':
    pass