# 2020.03.04-Homework-linux ifconfig output

import os
import re

ifconfig_result = os.popen('ifconfig ' + 'ens33').read()

ipv4_add = re.findall('\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}', ifconfig_result)[0]
netmask = re.findall('255.255.\d{1,3}.\d{1,3}', ifconfig_result)[0]
broadcast = re.findall(str(ipv4_add.split('.')[0]) + '.\d{1,3}.\d{1,3}.255', ifconfig_result)[0]
mac_addr = re.findall('\w{2}:\w{2}:\w{2}:\w{2}:\w{2}:\w{2}', ifconfig_result)[0]

format_string = '{0:<10s}:{1:s}'

print(format_string.format('ipv4_add', ipv4_add))
print(format_string.format('netmask', netmask))
print(format_string.format('broadcast', broadcast))
print(format_string.format('mac_addr', mac_addr))

ipv4_gw_tmp = ipv4_add.split('.')
ipv4_gw = ipv4_gw_tmp[0] + '.' + ipv4_gw_tmp[1] + '.' + ipv4_gw_tmp[2] + '.' + '254'
# real_ipv4_gw = ipv4_gw_tmp[0] + '.' + ipv4_gw_tmp[1] + '.' + ipv4_gw_tmp[2] + '.' + '2'

print('\n我们假设网关IP地址为最后一位为254， 因此网关IP地址为:' + ipv4_gw + '\n')

ping_result = os.popen('ping ' + ipv4_gw + ' -c 1').read()
# real_ping_result = os.popen('ping ' + real_ipv4_gw + ' -c 1').read()

re_ping_result = re.findall('64 bytes from', ping_result)

if re_ping_result:
    print('网关可达！')     #我的Linux VM的网关为192.168.200.2，不是.254,所以实际显示的测试结果为网关不可达
else:
    print('网关不可达！')
