# 2020.03.02-Homework-re_ip

import re

str1 = 'Port-channel1.189   192.168.189.254 YES    CONFIG  up'

result = re.match('(\w.*\d*)\s+(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})\s+(\w*)\s+(\w*)\s+(\w*)', str1).groups() # use groups() not group() !!!

print('-'*80)
print('{0:<7s} : {1:<s}'.format('接口', result[0]))
print('{0:<7s} : {1:<s}'.format('IP地址', result[1]))
print('{0:<7s} : {1:<s}'.format('状态', result[4]))