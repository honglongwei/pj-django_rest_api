#_*_ coding:utf-8 _*_

import urllib2
import sys
import cobbler
import xmlrpclib 
from celery import task
from models import AutoMsg


class CobblerAPI(object):
    def __init__(self, url, user, password):
        self.cobbler_user= user
        self.cobbler_pass = password
        self.cobbler_url = url
    
    def add_system(self, hostname, ip_add, mac_add, profile, ipmi_add, ipmi_user, ipmi_pass):
        '''
        Add Cobbler System Infomation
        '''
        ret = {
            "result": True,
            "comment": [],
        }
        
        remote = xmlrpclib.Server(self.cobbler_url) 
        token = remote.login(self.cobbler_user, self.cobbler_pass) 
        system_id = remote.new_system(token) 
        remote.modify_system(system_id, "name", hostname, token) 
        remote.modify_system(system_id, "hostname", hostname, token) 
        remote.modify_system(system_id, 'modify_interface', { 
            "macaddress-eth0" : mac_add, 
            "ipaddress-eth0" : ip_add, 
            "dnsname-eth0" : hostname, 
        }, token) 
        remote.modify_system(system_id, "profile", profile, token) 
        remote.modify_system(system_id, "power_type", "ipmilan", token) 
        remote.modify_system(system_id, "power_address", ipmi_add, token) 
        remote.modify_system(system_id, "power_user", ipmi_user, token) 
        remote.modify_system(system_id, "power_pass", ipmi_pass, token) 
        remote.save_system(system_id, token) 
        try:
            remote.sync(token)
        except Exception as e:
            ret['result'] = False
            ret['comment'].append(str(e))
        return ret



@task()
def AutoInstall(ID):
    cobbler = CobblerAPI('http://127.0.0.1/cobbler_api', 'admin', '111111')
    dt = AutoMsg.objects.get(id=ID)
    try:
        ret = cobbler.add_system(hostname=str(dt.HostName), 
                                 ip_add=str(dt.IP), 
                                 mac_add=str(dt.Mac), 
                                 profile=str(dt.osinfo), 
                                 ipmi_add=str(dt.IPMI_IP), 
                                 ipmi_user=str(dt.IPMI_User), 
                                 ipmi_pass=str(dt.IPMI_Pass)
           )
        return ret
    except:
        return 'invaild params!'
