# 2020.02.29 homework-Random_IPv4

import random

a = random.randint(0, 255)
b = random.randint(0, 255)
c = random.randint(0, 255)
d = random.randint(0, 255)

ipv4_address = str(a) + '.' + str(b) + '.' + str(c) + '.' + str(d)

print(ipv4_address)