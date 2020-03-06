# 2020.03.06-Homework-firewall connection

import re

asa_conn = "TCP Student 192.168.189.167:32806 Teacher 137.78.5.128:65247, idle 0:00:00, bytes 74, flags UIO\n TCP Student 192.168.189.167:80 Teacher 137.78.5.128:65233, idle 0:00:03, bytes 334516, flags UIO"

asa_dict = {}

for conn in asa_conn.split('\n'):
    re_result = re.match('\s*TCP Student\s+(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}):(\d{1,5})\s+Teacher\s+(\d{1,3}.\d{1,3}.\d{1,'
                   '3}.\d{1,3}):(\d{1,5}),\s+idle\s+(\d{1,3}:\d{1,3}:\d{1,3}),\s+bytes\s+(\d{1,10}),\s+(\w*)\s+(\w*)',
                   conn)

    asa_dict[(re_result.groups()[0],re_result.groups()[1],re_result.groups()[2],re_result.groups()[3])] = (re_result.groups()[5],
                                                                                                           re_result.groups()[7])

print('打印分析后的字典！\n')
print(asa_dict)

src = 'src'
src_ip = 'src_ip'
dst = 'dst'
dst_ip = 'dst_ip'
bytes_name = 'bytes'
flags = 'flags'
format_str1 = '{0:^10s}:{1:^15s}|{2:^10s}:{3:^15s}|{4:^10s}:{5:^15s}|{6:^10}:{7:^15s}'
format_str2 = '{0:^10s}:{1:^15s}|{2:^10s}:{3:^15s}'

print('\n格式化打印输出\n')

for key, value in asa_dict.items():
    format_result1= format_str1.format(src, key[0], src_ip, key[1], dst, key[2], dst_ip, key[3])
    format_result2= format_str2.format(bytes_name, value[0], flags, value[1])
    print(format_result1)
    print(format_result2)
    print('='*len(format_result1))
