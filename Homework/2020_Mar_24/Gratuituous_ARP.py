#!/usr/bin/env python3
# _*_ coding=utf-8 _*_

# 2020.03.24-Homework--gratuituous_arp

from kamene.all import *
import logging
logging.getLogger("kamene.runtime").setLevel(logging.ERROR)

localmac = '00:0c:29:33:66:4d'
broadcastmac = 'ff:ff:ff:ff:ff:ff'


def create_arp_request_gratuituous(ipaddr_to_broadcast):
    arp = ARP(psrc=ipaddr_to_broadcast,
              hwsrc=localmac,
              pdst=ipaddr_to_broadcast)
    return Ether(dst=broadcastmac) / arp


def send_gratuituous_arp(ipaddr):
    g_arp = create_arp_request_gratuituous(ipaddr)
    while True:
        try:
            sendp(g_arp)
            time.sleep(5)
        except KeyboardInterrupt:
            print('Stop by Ctrl+C or stop button!')


if __name__ == '__main__':
    send_gratuituous_arp('192.168.200.101')
