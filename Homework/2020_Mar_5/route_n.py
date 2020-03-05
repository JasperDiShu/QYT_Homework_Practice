# 2020.03.05-Homework-route -n

import os
import re

route_n_result = os.popen('route -n').read()

result_list = route_n_result.split('\n')

for result in result_list:
    output = re.match('(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})\s+(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})\s+(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,'
                      '3})\s+(\w*)\s+(\d{1,4})\s+(\d{1,3})\s+(\d{1,3})\s+(\w*)', result)
    if output is not None:
        gateway_output = output.groups()[1]
        if '0.0.0.0' not in gateway_output:
                gateway = gateway_output
                print('网关为：' + gateway)