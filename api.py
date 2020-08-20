from flask import Flask
from pyzabbix import ZabbixAPI
from flask import request
import sys

zabbixIP = sys.argv[1]
app = Flask('__zabbixAPI__')
zapi = ZabbixAPI("http://"+zabbixIP)


@app.route('/test')
def test():
    return 'zabbixIP:'+zabbixIP


@app.route('/login')
def login():
    zapi.login("Admin", "zabbix")
    return zapi.auth


@app.route('/example/hostName')
def getHostNameExp():
    login()
    hostResp = zapi.host.get(filter={'host': ['BIGDATADEV_1_LINUXS']})
    result = {
        'code': 0,
        'data': hostResp,
        'message': ''
    }
    return result


@app.route('/example/curValue')
def getCurValueExp():
    resultMap = {}
    hostName = request.args.get('hostName')
    itemName = request.args.get('itemName')

    login()
    # 获取hostid
    hostResp = zapi.host.get(filter={'host': [hostName]})
    hostid = hostResp[0]['hostid']

    # 查询item的值
    itemResp = zapi.item.get(output='extend', hostids=hostid,
                             search={'name': itemName}, sortfield='name')

    resultMap[hostName] = {
        itemName: itemResp[0]['lastvalue']
    }

    result = {
        'code': 0,
        'data': resultMap,
        'message': ''
    }

    return result
