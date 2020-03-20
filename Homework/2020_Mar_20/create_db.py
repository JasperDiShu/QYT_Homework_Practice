#!/usr/bin/env python3
# _*_ coding=utf-8 _*_

# 2020.03.20-Homework--create db

import sqlite3
import os

if os.path.exists('qytangconfig.sqlite'):
    os.remove('qytangconfig.sqlite')

conn = sqlite3.connect('qytangconfig.sqlite')
cursor = conn.cursor()
cursor.execute("create table config_md5 (ip varchar(40), config varchar(99999), md5 config varchar(999))")


if __name__ == '__main__':
    pass
