# 2020.03.06-Homework-sort interface name

import re

port_list = ['eth 1/101/1/42','eth 1/101/1/26','eth 1/101/1/23','eth 1/101/1/7','eth 1/101/2/46','eth 1/101/1/34','eth 1/101/1/18','eth 1/101/1/13','eth 1/101/1/32','eth 1/101/1/25','eth 1/101/1/45','eth 1/101/2/8']

print(sorted(port_list, key=lambda x: (int(re.match('^eth (\d)/(\d\d\d)/(\d)/(\d+)', x).groups()[2]), int(re.match('^eth (\d)/(\d\d\d)/(\d)/(\d+)', x).groups()[3]))))
