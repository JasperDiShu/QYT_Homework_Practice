# 2020.03.03-Homework-MAC_RE_match

import re

str1 = '166 54a2.74f7.0326 DYNAMIC Gi1/0/11'

result = re.match('(\d{1,4})\s+(\w*.\w*.\w*.\w*)\s+(\w*)\s+(\w*/\w*/\w*)', str1).groups()

VLAN_ID = '{0:<10s} : {1:<s}'.format('VLAN ID', result[0])
MAC = '{0:<10s} : {1:<s}'.format('MAC', result[1])
Type = '{0:<10s} : {1:<s}'.format('Type', result[2])
Interface = '{0:<10s} : {1:<s}'.format('Interface', result[3])

print(VLAN_ID)
print(MAC)
print(Type)
print(Interface)