#!/usr/bin/env python3
# _*_ coding=utf-8 _*_

# 2020.04.03-Homework--snmp trap ospf neighbor

from pysnmp.carrier.asynsock.dispatch import AsynsockDispatcher
from pysnmp.carrier.asynsock.dgram import udp, udp6
from pyasn1.codec.ber import decoder
from pysnmp.proto import api
from pprint import pprint
from netifaces import interfaces, ifaddresses, AF_INET, AF_INET6


# 只考虑在linux平台上使用


def get_ip_address(ifname):
    try:
        return ifaddresses(ifname)[AF_INET][0]['addr']
    except ValueError:
        return None


def analysis(info):
    # 分析Trap信息字典函数
    # 下面是这个大字典的键值与嵌套的小字典
    # 1.3.6.1.2.1.1.3.0 {'value': 'ObjectSyntax', 'application-wide': 'ApplicationSyntax', 'timeticks-value': '103170310'}
    # 1.3.6.1.6.3.1.1.4.1.0 {'value': 'ObjectSyntax', 'simple': 'SimpleSyntax', 'objectID-value': '1.3.6.1.6.3.1.1.5.4'}
    # 1.3.6.1.2.1.2.2.1.1.2 {'value': 'ObjectSyntax', 'simple': 'SimpleSyntax', 'integer-value': '2'}
    # 1.3.6.1.2.1.2.2.1.2.2 {'value': 'ObjectSyntax', 'simple': 'SimpleSyntax', 'string-value': 'GigabitEthernet2'}
    # 1.3.6.1.2.1.2.2.1.3.2 {'value': 'ObjectSyntax', 'simple': 'SimpleSyntax', 'integer-value': '6'}

    # if '1.3.6.1.6.3.1.1.4.1.0' in info.keys():
    #     if info["1.3.6.1.6.3.1.1.4.1.0"]['objectID-value'] == '1.3.6.1.6.3.1.1.5.4':
    #         print(info["1.3.6.1.2.1.2.2.1.2.2"]['string-value'], "UP")
    #     elif info["1.3.6.1.6.3.1.1.4.1.0"]['objectID-value'] == '1.3.6.1.6.3.1.1.5.3':
    #         print(info["1.3.6.1.2.1.2.2.1.2.2"]['string-value'], "Down")

    # https://snmp.cloudapps.cisco.com/Support/SNMP/do/BrowseOID.do?objectInput=1.3.6.1.2.1.14.16.2.2&translate=Translate&submitValue=SUBMIT&submitClicked=true
    # 其他部分都是copy的教主的代码，如下部分是自己修改的满足需求的
    ospf_nei_router_id = info['1.3.6.1.2.1.14.10.1.3']['ipAddress-value']
    if '1.3.6.1.2.1.14.10.1.6' in info.keys():
        if info["1.3.6.1.2.1.14.10.1.6"]['integer-value'] == '1':
            print('OSPF Neighbor ' + ospf_nei_router_id + ' down')
        elif info["1.3.6.1.2.1.14.10.1.6"]['integer-value'] == '8':
            print('OSPF Neighbor ' + ospf_nei_router_id + ' full')
        else:
            pprint(info, indent=4)


def cbFun(transportDispatcher, transportDomain, transportAddress, wholeMsg):
    while wholeMsg:
        msgVer = int(api.decodeMessageVersion(wholeMsg))
        if msgVer in api.protoModules:
            pMod = api.protoModules[msgVer]
        else:
            print('Unsupported SNMP version %s' % msgVer)
            return
        reqMsg, wholeMsg = decoder.decode(
            wholeMsg, asn1Spec=pMod.Message(),
        )
        print('Notification message from %s:%s:' % (
            transportDomain, transportAddress
        )
              )
        reqPDU = pMod.apiMessage.getPDU(reqMsg)
        if reqPDU.isSameTypeWith(pMod.TrapPDU()):
            if msgVer == api.protoVersion1:
                print('Enterprise: %s' % (
                    pMod.apiTrapPDU.getEnterprise(reqPDU).prettyPrint()
                )
                      )
                print('Agent Address: %s' % (
                    pMod.apiTrapPDU.getAgentAddr(reqPDU).prettyPrint()
                )
                      )
                print('Generic Trap: %s' % (
                    pMod.apiTrapPDU.getGenericTrap(reqPDU).prettyPrint()
                )
                      )
                print('Specific Trap: %s' % (
                    pMod.apiTrapPDU.getSpecificTrap(reqPDU).prettyPrint()
                )
                      )
                print('Uptime: %s' % (
                    pMod.apiTrapPDU.getTimeStamp(reqPDU).prettyPrint()
                )
                      )
                varBinds = pMod.apiTrapPDU.getVarBindList(reqPDU)
            else:
                varBinds = pMod.apiPDU.getVarBindList(reqPDU)

            result_dict = {}

            for x in varBinds:
                result = {}
                for x, y in x.items():
                    if x == "name":
                        id = y.prettyPrint()
                    else:
                        bind_v = [x.strip() for x in y.prettyPrint().split(':')]
                        for v in bind_v:
                            if v == '_BindValue':
                                next
                            else:
                                result[v.split('=')[0]] = v.split('=')[1]
                result_dict[id] = result
            analysis(result_dict)
    return wholeMsg


def snmp_trap_receiver(ifname, port=162):
    if_ip = get_ip_address(ifname)
    transportDispatcher = AsynsockDispatcher()
    transportDispatcher.registerRecvCbFun(cbFun)

    # UDP/IPv4
    transportDispatcher.registerTransport(
        udp.domainName, udp.UdpSocketTransport().openServerMode((if_ip, port))
    )

    transportDispatcher.jobStarted(1)
    print("SNMP Trap Receiver Started!!!")
    try:
        transportDispatcher.runDispatcher()
    except:
        transportDispatcher.closeDispatcher()
        raise


if __name__ == '__main__':
    snmp_trap_receiver("ens33")
