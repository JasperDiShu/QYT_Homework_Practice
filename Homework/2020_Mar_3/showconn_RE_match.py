# 2020.03.03-Homework-showconn_RE_match

import re

str1 = 'TCP server 172.16.1.101:443 localserver 172.16.66.1:53710, idle 0:01:09, bytes 27575949, flags UIO'

result = re.match('(\w*)\s+(\w*)\s+(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}:\d{1,5})\s+(\w*)\s+(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}:\d{1,'
               '5}\W)\s+(\w*)\s+(\d{1,2}:\d{1,2}:\d{1,2}\W)\s+(\w*)\s+(\d{1,10}\W)\s+(\w*)\s+(\w*)', str1).groups()

protocol = '{0:<20s} : {1:s}'.format('protocol', result[0])
server = '{0:<20s} : {1:s}'.format('server', result[2])
localserver = '{0:<20s} : {1:s}'.format('localserver', result[4][:-1])
idle_result = result[6].split(':')[0] + ' 小时 ' + result[6].split(':')[1] + '分钟 ' + result[6].split(':')[2][:-1] + '秒'
idle = '{0:<20s} : {1:s}'.format('idle', idle_result)
bytes = '{0:<20s} : {1:s}'.format('bytes', result[8][:-1])
flags = '{0:<20s} : {1:s}'.format('flags', result[10])

print(protocol)
print(server)
print(localserver)
print(idle)
print(bytes)
print(flags)

# 为了练习re.match就先这样吧，也试过用split先以空格分隔，然后再对各部分做re.match找到需要的值，那样是不是效率会更高一点啊？？？