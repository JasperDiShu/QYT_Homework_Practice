# 2020.03.10-Homework-while for monitor http

import os
import time
import re

while True:
    try:
        time.sleep(1)
        http80up = False
        print('等待一秒重新开始监控！')
        command_output = os.popen('netstat -tulnp').read()
        # command_output = 'tcp        0      0 0.0.0.0:8080              0.0.0.0:*               LISTEN      1274/sshd'
        for x in command_output.split('\n'):
            re_result = re.match('(\w*)\s+(\d{1,5})\s+(\d{1,5})\s+(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}:\d*)\s+(\d{1,3}.\d{1,'
                         '3}.\d{1,3}.\d{1,3}):\W\s+(\w*)\s+(\d{1,5}/\w*)', x)

            if re_result != None and re_result.groups()[0] == 'tcp':
                # print(re_result.groups()[0])
                local_addr = re_result.groups()[3]
                if (':80' in local_addr[-3:]):
                    # print(local_addr)
                    print('HTTP（TCP/80）服务已经被打开')
                    http80up = True
        if http80up:
            break
    except KeyboardInterrupt:
        print('stop by button')
